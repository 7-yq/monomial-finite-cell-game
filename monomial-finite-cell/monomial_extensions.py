"""Formula-free A-infinity relations for the monomial game."""

from __future__ import annotations

from typing import Any

import cyclic_extensions as cyclic


def _factor_keys(quiver: Any, factors: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(repr(quiver.mp_factor_key(factor)) for factor in factors)


def _all_proper_intervals_resolved(quiver: Any, word: tuple[Any, ...]) -> bool:
    """Check the lower terms that must vanish in the sliding identity."""

    arity = len(word) - 1

    for length in range(2, arity):
        for start in range(0, len(word) - length + 1):
            block = word[start:start + length]

            try:
                resolved = quiver.mp_block_has_primitive(
                    block,
                    allow_bridge_replacements=False,
                )
            except TypeError:
                resolved = quiver.mp_block_has_primitive(block)

            if not resolved:
                return False

    return True


def compatible_ainf_replacement_relations(self) -> list[dict[str, Any]]:
    """Return Stasheff slides implied by the chosen compatible Massey system.

    If ``M(a_0,...,a_{n-1})`` and ``M(a_1,...,a_n)`` are known and every
    shorter interval in the common word is resolved, the Stasheff identity has
    only its two endpoint terms left.  It therefore supplies the formula-free
    replacement

        M(a_0,...,a_{n-1}) a_n  ~  a_0 M(a_1,...,a_n).

    No primitive or cochain representative is expanded here.
    """

    if not getattr(self, "compatible_massey_system", False):
        return []

    try:
        if cyclic._ainf_outer_arity_limit(self) == 0:
            return []
    except Exception:
        pass

    known = []
    seen_products = set()

    for item in cyclic._stasheff_known_massey_index(self).values():
        inputs = tuple(self.normalize_mp_inputs(tuple(item.inputs)))

        if len(inputs) < 3:
            continue

        key = (len(inputs), _factor_keys(self, inputs))

        if key in seen_products:
            continue

        seen_products.add(key)
        known.append((item, inputs))

    relations = []
    seen_relations = set()

    for left_massey, left_inputs in known:
        for right_massey, right_inputs in known:
            if len(left_inputs) != len(right_inputs):
                continue

            arity = len(left_inputs)

            if _factor_keys(self, left_inputs[1:]) != _factor_keys(
                self,
                right_inputs[:-1],
            ):
                continue

            word = left_inputs + (right_inputs[-1],)

            if not _all_proper_intervals_resolved(self, word):
                continue

            left = tuple(self.canonical_mp_factors((left_massey, word[-1])))
            right = tuple(self.canonical_mp_factors((word[0], right_massey)))

            if not (
                self.mp_factors_composable(left, cyclic=False)
                and self.mp_factors_composable(right, cyclic=False)
            ):
                continue

            left_key = self.mp_factor_tuple_key(left)
            right_key = self.mp_factor_tuple_key(right)
            relation_key = tuple(sorted((repr(left_key), repr(right_key))))

            if left_key == right_key or relation_key in seen_relations:
                continue

            seen_relations.add(relation_key)
            left_coeff = cyclic._stasheff_insertion_coefficient(
                self,
                word,
                0,
                arity,
            )
            right_coeff = cyclic._stasheff_insertion_coefficient(
                self,
                word,
                1,
                arity + 1,
            )
            relations.append({
                "replacement_type": "ainf",
                "ainf_kind": "compatible_massey_slide",
                "formula_free": True,
                "compatible_system": True,
                "left": left,
                "right": right,
                "left_key": left_key,
                "right_key": right_key,
                "left_coeff": left_coeff,
                "right_coeff": right_coeff,
                "relation_replacement_coeff": (
                    cyclic._stasheff_relation_replacement_coeff(
                        self,
                        left_coeff,
                        right_coeff,
                    )
                ),
                "ainf_inputs": word,
                "ainf_outer_arity": 2,
            })

    return relations


def _merge_formula_free_relations(self, relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = list(relations)
    seen = {
        tuple(sorted((repr(relation.get("left_key")), repr(relation.get("right_key")))))
        for relation in merged
        if relation.get("left_key") is not None and relation.get("right_key") is not None
    }

    for relation in compatible_ainf_replacement_relations(self):
        key = tuple(sorted((repr(relation["left_key"]), repr(relation["right_key"]))))

        if key in seen:
            continue

        seen.add(key)
        merged.append(relation)

    return merged


def product_replacement_relations(
    self,
    include_bridge: bool = True,
    include_ainf: bool = True,
):
    relations = self._monomial_base_product_replacement_relations(
        include_bridge=False,
        include_ainf=include_ainf,
    )

    if not include_ainf:
        return relations

    return _merge_formula_free_relations(self, relations)


def mp_presentation_replacement_relations(
    self,
    include_bridge: bool = True,
    include_ainf: bool = True,
    include_self_expanding: bool = True,
):
    relations = self._monomial_base_mp_presentation_replacement_relations(
        include_bridge=False,
        include_ainf=include_ainf,
        include_self_expanding=include_self_expanding,
    )

    if not include_ainf:
        return relations

    return _merge_formula_free_relations(self, relations)


def install_monomial_extensions(quiver_class: type) -> None:
    if not hasattr(quiver_class, "_monomial_base_product_replacement_relations"):
        quiver_class._monomial_base_product_replacement_relations = (
            quiver_class.product_replacement_relations
        )

    if not hasattr(
        quiver_class,
        "_monomial_base_mp_presentation_replacement_relations",
    ):
        quiver_class._monomial_base_mp_presentation_replacement_relations = (
            quiver_class.mp_presentation_replacement_relations
        )

    quiver_class.compatible_ainf_replacement_relations = (
        compatible_ainf_replacement_relations
    )
    quiver_class.product_replacement_relations = product_replacement_relations
    quiver_class.mp_presentation_replacement_relations = (
        mp_presentation_replacement_relations
    )
