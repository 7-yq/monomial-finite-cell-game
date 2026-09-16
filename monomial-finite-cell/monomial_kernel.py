"""Exact kernel for pair-poset monomial finite-cell presentations.

The kernel recognizes presentations whose attached cells are exactly the
descent words of a finite partially ordered set of two-arrow blocks.  For that
subclass, properness is decided by the finite support automaton from the
pair-poset word-complex criterion; no cochain formulas or search cutoffs are
used.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterable, Optional


Word = tuple[str, ...]
Pair = tuple[str, str]
State = tuple[str, Optional[Pair], int]

MAX_EXPECTED_CELLS = 50_000
MAX_SUPPORT_PREVIEW = 24
MAX_BASIS_ELEMENTS = 100_000


def _flatten_spec(spec: Any) -> Word | None:
    if not isinstance(spec, dict):
        return None

    kind = spec.get("type")

    if kind == "arrow":
        name = spec.get("name")
        return (str(name),) if name else None

    if kind == "path":
        names = spec.get("arrows")
        if not isinstance(names, list) or not names:
            return None
        return tuple(str(name) for name in names)

    if kind in {"mp", "massey"}:
        parts = [_flatten_spec(item) for item in spec.get("inputs", [])]
    elif kind == "product":
        parts = [_flatten_spec(item) for item in spec.get("factors", [])]
    else:
        return None

    if not parts or any(part is None for part in parts):
        return None

    return tuple(name for part in parts for name in part)


def _word_label(word: Iterable[str]) -> str:
    return "".join(str(name) for name in word)


def _transitive_closure(relations: set[tuple[Pair, Pair]]) -> set[tuple[Pair, Pair]]:
    closure = set(relations)
    changed = True

    while changed:
        changed = False
        additions = {
            (left, right)
            for left, middle in closure
            for source, right in closure
            if middle == source and (left, right) not in closure
        }
        if additions:
            closure.update(additions)
            changed = True

    return closure


def _expected_descent_words(
    selected_pairs: set[Pair],
    order: set[tuple[Pair, Pair]],
) -> set[Word] | None:
    expected: set[Word] = {tuple(pair) for pair in selected_pairs}
    queue = deque(expected)

    while queue:
        word = queue.popleft()
        previous = (word[-2], word[-1])

        for following in selected_pairs:
            if following[0] != word[-1] or (previous, following) not in order:
                continue

            extension = (*word, following[1])
            if extension in expected:
                continue

            expected.add(extension)
            if len(expected) > MAX_EXPECTED_CELLS:
                return None
            queue.append(extension)

    return expected


def _extract_presentation(actions: list[dict[str, Any]]) -> dict[str, Any]:
    vertex_order = list(dict.fromkeys(
        str(action.get("name"))
        for action in actions
        if action.get("kind") == "add_vertex" and action.get("name")
    ))
    vertices = set(vertex_order)
    arrows = {
        str(action.get("name")): (
            str(action.get("source")),
            str(action.get("target")),
        )
        for action in actions
        if action.get("kind") == "add_arrow" and action.get("name")
    }
    arrow_gradings = {
        str(action.get("name")): (
            int(action.get("grading"))
            if action.get("grading") not in {None, ""}
            else 0
        )
        for action in actions
        if action.get("kind") == "add_arrow" and action.get("name")
    }
    unsupported_actions = sorted({
        str(action.get("kind"))
        for action in actions
        if action.get("kind") in {"attach_bridge", "autocomplete", "autocomplete_selected"}
    })
    cells: set[Word] = set()
    unflattened = 0

    for action in actions:
        if action.get("kind") != "attach_mp_cell":
            continue

        word = _flatten_spec(action.get("expression"))
        if word is None or any(name not in arrows for name in word):
            unflattened += 1
            continue
        cells.add(word)

    return {
        "vertices": vertices,
        "vertexOrder": vertex_order,
        "arrows": arrows,
        "arrowGradings": arrow_gradings,
        "cells": cells,
        "unflattened": unflattened,
        "unsupportedActions": unsupported_actions,
    }


def _pair_poset_data(presentation: dict[str, Any]) -> dict[str, Any]:
    arrows: dict[str, tuple[str, str]] = presentation["arrows"]
    cells: set[Word] = presentation["cells"]

    if presentation["unsupportedActions"]:
        return {
            "kind": "unsupported",
            "reason": "The action log contains generated multi-cell operations.",
        }

    if presentation["unflattened"]:
        return {
            "kind": "unsupported",
            "reason": "Some attached differentials do not flatten to base-arrow words.",
        }

    singleton_cells = sorted(word for word in cells if len(word) < 2)
    if singleton_cells:
        return {
            "kind": "unsupported",
            "reason": "Singleton-killing cells lie outside the pair-poset subclass.",
        }

    noncomposable = sorted({
        word
        for word in cells
        if any(
            arrows[left][1] != arrows[right][0]
            for left, right in zip(word, word[1:])
        )
    })
    if noncomposable:
        return {
            "kind": "unsupported",
            "reason": "An attached cell word is not composable.",
            "invalidCells": [_word_label(word) for word in noncomposable[:8]],
        }

    missing_intervals = sorted({
        word[start:end]
        for word in cells
        for start in range(len(word))
        for end in range(start + 2, len(word) + 1)
        if end - start < len(word) and word[start:end] not in cells
    })
    if missing_intervals:
        return {
            "kind": "unsupported",
            "reason": "The attached cell language is not interval-closed.",
            "missingIntervals": [
                _word_label(word) for word in missing_intervals[:12]
            ],
        }

    selected_pairs = {tuple(word) for word in cells if len(word) == 2}
    relations = {
        ((word[index], word[index + 1]), (word[index + 1], word[index + 2]))
        for word in cells
        for index in range(len(word) - 2)
    }
    order = _transitive_closure(relations)

    if any(left == right for left, right in order):
        return {
            "kind": "unsupported",
            "reason": "The inferred two-block order contains a cycle.",
        }

    expected = _expected_descent_words(selected_pairs, order)
    if expected is None:
        return {
            "kind": "unsupported",
            "reason": "The inferred descent language is too large for the exact kernel.",
        }

    longer_cells = {word for word in cells if len(word) >= 2}
    missing_cells = sorted(expected - longer_cells, key=lambda word: (len(word), word))
    extra_cells = sorted(longer_cells - expected, key=lambda word: (len(word), word))

    if extra_cells:
        return {
            "kind": "unsupported",
            "reason": "Some cells are not descent words for the inferred pair order.",
            "extraCells": [_word_label(word) for word in extra_cells[:12]],
        }

    common = {
        "selectedPairs": sorted(_word_label(pair) for pair in selected_pairs),
        "selectedPairCount": len(selected_pairs),
        "orderRelationCount": len(order),
        "cellCount": len(cells),
        "selectedPairData": selected_pairs,
        "orderData": order,
    }

    if missing_cells:
        return {
            **common,
            "kind": "incomplete_pair_poset",
            "reason": "The compatible descent-cell system is incomplete.",
            "missingCells": [_word_label(word) for word in missing_cells[:24]],
            "missingCellWords": [list(word) for word in missing_cells[:24]],
            "missingCellCount": len(missing_cells),
        }

    return {
        **common,
        "kind": "pair_poset",
        "reason": "The cells form a complete pair-poset descent language.",
    }


def _next_state(
    state: State,
    next_arrow: str,
    selected_pairs: set[Pair],
    order: set[tuple[Pair, Pair]],
) -> State | None:
    last_arrow, last_selected, residue = state
    new_pair = (last_arrow, next_arrow)

    if new_pair not in selected_pairs:
        if residue == 1:
            return None
        return (next_arrow, None, 0)

    if last_selected is not None and (last_selected, new_pair) not in order:
        return (next_arrow, new_pair, (residue + 1) % 3)

    if residue == 1:
        return None
    return (next_arrow, new_pair, 1)


def _reachable_automaton(
    arrows: dict[str, tuple[str, str]],
    selected_pairs: set[Pair],
    order: set[tuple[Pair, Pair]],
) -> tuple[
    list[tuple[State, str]],
    dict[State, list[tuple[State, str]]],
    dict[State, tuple[State | None, str]],
]:
    starts = [((name, None, 0), name) for name in sorted(arrows)]
    graph: dict[State, list[tuple[State, str]]] = {}
    parent: dict[State, tuple[State | None, str]] = {
        state: (None, label) for state, label in starts
    }
    queue = deque(state for state, _label in starts)

    while queue:
        state = queue.popleft()
        last_arrow = state[0]
        edges: list[tuple[State, str]] = []

        for name, (source, _target) in sorted(arrows.items()):
            if arrows[last_arrow][1] != source:
                continue

            following = _next_state(state, name, selected_pairs, order)
            if following is None:
                continue

            edges.append((following, name))
            if following not in parent:
                parent[following] = (state, name)
                queue.append(following)

        graph[state] = edges

    return starts, graph, parent


def _coaccessible_states(graph: dict[State, list[tuple[State, str]]]) -> set[State]:
    reverse: dict[State, list[State]] = {state: [] for state in graph}
    for state, edges in graph.items():
        for target, _label in edges:
            reverse.setdefault(target, []).append(state)

    productive = {state for state in graph if state[2] != 1}
    queue = deque(productive)

    while queue:
        state = queue.popleft()
        for previous in reverse.get(state, []):
            if previous not in productive:
                productive.add(previous)
                queue.append(previous)

    return productive


def _find_cycle(
    graph: dict[State, list[tuple[State, str]]],
    productive: set[State],
) -> tuple[State, list[str]] | None:
    colors: dict[State, int] = {}
    stack: list[State] = []
    stack_edges: list[str] = []
    positions: dict[State, int] = {}

    def visit(state: State) -> tuple[State, list[str]] | None:
        colors[state] = 1
        positions[state] = len(stack)
        stack.append(state)

        for target, label in graph.get(state, []):
            if target not in productive:
                continue
            if colors.get(target, 0) == 0:
                stack_edges.append(label)
                found = visit(target)
                if found is not None:
                    return found
                stack_edges.pop()
            elif colors.get(target) == 1:
                start = positions[target]
                return target, [*stack_edges[start:], label]

        stack.pop()
        positions.pop(state, None)
        colors[state] = 2
        return None

    for state in productive:
        if colors.get(state, 0) == 0:
            found = visit(state)
            if found is not None:
                return found

    return None


def _prefix_word(
    state: State,
    parent: dict[State, tuple[State | None, str]],
) -> list[str]:
    labels = []
    current: State | None = state

    while current is not None:
        previous, label = parent[current]
        labels.append(label)
        current = previous

    return list(reversed(labels))


def _accepting_suffix(
    start: State,
    graph: dict[State, list[tuple[State, str]]],
    productive: set[State],
) -> list[str]:
    if start[2] != 1:
        return []

    queue = deque([(start, [])])
    seen = {start}

    while queue:
        state, labels = queue.popleft()
        for target, label in graph.get(state, []):
            if target not in productive or target in seen:
                continue
            following = [*labels, label]
            if target[2] != 1:
                return following
            seen.add(target)
            queue.append((target, following))

    return []


def _finite_support_summary(
    starts: list[tuple[State, str]],
    graph: dict[State, list[tuple[State, str]]],
    productive: set[State],
) -> dict[str, Any]:
    memo: dict[State, tuple[int, int]] = {}

    def totals(state: State) -> tuple[int, int]:
        if state in memo:
            return memo[state]

        count = 1 if state[2] != 1 else 0
        longest = 0 if state[2] != 1 else -1

        for target, _label in graph.get(state, []):
            if target not in productive:
                continue
            child_count, child_longest = totals(target)
            count += child_count
            if child_longest >= 0:
                longest = max(longest, child_longest + 1)

        memo[state] = (count, longest)
        return memo[state]

    support_count = 0
    max_length = 0
    for state, _label in starts:
        if state not in productive:
            continue
        count, extra_length = totals(state)
        support_count += count
        if extra_length >= 0:
            max_length = max(max_length, extra_length + 1)

    preview: list[str] = []
    preview_words: list[list[str]] = []
    queue = deque(
        (state, (label,))
        for state, label in starts
        if state in productive
    )
    while queue and len(preview) < MAX_SUPPORT_PREVIEW:
        state, word = queue.popleft()
        if state[2] != 1:
            preview.append(_word_label(word))
            preview_words.append(list(word))
        for target, label in graph.get(state, []):
            if target in productive:
                queue.append((target, (*word, label)))

    return {
        "supportWordCount": support_count,
        "maxSupportedLength": max_length,
        "supportedWordPreview": preview,
        "supportedWordData": preview_words,
    }


def _finite_supported_words(
    starts: list[tuple[State, str]],
    graph: dict[State, list[tuple[State, str]]],
    productive: set[State],
) -> list[Word]:
    """Enumerate the finite accepted support language in length-lexicographic order."""

    words: list[Word] = []
    queue = deque(
        (state, (label,))
        for state, label in starts
        if state in productive
    )

    while queue:
        state, word = queue.popleft()

        if state[2] != 1:
            words.append(word)

            if len(words) > MAX_BASIS_ELEMENTS:
                raise ValueError(
                    "The finite cohomology basis is too large to display safely."
                )

        for target, label in graph.get(state, []):
            if target in productive:
                queue.append((target, (*word, label)))

    return words


def _spec_degree(spec: Any, arrow_gradings: dict[str, int]) -> int:
    if not isinstance(spec, dict):
        return 0

    kind = spec.get("type")

    if kind == "arrow":
        return int(arrow_gradings.get(str(spec.get("name")), 0))

    if kind == "path":
        return sum(
            int(arrow_gradings.get(str(name), 0))
            for name in spec.get("arrows", [])
        )

    if kind == "product":
        return sum(
            _spec_degree(factor, arrow_gradings)
            for factor in spec.get("factors", [])
        )

    if kind in {"mp", "massey"}:
        inputs = list(spec.get("inputs", []))
        return 2 - len(inputs) + sum(
            _spec_degree(item, arrow_gradings)
            for item in inputs
        )

    return 0


def _word_degree(word: Word, arrow_gradings: dict[str, int]) -> int:
    degree = sum(int(arrow_gradings.get(name, 0)) for name in word)
    return degree if len(word) == 1 else degree + 2 - len(word)


def _basis_spec(word: Word) -> dict[str, Any]:
    inputs = [{"type": "arrow", "name": name} for name in word]

    if len(inputs) == 1:
        return inputs[0]

    return {"type": "mp", "inputs": inputs}


def _integer_determinant(matrix: list[list[int]]) -> int:
    """Compute an exact integer determinant with fraction-free elimination."""

    size = len(matrix)

    if size == 0:
        return 1

    work = [list(map(int, row)) for row in matrix]
    sign = 1
    previous = 1

    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap_index = next(
                (
                    row_index
                    for row_index in range(pivot_index + 1, size)
                    if work[row_index][pivot_index] != 0
                ),
                None,
            )

            if swap_index is None:
                return 0

            work[pivot_index], work[swap_index] = (
                work[swap_index],
                work[pivot_index],
            )
            sign *= -1

        pivot = work[pivot_index][pivot_index]

        for row_index in range(pivot_index + 1, size):
            for column_index in range(pivot_index + 1, size):
                numerator = (
                    work[row_index][column_index] * pivot
                    - work[row_index][pivot_index]
                    * work[pivot_index][column_index]
                )
                work[row_index][column_index] = numerator // previous

        previous = pivot

    return sign * work[-1][-1]


def _ordinary_cartan(
    vertices: list[str],
    basis: list[dict[str, Any]],
) -> dict[str, Any]:
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    matrix = [[0 for _target in vertices] for _source in vertices]

    for entry in basis:
        source = positions[entry["source"]]
        target = positions[entry["target"]]
        matrix[source][target] += -1 if int(entry["grading"]) % 2 else 1

    return {
        "matrix": matrix,
        "determinant": _integer_determinant(matrix),
    }


def _cellular_cartan(
    actions: list[dict[str, Any]],
    presentation: dict[str, Any],
) -> dict[str, Any]:
    vertices = list(presentation["vertexOrder"])
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    arrows = presentation["arrows"]
    arrow_gradings = presentation["arrowGradings"]
    matrix = [
        [1 if source == target else 0 for target in vertices]
        for source in vertices
    ]
    cellular_basis: list[dict[str, Any]] = []

    for name, (source, target) in arrows.items():
        cellular_basis.append({
            "kind": "generator",
            "label": name,
            "source": source,
            "target": target,
            "grading": int(arrow_gradings.get(name, 0)),
        })

    cell_index = 0
    for action in actions:
        if action.get("kind") != "attach_mp_cell":
            continue

        expression = action.get("expression")
        word = _flatten_spec(expression)

        if not word:
            continue

        cell_index += 1
        cellular_basis.append({
            "kind": "cell",
            "label": f"cell_{cell_index}",
            "source": arrows[word[0]][0],
            "target": arrows[word[-1]][1],
            "grading": _spec_degree(expression, arrow_gradings) - 1,
        })

    for entry in cellular_basis:
        source = positions[entry["source"]]
        target = positions[entry["target"]]
        sign = -1 if int(entry["grading"]) % 2 else 1
        matrix[source][target] -= sign

    return {
        "matrix": matrix,
        "determinant": _integer_determinant(matrix),
        "cellularBasisCount": len(cellular_basis),
    }


def _analyze_support_automaton(
    arrows: dict[str, tuple[str, str]],
    selected_pairs: set[Pair],
    order: set[tuple[Pair, Pair]],
) -> dict[str, Any]:
    starts, graph, parent = _reachable_automaton(arrows, selected_pairs, order)
    productive = _coaccessible_states(graph)
    cycle = _find_cycle(graph, productive)

    common = {
        "automatonStateCount": len(graph),
        "productiveStateCount": len(productive),
    }

    if cycle is not None:
        cycle_state, cycle_labels = cycle
        prefix = _prefix_word(cycle_state, parent)
        suffix = _accepting_suffix(cycle_state, graph, productive)
        return {
            **common,
            "proper": False,
            "infiniteSupport": True,
            "witnessPrefix": _word_label(prefix),
            "repeatableBlock": _word_label(cycle_labels),
            "witnessSuffix": _word_label(suffix),
            "supportedWordWitness": _word_label([*prefix, *cycle_labels, *suffix]),
            "supportedWordWitnessLength": len(prefix) + len(cycle_labels) + len(suffix),
        }

    return {
        **common,
        "proper": True,
        "infiniteSupport": False,
        **_finite_support_summary(starts, graph, productive),
    }


def analyze_monomial_actions(actions: list[dict[str, Any]]) -> dict[str, Any]:
    """Return an exact pair-poset verdict or a conservative applicability result."""

    presentation = _extract_presentation(actions)
    pair_poset = _pair_poset_data(presentation)
    public = {
        key: value
        for key, value in pair_poset.items()
        if key not in {"selectedPairData", "orderData"}
    }
    public.update({
        "vertexCount": len(presentation["vertices"]),
        "generatorCount": len(presentation["arrows"]),
    })

    if pair_poset.get("kind") != "pair_poset":
        public["applicable"] = pair_poset.get("kind") == "incomplete_pair_poset"
        public["exact"] = False
        public["proper"] = None
        return public

    automaton = _analyze_support_automaton(
        presentation["arrows"],
        pair_poset["selectedPairData"],
        pair_poset["orderData"],
    )
    public.update(automaton)
    public["applicable"] = True
    public["exact"] = True
    if automaton["proper"]:
        cells = presentation["cells"]
        higher_massey_words = [
            tuple(word)
            for word in automaton.get("supportedWordData", [])
            if len(word) >= 3
            and tuple(word) not in cells
            and all(
                tuple(word[start:end]) in cells
                for start in range(len(word))
                for end in range(start + 2, len(word) + 1)
                if end - start < len(word)
            )
        ]
        public["higherMasseyClassPreview"] = [
            _word_label(word) for word in higher_massey_words
        ]
        public["higherMasseyClassWordPreview"] = [
            list(word) for word in higher_massey_words
        ]
        public["cohomologyDimension"] = (
            len(presentation["vertices"])
            + int(automaton["supportWordCount"])
        )
    return public


def compute_victory_invariants(actions: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute the finite cohomology basis and Cartan data for an exact victory."""

    presentation = _extract_presentation(actions)
    pair_poset = _pair_poset_data(presentation)

    if pair_poset.get("kind") != "pair_poset":
        return {
            "available": False,
            "reason": pair_poset.get("reason")
            or "The exact pair-poset presentation is incomplete.",
        }

    starts, graph, _parent = _reachable_automaton(
        presentation["arrows"],
        pair_poset["selectedPairData"],
        pair_poset["orderData"],
    )
    productive = _coaccessible_states(graph)

    if _find_cycle(graph, productive) is not None:
        return {
            "available": False,
            "reason": "The support language is infinite, so no finite basis exists.",
        }

    try:
        words = _finite_supported_words(starts, graph, productive)
    except ValueError as exc:
        return {"available": False, "reason": str(exc)}

    vertices = list(presentation["vertexOrder"])
    arrows = presentation["arrows"]
    arrow_gradings = presentation["arrowGradings"]
    basis = [
        {
            "kind": "identity",
            "label": f"e_{vertex}",
            "spec": {"type": "identity", "vertex": vertex},
            "source": vertex,
            "target": vertex,
            "grading": 0,
            "arity": 0,
            "word": [],
        }
        for vertex in vertices
    ]

    for word in words:
        basis.append({
            "kind": "generator" if len(word) == 1 else "higher_product",
            "label": (
                word[0]
                if len(word) == 1
                else f"m_{len(word)}({','.join(word)})"
            ),
            "spec": _basis_spec(word),
            "source": arrows[word[0]][0],
            "target": arrows[word[-1]][1],
            "grading": _word_degree(word, arrow_gradings),
            "arity": len(word),
            "word": list(word),
        })

    ordinary = _ordinary_cartan(vertices, basis)
    cellular = _cellular_cartan(actions, presentation)

    return {
        "available": True,
        "victory": True,
        "finite": True,
        "dimension": len(basis),
        "vertices": vertices,
        "basis": basis,
        "ordinaryCartan": ordinary,
        "cellularCartan": cellular,
        "gradingConvention": (
            "deg(m_n(a_1,...,a_n)) = 2 - n + sum deg(a_i); "
            "unspecified generator gradings are treated as 0."
        ),
    }
