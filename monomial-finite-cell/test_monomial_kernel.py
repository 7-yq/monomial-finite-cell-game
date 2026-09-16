from __future__ import annotations

import json
from pathlib import Path

from monomial_kernel import analyze_monomial_actions, compute_victory_invariants


ROOT = Path(__file__).resolve().parent.parent
LEGACY_SAVES = ROOT / "program-A-inf" / "saved quivers"


def analyze_save(name: str) -> dict:
    data = json.loads((LEGACY_SAVES / name).read_text())
    return analyze_monomial_actions(data["actions"])


def test_triangle_uses_exact_finite_support_certificate() -> None:
    result = analyze_save("triangle quiver.json")

    assert result["kind"] == "pair_poset"
    assert result["exact"] is True
    assert result["proper"] is True
    assert result["cohomologyDimension"] == 7
    assert result["maxSupportedLength"] == 3
    assert result["supportedWordPreview"] == ["x", "y", "z", "xyz"]


def test_triangle_victory_basis_and_cartan_determinants() -> None:
    data = json.loads((LEGACY_SAVES / "triangle quiver.json").read_text())
    result = compute_victory_invariants(data["actions"])

    assert result["available"] is True
    assert result["dimension"] == 7
    assert [entry["label"] for entry in result["basis"]] == [
        "e_1",
        "e_2",
        "e_3",
        "x",
        "y",
        "z",
        "m_3(x,y,z)",
    ]
    higher_class = result["basis"][-1]
    assert higher_class["grading"] == -1
    assert (higher_class["source"], higher_class["target"]) == ("1", "1")
    assert result["ordinaryCartan"] == {
        "matrix": [[0, 1, 0], [0, 1, 1], [1, 0, 1]],
        "determinant": 1,
    }
    assert result["cellularCartan"]["determinant"] == 1


def test_incomplete_g5_reports_the_missing_descent_cell() -> None:
    result = analyze_save("G5 Green algebra incomplete.json")

    assert result["kind"] == "incomplete_pair_poset"
    assert result["exact"] is False
    assert result["proper"] is None
    assert result["missingCells"] == ["x1x2x3x4x5"]
    assert result["missingCellWords"] == [["x1", "x2", "x3", "x4", "x5"]]


def test_completed_higher_g3_is_certified_proper() -> None:
    result = analyze_save("higher G3 completed(alike).json")

    assert result["kind"] == "pair_poset"
    assert result["proper"] is True
    assert result["cohomologyDimension"] == 10
    assert result["maxSupportedLength"] == 4


def test_productive_support_cycle_is_an_exact_nonproperness_witness() -> None:
    actions = [
        {"kind": "add_vertex", "name": "v"},
        {
            "kind": "add_arrow",
            "name": "x",
            "source": "v",
            "target": "v",
            "grading": None,
        },
    ]

    result = analyze_monomial_actions(actions)

    assert result["kind"] == "pair_poset"
    assert result["exact"] is True
    assert result["proper"] is False
    assert result["infiniteSupport"] is True
    assert result["repeatableBlock"] == "x"


def test_pdf_three_vertex_example_has_92_cells_and_dimension_23() -> None:
    endpoints = {
        "1": ("a", "b"),
        "4": ("a", "b"),
        "2": ("b", "c"),
        "5": ("b", "c"),
        "3": ("c", "a"),
        "6": ("c", "a"),
    }
    chains = (
        ("56", "61", "15", "53"),
        ("56", "64", "45", "53"),
        ("53", "34", "42", "23", "31", "12"),
    )
    order = {
        (larger, smaller)
        for chain in chains
        for index, larger in enumerate(chain)
        for smaller in chain[index + 1 :]
    }
    changed = True
    while changed:
        additions = {
            (left, right)
            for left, middle in order
            for source, right in order
            if middle == source and (left, right) not in order
        }
        changed = bool(additions)
        order.update(additions)
    selected = {pair for chain in chains for pair in chain}

    actions = [
        {"kind": "add_vertex", "name": vertex}
        for vertex in ("a", "b", "c")
    ]
    actions.extend(
        {
            "kind": "add_arrow",
            "name": name,
            "source": source,
            "target": target,
            "grading": None,
        }
        for name, (source, target) in endpoints.items()
    )

    def extend(prefix: tuple[str, ...]):
        if len(prefix) >= 2:
            yield prefix
        previous = "".join(prefix[-2:]) if len(prefix) >= 2 else None
        for name, (source, _target) in endpoints.items():
            if not prefix or source != endpoints[prefix[-1]][1]:
                continue
            following = prefix[-1] + name
            if len(prefix) == 1:
                allowed = following in selected
            else:
                allowed = following in selected and (previous, following) in order
            if allowed:
                yield from extend((*prefix, name))

    words = sorted(
        {word for name in endpoints for word in extend((name,))},
        key=lambda word: (len(word), word),
    )
    for word in words:
        if len(word) == 2:
            expression = {
                "type": "product",
                "coefficient": "1",
                "factors": [
                    {"type": "arrow", "name": name} for name in word
                ],
            }
        else:
            expression = {
                "type": "massey",
                "inputs": [
                    {"type": "arrow", "name": name} for name in word
                ],
            }
        actions.append({"kind": "attach_mp_cell", "expression": expression})

    result = analyze_monomial_actions(actions)
    invariants = compute_victory_invariants(actions)

    assert len(words) == 92
    assert result["kind"] == "pair_poset"
    assert result["proper"] is True
    assert result["cohomologyDimension"] == 23
    assert result["maxSupportedLength"] == 6
    assert result["supportWordCount"] == 20
    assert result["higherMasseyClassPreview"] == [
        "123",
        "156",
        "234",
        "315",
        "345",
        "456",
    ]
    assert invariants["dimension"] == 23
    assert len(invariants["basis"]) == 23
    assert invariants["ordinaryCartan"]["determinant"] == 39
    assert invariants["cellularCartan"]["determinant"] == 1
