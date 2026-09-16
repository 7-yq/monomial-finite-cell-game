"""
Cyclic-class helpers for the A_inf notebook.

The notebook owns the algebra classes, so install_cyclic_extensions receives
the notebook globals and patches methods onto Quiver.
"""


def install_cyclic_extensions(Quiver, namespace):
    needed = [
        "MasseyProduct",
        "MPProduct",
        "MPElement",
        "Arrow",
        "Path",
        "Element",
        "Sign",
        "to_element",
        "is_zero_coeff",
        "simplify_coeff",
    ]

    for name in needed:
        globals()[name] = namespace[name]

    if (
        hasattr(Quiver, "classify_massey_product_primitives")
        and not hasattr(Quiver, "_cyclic_base_classify_massey_product_primitives")
    ):
        Quiver._cyclic_base_classify_massey_product_primitives = (
            Quiver.classify_massey_product_primitives
        )

    if (
        hasattr(Quiver, "generate_massey_products")
        and not hasattr(Quiver, "_cyclic_base_generate_massey_products")
    ):
        Quiver._cyclic_base_generate_massey_products = (
            Quiver.generate_massey_products
        )

    if (
        hasattr(Quiver, "can_define_mp")
        and not hasattr(Quiver, "_cyclic_base_can_define_mp")
    ):
        Quiver._cyclic_base_can_define_mp = Quiver.can_define_mp

    if hasattr(Quiver, "mp") and not hasattr(Quiver, "_cyclic_base_mp"):
        Quiver._cyclic_base_mp = Quiver.mp

    if (
        hasattr(Quiver, "missing_requirements_for_mp")
        and not hasattr(Quiver, "_cyclic_base_missing_requirements_for_mp")
    ):
        Quiver._cyclic_base_missing_requirements_for_mp = (
            Quiver.missing_requirements_for_mp
        )

    if (
        hasattr(Quiver, "expand_mp")
        and not hasattr(Quiver, "_cyclic_base_expand_mp")
    ):
        Quiver._cyclic_base_expand_mp = Quiver.expand_mp

    if (
        hasattr(Quiver, "bridge_interval_representative_data")
        and not hasattr(Quiver, "_cyclic_base_bridge_interval_representative_data")
    ):
        Quiver._cyclic_base_bridge_interval_representative_data = (
            Quiver.bridge_interval_representative_data
        )

    if (
        hasattr(Quiver, "attach_bridge")
        and not hasattr(Quiver, "_cyclic_base_attach_bridge")
    ):
        Quiver._cyclic_base_attach_bridge = Quiver.attach_bridge

    if (
        hasattr(Quiver, "attach_one_cell")
        and not hasattr(Quiver, "_cyclic_base_attach_one_cell")
    ):
        Quiver._cyclic_base_attach_one_cell = Quiver.attach_one_cell

    if (
        hasattr(Quiver, "attach_mp_cell")
        and not hasattr(Quiver, "_cyclic_base_attach_mp_cell")
    ):
        Quiver._cyclic_base_attach_mp_cell = Quiver.attach_mp_cell

    if (
        hasattr(Quiver, "d_arrow")
        and not hasattr(Quiver, "_cyclic_base_d_arrow")
    ):
        Quiver._cyclic_base_d_arrow = Quiver.d_arrow

    if (
        hasattr(Quiver, "direct_mp_block_primitive")
        and not hasattr(Quiver, "_cyclic_base_direct_mp_block_primitive")
    ):
        Quiver._cyclic_base_direct_mp_block_primitive = (
            Quiver.direct_mp_block_primitive
        )

    if (
        hasattr(Quiver, "generation_item_key")
        and not hasattr(Quiver, "_cyclic_base_generation_item_key")
    ):
        Quiver._cyclic_base_generation_item_key = Quiver.generation_item_key

    if (
        hasattr(Quiver, "bridge_replacement_primitive_candidates")
        and not hasattr(Quiver, "_cyclic_base_bridge_replacement_primitive_candidates")
    ):
        Quiver._cyclic_base_bridge_replacement_primitive_candidates = (
            Quiver.bridge_replacement_primitive_candidates
        )

    if (
        hasattr(Quiver, "find_primitives_mp_product")
        and not hasattr(Quiver, "_cyclic_base_find_primitives_mp_product")
    ):
        Quiver._cyclic_base_find_primitives_mp_product = (
            Quiver.find_primitives_mp_product
        )

    if (
        hasattr(Quiver, "primitive_candidate_to_element")
        and not hasattr(Quiver, "_cyclic_base_primitive_candidate_to_element")
    ):
        Quiver._cyclic_base_primitive_candidate_to_element = (
            Quiver.primitive_candidate_to_element
        )

    if (
        hasattr(Quiver, "replacement_edge_records")
        and not hasattr(Quiver, "_cyclic_base_replacement_edge_records")
    ):
        Quiver._cyclic_base_replacement_edge_records = (
            Quiver.replacement_edge_records
        )

    methods = {
        "cyclic_factor_key": cyclic_factor_key,
        "cyclic_factor_tuple_key": cyclic_factor_tuple_key,
        "cyclic_rotations": cyclic_rotations,
        "canonical_cyclic_factor_tuple": canonical_cyclic_factor_tuple,
        "canonical_cyclic_factor_key": canonical_cyclic_factor_key,
        "mp_factors_composable": mp_factors_composable,
        "cyclic_factor_alphabet": cyclic_factor_alphabet,
        "exact_product_block_resolution": exact_product_block_resolution,
        "product_word_resolution_candidates": product_word_resolution_candidates,
        "replacement_relation_cycle_class_reports": replacement_relation_cycle_class_reports,
        "generated_product_cycle_class_reports": generated_product_cycle_class_reports,
        "cyclic_product_class_report": cyclic_product_class_report,
        "known_resolved_product_blocks": known_resolved_product_blocks,
        "product_word_contains_forbidden_block": product_word_contains_forbidden_block,
        "bridge_product_relations": bridge_product_relations,
        "replacement_edge_records": replacement_edge_records,
        "product_replacement_relations": product_replacement_relations,
        "mp_presentation_replacement_relations": mp_presentation_replacement_relations,
        "linear_replacement_neighbors": linear_replacement_neighbors,
        "linear_replacement_component": linear_replacement_component,
        "mp_presentation_equivalent_primitive_report": mp_presentation_equivalent_primitive_report,
        "cyclic_rotation_preserves_block": cyclic_rotation_preserves_block,
        "bridge_cyclic_neighbor_records": bridge_cyclic_neighbor_records,
        "bridge_cyclic_neighbors": bridge_cyclic_neighbors,
        "bridge_cyclic_component_paths": bridge_cyclic_component_paths,
        "bridge_cyclic_component": bridge_cyclic_component,
        "product_cyclic_class_is_bridge_resolved": product_cyclic_class_is_bridge_resolved,
        "redundant_generator_report": redundant_generator_report,
        "product_cyclic_class_over_resolution_report": product_cyclic_class_over_resolution_report,
        "product_cyclic_automaton": product_cyclic_automaton,
        "product_quotient_suffix_component": product_quotient_suffix_component,
        "product_quotient_automaton": product_quotient_automaton,
        "shortest_product_automaton_cycle": shortest_product_automaton_cycle,
        "product_automaton_max_word_length": product_automaton_max_word_length,
        "next_product_cyclic_class": next_product_cyclic_class,
        "product_cyclic_frontier_report": product_cyclic_frontier_report,
        "unresolved_product_cyclic_classes_at_length": unresolved_product_cyclic_classes_at_length,
        "pure_massey_input_alphabet": pure_massey_input_alphabet,
        "canonical_pure_massey_input_tuple": canonical_pure_massey_input_tuple,
        "canonical_pure_massey_input_key": canonical_pure_massey_input_key,
        "generated_pure_massey_cyclic_class_reports": generated_pure_massey_cyclic_class_reports,
        "next_pure_massey_cyclic_class": next_pure_massey_cyclic_class,
        "cyclic_search_stage_report": cyclic_search_stage_report,
        "cyclic_autocomplete_plan": cyclic_autocomplete_plan,
        "apply_cyclic_autocomplete": apply_cyclic_autocomplete,
        "undo_cyclic_autocomplete": undo_cyclic_autocomplete,
        "massey_orbit_tower_plan": massey_orbit_tower_plan,
        "apply_massey_orbit_tower": apply_massey_orbit_tower,
        "undo_massey_orbit_tower": undo_massey_orbit_tower,
        "cyclic_massey_rotation_report": cyclic_massey_rotation_report,
        "pure_massey_cyclic_class_report": pure_massey_cyclic_class_report,
        "completed_massey_tower_elimination_records": completed_massey_tower_elimination_records,
        "completed_massey_pair_tower_elimination_records": completed_massey_pair_tower_elimination_records,
        "record_completed_massey_towers": record_completed_massey_towers,
        "is_tower_eliminated_mp": is_tower_eliminated_mp,
        "tower_elimination_report": tower_elimination_report,
        "pair_tower_elimination_report": pair_tower_elimination_report,
        "is_pair_tower_eliminated_mp": is_pair_tower_eliminated_mp,
        "mp_block_has_primitive": mp_block_has_primitive,
        "absorbing_higher_product": absorbing_higher_product,
        "generalized_higher_product_definition_report": generalized_higher_product_definition_report,
        "can_define_mp": can_define_mp,
        "mp": mp,
        "missing_requirements_for_mp": missing_requirements_for_mp,
        "virtual_mp": virtual_mp,
        "try_generate_mp": try_generate_mp,
        "generation_item_key": generation_item_key,
        "generated_massey_inputs_have_zero_product_input": generated_massey_inputs_have_zero_product_input,
        "generated_massey_inputs_are_product_multiple": generated_massey_inputs_are_product_multiple,
        "fast_generate_massey_products": fast_generate_massey_products,
        "generate_massey_products": generate_massey_products,
        "classify_massey_product_primitives": classify_massey_product_primitives,
        "classify_massey_product_primitive_summary": classify_massey_product_primitive_summary,
        "bridge_interval_representative_data": bridge_interval_representative_data,
        "bridge_replacement_primitive_candidates": bridge_replacement_primitive_candidates,
        "find_primitives_mp_product": find_primitives_mp_product,
        "primitive_candidate_to_element": primitive_candidate_to_element,
        "direct_mp_block_primitive": direct_mp_block_primitive,
        "expand_mp": expand_mp,
        "attach_one_cell": attach_one_cell,
        "attach_mp_cell": attach_mp_cell,
        "attach_bridge": attach_bridge,
        "attach_bridge_cell": attach_bridge_cell,
        "d_arrow": d_arrow,
    }

    for name, fn in methods.items():
        setattr(Quiver, name, fn)

    return Quiver


def d_arrow(self, a):
    expression = getattr(a, "deferred_differential_expression", None)

    if expression is not None and getattr(self, "differential", {}).get(a, None) is None:
        if (
            getattr(self, "_suppress_primitive_expansion", False)
            or _massey_formula_disabled(self)
        ):
            return self.zero()

        try:
            differential = self.expand_mp_expression(expression)
        except Exception:
            differential = None

        if differential is None:
            return self.zero()

        self.differential[a] = differential
        return differential

    base = getattr(type(self), "_cyclic_base_d_arrow", None)

    if base is not None:
        result = base(self, a)
        return self.zero() if result is None else result

    result = getattr(self, "differential", {}).get(a, None)
    return self.zero() if result is None else result


def _massey_formula_disabled(self):
    return bool(
        getattr(self, "_disable_massey_formula", False)
        or getattr(self, "disable_massey_formula", False)
    )


AbsorbingHigherProduct = None


def _ensure_absorbing_higher_product_class():
    global AbsorbingHigherProduct

    base = globals().get("MasseyProduct")

    if base is None:
        return None

    try:
        if AbsorbingHigherProduct is not None and issubclass(
            AbsorbingHigherProduct,
            base,
        ):
            return AbsorbingHigherProduct
    except TypeError:
        pass

    class _AbsorbingHigherProduct(base):
        def __init__(self, quiver, inputs, resolution_data=None):
            super().__init__(quiver, inputs)
            self.absorbing_higher_product = True
            self.cell_kind = "absorbing_higher_product"
            self.resolution_data = dict(resolution_data or {})

        def __repr__(self):
            inside = " ".join(str(item) for item in self.inputs)
            return f"<{inside}>"

        def key(self):
            pieces = []

            for item in self.inputs:
                try:
                    pieces.append(self.Q.mp_factor_key(item))
                except Exception:
                    if hasattr(item, "key"):
                        pieces.append(item.key())
                    else:
                        pieces.append(str(item))

            return ("AbsorbingHigherProduct", tuple(pieces))

    _AbsorbingHigherProduct.__name__ = "AbsorbingHigherProduct"
    AbsorbingHigherProduct = _AbsorbingHigherProduct
    return AbsorbingHigherProduct


def _is_absorbing_higher_product(item):
    if bool(getattr(item, "absorbing_higher_product", False)):
        return True

    cls = globals().get("AbsorbingHigherProduct")

    try:
        return cls is not None and isinstance(item, cls)
    except TypeError:
        return False


def _absorbing_input_from_factor(self, factor):
    factor = self.normalize_mp_input(factor)

    if isinstance(factor, MasseyProduct) and len(tuple(factor.inputs)) == 1:
        return self.normalize_mp_input(factor.inputs[0])

    return factor


def _absorbing_higher_product_key(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    return (
        "absorbing_higher_product",
        tuple(self.mp_factor_key(item) for item in inputs),
    )


def absorbing_higher_product(self, *inputs, record=True, resolution_data=None):
    cls = _ensure_absorbing_higher_product_class()

    if cls is None:
        return None

    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return None

    if not _fast_key_is_composable(self, inputs):
        return None

    try:
        key = _absorbing_higher_product_key(self, inputs)
    except Exception:
        key = ("absorbing_higher_product", tuple(repr(item) for item in inputs))

    registry = getattr(self, "absorbing_higher_products", None)

    if not isinstance(registry, dict):
        registry = {}
        self.absorbing_higher_products = registry

    existing = registry.get(key)

    if existing is not None:
        if resolution_data:
            existing.resolution_data.update(dict(resolution_data))

        return existing

    product = cls(self, inputs, resolution_data=resolution_data)

    if record:
        registry[key] = product

    return product


def _absorbing_cell_resolved_binary_product_blocks(self):
    blocks = []
    seen = set()

    def remember(raw_block, source, primitive=None):
        try:
            block = self.canonical_mp_factors(tuple(raw_block))
        except Exception:
            return

        if len(block) != 2:
            return

        try:
            if not self.mp_factors_composable(block, cyclic=False):
                return
        except Exception:
            return

        try:
            key = self.cyclic_factor_tuple_key(block)
        except Exception:
            key = tuple(repr(item) for item in block)

        key_token = repr(key)

        if key_token in seen:
            return

        seen.add(key_token)
        blocks.append({
            "factors": block,
            "source": source,
            "primitive": primitive,
        })

    for key, primitive in tuple(
        (getattr(self, "resolved_massey_products", {}) or {}).items()
    ):
        if _is_absorbing_higher_product(primitive):
            continue

        if _is_virtual_massey_primitive(primitive):
            continue

        if len(tuple(key)) == 2:
            remember(tuple(key), "resolved_massey_product", primitive=primitive)

    for entry in tuple(getattr(self, "attachment_history", ()) or ()):
        expression = entry.get("expression", None)

        if isinstance(expression, MPProduct):
            remember(
                expression.factors,
                entry.get("kind", "mp_product_cell"),
                primitive=entry.get("cell", None),
            )

        elif isinstance(expression, MPElement) and len(expression.terms) == 1:
            product, coeff = next(iter(expression.terms.items()))

            if not is_zero_coeff(coeff) and isinstance(product, MPProduct):
                remember(
                    product.factors,
                    entry.get("kind", "mp_expression_cell"),
                    primitive=entry.get("cell", None),
                )

        elif isinstance(expression, MasseyProduct):
            remember(
                tuple(expression.inputs),
                entry.get("kind", "mp_cell"),
                primitive=entry.get("cell", None),
            )

        elif isinstance(expression, (Arrow, Path, Element)):
            try:
                product = self.path_to_mp_product(expression)
            except Exception:
                product = None

            if isinstance(product, MPProduct):
                remember(
                    product.factors,
                    entry.get("kind", "ordinary_cell"),
                    primitive=entry.get("cell", None),
                )

    for path_key, cell in tuple((getattr(self, "cells", {}) or {}).items()):
        if len(tuple(path_key)) != 2:
            continue

        try:
            remember(
                tuple(self.mp(self.arrows[name]) for name in tuple(path_key)),
                "ordinary_cell",
                primitive=cell,
            )
        except Exception:
            continue

    return tuple(blocks)


def _absorbing_bridge_replacement_pairs(self):
    pairs = []
    seen = set()

    try:
        relations = tuple(self.bridge_product_relations() or ())
    except Exception:
        return pairs

    for relation in relations:
        raw_sides = (
            (relation.get("left", ()), relation.get("right", ())),
            (relation.get("right", ()), relation.get("left", ())),
        )

        for source, target in raw_sides:
            try:
                source = self.canonical_mp_factors(tuple(source))
                target = self.canonical_mp_factors(tuple(target))
            except Exception:
                continue

            if len(source) != 1 or len(target) != 1:
                continue

            replacement = target[0]

            if not isinstance(replacement, MasseyProduct):
                continue

            replacement_inputs = tuple(
                self.normalize_mp_inputs(tuple(replacement.inputs))
            )

            if len(replacement_inputs) < 2:
                continue

            try:
                pair_key = (
                    repr(self.cyclic_factor_tuple_key(source)),
                    repr(self.cyclic_factor_tuple_key(target)),
                )
            except Exception:
                pair_key = (repr(source), repr(target))

            if pair_key in seen:
                continue

            seen.add(pair_key)
            pairs.append({
                "base": source[0],
                "replacement": replacement,
                "replacement_inputs": replacement_inputs,
                "relation": relation,
            })

    return tuple(pairs)


def _absorbing_can_define_inner_side(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 2:
        return False

    try:
        return bool(self.can_define_mp(*inputs))
    except Exception:
        return False


def _absorbing_mp_factor_if_directly_defined(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 1:
        return None

    if len(inputs) == 1:
        try:
            return self.mp(inputs[0])
        except Exception:
            return None

    try:
        if not self.can_define_mp_direct(*inputs):
            return None
    except Exception:
        return None

    try:
        existing = getattr(self, "massey_products", {}).get(tuple(inputs), None)

        if isinstance(existing, MasseyProduct):
            return existing

        return MasseyProduct(self, inputs)
    except Exception:
        return None


def _absorbing_product_has_direct_primitive(self, factors):
    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return False

    if len(factors) != 2:
        return False

    try:
        if not self.mp_factors_composable(factors, cyclic=False):
            return False
    except Exception:
        return False

    try:
        block_key = self.mp_product_block_key(factors)
        primitive = self.direct_mp_block_primitive(*block_key)
    except Exception:
        primitive = None

    return primitive is not None and not _is_absorbing_higher_product(primitive)


def _absorbing_record_resolution(
    self,
    block_map,
    resolved_keys,
    target_block,
    absorbing_inputs,
    absorbed_block,
    bridge_pair,
    cell_block,
    direction,
):
    try:
        target_block = self.canonical_mp_factors(tuple(target_block))
        absorbed_block = self.canonical_mp_factors(tuple(absorbed_block))
    except Exception:
        return None

    if len(target_block) != 2 or len(absorbed_block) != 2:
        return None

    try:
        if not self.mp_factors_composable(target_block, cyclic=False):
            return None
    except Exception:
        return None

    try:
        block_key = self.mp_product_block_key(target_block)
    except Exception:
        return None

    existing = getattr(self, "resolved_massey_products", {}).get(block_key)

    if existing is not None and not _is_absorbing_higher_product(existing):
        return None

    try:
        target_key = self.cyclic_factor_tuple_key(target_block)
        absorbed_key = self.cyclic_factor_tuple_key(absorbed_block)
    except Exception:
        return None

    resolution_group_key = ("primitive_block", absorbed_key)
    data = {
        "source": "absorbing_higher_product",
        "direction": direction,
        "target_product_factors": target_block,
        "absorbed_product_factors": absorbed_block,
        "absorbed_product_source": cell_block.get("source"),
        "bridge_relation": bridge_pair.get("relation"),
        "bridge_base_factor": bridge_pair.get("base"),
        "bridge_replacement_factor": bridge_pair.get("replacement"),
        "resolution_group_key": resolution_group_key,
    }
    primitive = absorbing_higher_product(
        self,
        *absorbing_inputs,
        record=True,
        resolution_data=data,
    )

    if primitive is None:
        return None

    data["primitive"] = primitive
    block_map[repr(target_key)] = data

    if not hasattr(self, "resolved_massey_products"):
        self.resolved_massey_products = {}

    self.resolved_massey_products[block_key] = primitive
    resolved_keys.add(block_key)
    return data


def _absorbing_state_signature(self):
    resolved_keys = []

    for key, primitive in tuple(
        (getattr(self, "resolved_massey_products", {}) or {}).items()
    ):
        if _is_absorbing_higher_product(primitive):
            continue

        resolved_keys.append(repr(key))

    return (
        len(tuple(getattr(self, "attachment_history", ()) or ())),
        len(getattr(self, "resolved_mp_expressions", {}) or {}),
        len(getattr(self, "cells", {}) or {}),
        len(tuple(getattr(self, "bridge_history", ()) or ())),
        tuple(sorted(resolved_keys)),
    )


def _ensure_absorbing_higher_products(self):
    if getattr(self, "_building_absorbing_higher_products", False):
        return getattr(self, "absorbing_higher_product_resolutions", {})

    signature = _absorbing_state_signature(self)

    if getattr(self, "_absorbing_higher_product_signature", None) == signature:
        return getattr(self, "absorbing_higher_product_resolutions", {})

    self._building_absorbing_higher_products = True

    try:
        old_keys = set(getattr(self, "_absorbing_higher_product_resolved_keys", set()))

        for key in old_keys:
            primitive = getattr(self, "resolved_massey_products", {}).get(key)

            if _is_absorbing_higher_product(primitive):
                try:
                    del self.resolved_massey_products[key]
                except Exception:
                    pass

        self.absorbing_higher_products = {}
        block_map = {}
        resolved_keys = set()
        cell_blocks = _absorbing_cell_resolved_binary_product_blocks(self)
        bridge_pairs = _absorbing_bridge_replacement_pairs(self)

        for cell_block in cell_blocks:
            block = tuple(cell_block.get("factors", ()))

            if len(block) != 2:
                continue

            for bridge_pair in bridge_pairs:
                base = bridge_pair["base"]
                replacement = bridge_pair["replacement"]
                replacement_inputs = tuple(bridge_pair["replacement_inputs"])

                if self.mp_factors_equal((block[1],), (base,)):
                    absorbing_inputs = (
                        (_absorbing_input_from_factor(self, block[0]),)
                        + replacement_inputs
                    )
                    prefix = _absorbing_mp_factor_if_directly_defined(
                        self,
                        absorbing_inputs[:-1],
                    )
                    last = _absorbing_mp_factor_if_directly_defined(
                        self,
                        absorbing_inputs[-1:],
                    )

                    if prefix is None or last is None:
                        continue

                    if not _absorbing_product_has_direct_primitive(
                        self,
                        (prefix, last),
                    ):
                        continue

                    _absorbing_record_resolution(
                        self,
                        block_map,
                        resolved_keys,
                        (block[0], replacement),
                        absorbing_inputs,
                        block,
                        bridge_pair,
                        cell_block,
                        "right_bridge_replacement",
                    )

                if self.mp_factors_equal((block[0],), (base,)):
                    absorbing_inputs = (
                        replacement_inputs
                        + (_absorbing_input_from_factor(self, block[1]),)
                    )
                    first = _absorbing_mp_factor_if_directly_defined(
                        self,
                        absorbing_inputs[:1],
                    )
                    suffix = _absorbing_mp_factor_if_directly_defined(
                        self,
                        absorbing_inputs[1:],
                    )

                    if first is None or suffix is None:
                        continue

                    if not _absorbing_product_has_direct_primitive(
                        self,
                        (first, suffix),
                    ):
                        continue

                    _absorbing_record_resolution(
                        self,
                        block_map,
                        resolved_keys,
                        (replacement, block[1]),
                        absorbing_inputs,
                        block,
                        bridge_pair,
                        cell_block,
                        "left_bridge_replacement",
                    )

        self.absorbing_higher_product_resolutions = block_map
        self._absorbing_higher_product_resolved_keys = resolved_keys
        self._absorbing_higher_product_signature = signature
        return block_map
    finally:
        self._building_absorbing_higher_products = False


def _absorbing_higher_product_resolution_for_block(self, factors):
    try:
        factors = self.canonical_mp_factors(tuple(factors))
        key = repr(self.cyclic_factor_tuple_key(factors))
    except Exception:
        return None

    resolutions = _ensure_absorbing_higher_products(self)
    return resolutions.get(key)


def _is_higher_massey_factor(factor):
    return isinstance(factor, MasseyProduct) and len(tuple(factor.inputs)) >= 3


def _mp_inputs_require_higher_massey_formula(inputs):
    inputs = tuple(inputs or ())

    if len(inputs) >= 3:
        return True

    return any(_is_higher_massey_factor(item) for item in inputs)


def expand_mp(self, *inputs):
    normalized = tuple(self.normalize_mp_input(x) for x in tuple(inputs))

    if (
        _massey_formula_disabled(self)
        and _mp_inputs_require_higher_massey_formula(normalized)
    ):
        raise RuntimeError(
            "Massey product formula is disabled for this computation."
        )

    base = getattr(type(self), "_cyclic_base_expand_mp", None)

    if base is None:
        return None

    return base(self, *inputs)


def _eval_bridge_expression_arg(self, value, label):
    if not isinstance(value, str):
        return value

    try:
        return eval(value, self.mp_eval_environment())
    except Exception as exc:
        print(f"Could not understand the {label} MP expression.")
        print("Python error:", exc)
        return None


def _bridge_mp_difference(self, g1, g2=None):
    g1 = _eval_bridge_expression_arg(self, g1, "first")

    if g1 is None:
        return None

    has_second_arg = g2 is not None
    g2 = _eval_bridge_expression_arg(self, g2, "second")

    if has_second_arg and g2 is None:
        return None

    try:
        if g2 is None:
            return self.to_mp_element(g1)

        return self.to_mp_element(g1) - self.to_mp_element(g2)
    except Exception as exc:
        print("Could not form the MP difference.")
        print("Python error:", exc)
        return None


def _factor_is_virtual_massey(self, factor):
    if not isinstance(factor, MasseyProduct) or len(tuple(factor.inputs)) < 3:
        return False

    inputs = tuple(self.normalize_mp_inputs(tuple(factor.inputs)))

    try:
        key = self.mp_key(*inputs)
        primitive = getattr(self, "resolved_massey_products", {}).get(key, None)

        if _is_virtual_massey_primitive(primitive):
            return True
    except Exception:
        pass

    try:
        if not self.can_define_mp(*inputs):
            return False
    except Exception:
        return False

    try:
        return not self.can_define_mp_direct(*inputs)
    except Exception:
        return True


def _bridge_expression_has_virtual_massey_factor(self, expression):
    if isinstance(expression, MasseyProduct):
        return _factor_is_virtual_massey(self, expression)

    if isinstance(expression, MPProduct):
        products = (expression,)
    elif isinstance(expression, MPElement):
        products = tuple(expression.terms.keys())
    else:
        return False

    for product in products:
        for factor in tuple(getattr(product, "factors", ())):
            if _factor_is_virtual_massey(self, factor):
                return True

    return False


def _single_mp_product_from_value(self, value):
    if isinstance(value, MasseyProduct):
        return value.as_product()

    if isinstance(value, MPProduct):
        return value

    if not isinstance(value, MPElement):
        return None

    nonzero_terms = [
        (product, coeff)
        for product, coeff in value.terms.items()
        if not is_zero_coeff(coeff)
    ]

    if len(nonzero_terms) != 1:
        return None

    return nonzero_terms[0][0]


def _is_ordinary_generator_arrow(self, arrow):
    return (
        isinstance(arrow, Arrow)
        and getattr(arrow, "Q", self) is self
        and getattr(self, "arrows", {}).get(getattr(arrow, "name", None)) is arrow
        and not hasattr(arrow, "cell_prefix")
        and not hasattr(arrow, "index")
        and not getattr(arrow, "virtual_primitive_cell", False)
    )


def _single_generator_arrow_from_bridge_side(self, value):
    product = _single_mp_product_from_value(self, value)

    if product is None or len(tuple(product.factors)) != 1:
        return None

    factor = tuple(product.factors)[0]

    if not isinstance(factor, MasseyProduct):
        return None

    inputs = tuple(self.normalize_mp_inputs(tuple(factor.inputs)))

    if len(inputs) != 1:
        return None

    arrow = inputs[0]

    if not _is_ordinary_generator_arrow(self, arrow):
        return None

    return arrow


def _primitive_resolution_uses_primitive(resolution, primitive):
    if primitive is None or not isinstance(resolution, dict):
        return False

    return (
        resolution.get("raw_primitive", None) is primitive
        or resolution.get("primitive", None) is primitive
    )


def _concrete_primitive_resolution_for_product(
    self,
    product,
    excluded_primitives=(),
):
    product = _single_mp_product_from_value(self, product)

    if product is None:
        return None

    try:
        factors = tuple(self.canonical_mp_factors(tuple(product.factors)))
    except Exception:
        factors = tuple(getattr(product, "factors", ()) or ())

    if not factors:
        return None

    try:
        resolution = self.exact_product_block_resolution(
            factors,
            verify=False,
        )
    except Exception:
        return None

    if not isinstance(resolution, dict) or not resolution.get("resolved"):
        return None

    primitive = resolution.get("raw_primitive", None)

    if primitive is None:
        primitive = resolution.get("primitive", None)

    if primitive is None:
        return None

    for excluded in tuple(excluded_primitives or ()):
        if _primitive_resolution_uses_primitive(resolution, excluded):
            return None

    return resolution


def _mp_expression_uses_arrow_names(self, value, arrow_names, seen=None):
    if value is None:
        return False

    arrow_names = set(arrow_names)

    if not arrow_names:
        return False

    if seen is None:
        seen = set()

    marker = id(value)

    if marker in seen:
        return False

    seen.add(marker)

    if isinstance(value, Arrow):
        return getattr(value, "name", None) in arrow_names

    if isinstance(value, Path):
        return any(name in arrow_names for name in tuple(value.arrows))

    if isinstance(value, Element):
        return any(
            _mp_expression_uses_arrow_names(self, path, arrow_names, seen)
            for path in value.terms
        )

    if isinstance(value, MasseyProduct):
        return any(
            _mp_expression_uses_arrow_names(self, item, arrow_names, seen)
            for item in tuple(value.inputs)
        )

    if isinstance(value, MPProduct):
        return any(
            _mp_expression_uses_arrow_names(self, factor, arrow_names, seen)
            for factor in tuple(value.factors)
        )

    if isinstance(value, MPElement):
        return any(
            _mp_expression_uses_arrow_names(self, product, arrow_names, seen)
            for product in value.terms
        )

    if isinstance(value, dict):
        return any(
            _mp_expression_uses_arrow_names(self, item, arrow_names, seen)
            for pair in value.items()
            for item in pair
        )

    if isinstance(value, (list, tuple, set, frozenset)):
        return any(
            _mp_expression_uses_arrow_names(self, item, arrow_names, seen)
            for item in value
        )

    return False


def _cell_definition_uses_arrow_names(self, cell, arrow_names):
    pieces = [
        getattr(cell, "index", None),
        getattr(cell, "deferred_differential_expression", None),
        getattr(cell, "virtual_massey_inputs", None),
        getattr(self, "differential", {}).get(cell, None),
    ]

    return any(
        _mp_expression_uses_arrow_names(self, piece, arrow_names)
        for piece in pieces
    )


def _primitive_uses_arrow_names(self, primitive, arrow_names):
    if _mp_expression_uses_arrow_names(self, primitive, arrow_names):
        return True

    if isinstance(primitive, Arrow):
        return _cell_definition_uses_arrow_names(self, primitive, arrow_names)

    return False


def _generator_dependency_arrow_names(self, generator):
    blocked = {generator.name}
    changed = True

    while changed:
        changed = False

        for name, arrow in tuple(getattr(self, "arrows", {}).items()):
            if name in blocked or _is_ordinary_generator_arrow(self, arrow):
                continue

            if _cell_definition_uses_arrow_names(self, arrow, blocked):
                blocked.add(name)
                changed = True

    return blocked


def _mp_input_defined_without_arrow_names(self, value, blocked_names, memo=None):
    if memo is None:
        memo = {}

    if _mp_expression_uses_arrow_names(self, value, blocked_names):
        return False

    if isinstance(value, MasseyProduct):
        inputs = tuple(self.normalize_mp_inputs(tuple(value.inputs)))
        key = ("massey", self.mp_factor_tuple_key(inputs), tuple(sorted(blocked_names)))

        if key in memo:
            return memo[key]

        memo[key] = False

        if not all(
            _mp_input_defined_without_arrow_names(self, item, blocked_names, memo)
            for item in inputs
        ):
            return False

        if len(inputs) == 0:
            return False

        if self.has_zero_mp_input(inputs):
            memo[key] = True
            return True

        if len(inputs) == 1:
            memo[key] = True
            return True

        if len(inputs) == 2:
            try:
                result = bool(self.are_composable(inputs[0], inputs[1]))
            except Exception:
                result = False

            memo[key] = result
            return result

        for subkey in self.required_lower_mps(*inputs):
            if not _mp_block_has_surviving_primitive(
                self,
                subkey,
                blocked_names,
                memo=memo,
            ):
                return False

        memo[key] = True
        return True

    if isinstance(value, MPProduct):
        return _mp_product_defined_without_arrow_names(
            self,
            value,
            blocked_names,
            memo=memo,
        )

    if isinstance(value, MPElement):
        return all(
            _mp_product_defined_without_arrow_names(
                self,
                product,
                blocked_names,
                memo=memo,
            )
            for product, coeff in value.terms.items()
            if not is_zero_coeff(coeff)
        )

    return True


def _mp_product_defined_without_arrow_names(self, product, blocked_names, memo=None):
    if not isinstance(product, MPProduct):
        return _mp_input_defined_without_arrow_names(
            self,
            product,
            blocked_names,
            memo=memo,
        )

    if _mp_expression_uses_arrow_names(self, product, blocked_names):
        return False

    factors = tuple(product.factors)

    return all(
        _mp_input_defined_without_arrow_names(
            self,
            factor,
            blocked_names,
            memo=memo,
        )
        for factor in factors
    )


def _surviving_attachment_primitive_for_product(self, product, blocked_names):
    try:
        target_key = self.mp_product_key(product)
    except Exception:
        return None

    for entry in tuple(getattr(self, "attachment_history", ())):
        expression = entry.get("expression", None)
        primitive = entry.get("cell", None)
        differential = entry.get("differential", None)
        expression_product = _single_mp_product_from_value(self, expression)

        if expression_product is None:
            continue

        try:
            if self.mp_product_key(expression_product) != target_key:
                continue
        except Exception:
            continue

        if any(
            _mp_expression_uses_arrow_names(self, piece, blocked_names)
            for piece in (expression, primitive, differential)
        ):
            continue

        return primitive

    return None


def _mp_block_has_surviving_primitive(self, inputs, blocked_names, memo=None):
    if memo is None:
        memo = {}

    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    key = ("block", self.mp_factor_tuple_key(inputs), tuple(sorted(blocked_names)))

    if key in memo:
        return memo[key]

    memo[key] = False

    if len(inputs) == 0:
        return False

    if not all(
        _mp_input_defined_without_arrow_names(self, item, blocked_names, memo)
        for item in inputs
    ):
        return False

    if self.has_zero_mp_input(inputs):
        memo[key] = True
        return True

    if len(inputs) == 1:
        memo[key] = True
        return True

    primitive = getattr(self, "resolved_massey_products", {}).get(
        self.mp_key(*inputs),
        None,
    )

    if primitive is not None and not _primitive_uses_arrow_names(
        self,
        primitive,
        blocked_names,
    ):
        memo[key] = True
        return True

    try:
        factors = tuple(self.canonical_mp_factors(inputs))
        product = MPProduct(self, factors)
    except Exception:
        factors = None
        product = None

    if product is not None:
        primitive = _surviving_attachment_primitive_for_product(
            self,
            product,
            blocked_names,
        )

        if primitive is not None:
            memo[key] = True
            return True

    if factors is not None:
        try:
            element = self.mp_factors_to_element(factors)
        except Exception:
            element = None

        if element is not None and len(element.terms) == 1:
            path, coeff = next(iter(element.terms.items()))

            if coeff == 1 and not _mp_expression_uses_arrow_names(
                self,
                path,
                blocked_names,
            ):
                primitive = getattr(self, "cells", {}).get(tuple(path.arrows), None)

                if primitive is not None and not _primitive_uses_arrow_names(
                    self,
                    primitive,
                    blocked_names,
                ):
                    memo[key] = True
                    return True

    return False


def _bridge_side_display_text(self, value):
    product = _single_mp_product_from_value(self, value)

    if product is not None:
        try:
            if len(tuple(product.factors)) == 1:
                return self.format_mp_input_product(tuple(product.factors))

            return self.format_mp_input_product(tuple(product.factors))
        except Exception:
            return str(product)

    return str(value)


def _stasheff_zero_primitive_resolution_for_product(self, product):
    product = _single_mp_product_from_value(self, product) or product

    if not isinstance(product, MPProduct):
        return None

    try:
        factors = self.canonical_mp_factors(tuple(product.factors))
    except Exception:
        return None

    if len(factors) < 2:
        return None

    try:
        candidates = _stasheff_zero_product_resolution_candidates(
            self,
            factors,
        )
    except Exception:
        candidates = ()

    for candidate in tuple(candidates or ()):
        if candidate.get("source") != "stasheff_zero":
            continue

        return {
            "resolved": True,
            "factors": factors,
            "source": "stasheff_zero",
            "virtual_primitive": True,
            "candidate": candidate,
        }

    return None


def _generator_bridge_redundancy_report(self, left, right):
    if right is None:
        return None

    for side, generator, other in (
        ("left", _single_generator_arrow_from_bridge_side(self, left), right),
        ("right", _single_generator_arrow_from_bridge_side(self, right), left),
    ):
        if generator is None:
            continue

        blocked = _generator_dependency_arrow_names(self, generator)
        other_product = _single_mp_product_from_value(self, other)

        if other_product is not None:
            primitive_resolution = _concrete_primitive_resolution_for_product(
                self,
                other_product,
            )

            if primitive_resolution is not None:
                return {
                    "reason": "generator_redundant_bridge",
                    "generator": generator,
                    "generator_name": generator.name,
                    "generator_side": side,
                    "other_side": other,
                    "other_side_text": _bridge_side_display_text(self, other),
                    "other_side_primitive_resolution": primitive_resolution,
                    "removed_arrow_names": tuple(sorted(blocked, key=str)),
                }

            primitive_resolution = _stasheff_zero_primitive_resolution_for_product(
                self,
                other_product,
            )

            if primitive_resolution is not None:
                return {
                    "reason": "generator_redundant_bridge",
                    "generator": generator,
                    "generator_name": generator.name,
                    "generator_side": side,
                    "other_side": other,
                    "other_side_text": _bridge_side_display_text(self, other),
                    "other_side_primitive_resolution": primitive_resolution,
                    "removed_arrow_names": tuple(sorted(blocked, key=str)),
                }

            defined = _mp_product_defined_without_arrow_names(
                self,
                other_product,
                blocked,
                memo={},
            )
        else:
            defined = _mp_input_defined_without_arrow_names(
                self,
                other,
                blocked,
                memo={},
            )

        if not defined:
            continue

        return {
            "reason": "generator_redundant_bridge",
            "generator": generator,
            "generator_name": generator.name,
            "generator_side": side,
            "other_side": other,
            "other_side_text": _bridge_side_display_text(self, other),
            "removed_arrow_names": tuple(sorted(blocked, key=str)),
        }

    return None


def _format_generator_bridge_redundancy_warning(self, report):
    generator_name = report.get("generator_name", "the generator")
    other_side = report.get("other_side_text", "the other side")

    if report.get("other_side_primitive_resolution") is not None:
        return (
            "Warning: not attaching this bridge because "
            f"{other_side} already has a primitive. "
            f"The bridge would make {generator_name} redundant."
        )

    removed_count = max(0, len(tuple(report.get("removed_arrow_names", ()))) - 1)
    cell_text = (
        f" and {removed_count} dependent cell(s)"
        if removed_count
        else ""
    )

    return (
        "Warning: not attaching this bridge because "
        f"{other_side} is already defined after removing generator "
        f"{generator_name}{cell_text}. "
        f"The bridge would make {generator_name} redundant."
    )


def _source_target_of_mp_element(self, expression):
    if isinstance(expression, MasseyProduct):
        return expression.source, expression.target

    if isinstance(expression, MPProduct):
        return expression.source, expression.target

    if not isinstance(expression, MPElement) or not expression.terms:
        return None, None

    sources = set()
    targets = set()

    for product in expression.terms:
        if not product.factors:
            return None, None

        sources.add(product.source)
        targets.add(product.target)

    if len(sources) != 1 or len(targets) != 1:
        return None, None

    return next(iter(sources)), next(iter(targets))


def _attach_deferred_bridge_cell(self, expression):
    if not isinstance(expression, MPElement) or len(expression.terms) < 2:
        print("The bridge cell index must be a nontrivial MPElement difference.")
        print("No bridge cell was attached.")
        return None

    source, target = _source_target_of_mp_element(self, expression)

    if source is None or target is None:
        print("Warning: the chosen bridge expression does not have a unique source and target.")
        print(f"The expression {expression} is not homogeneous as a formal MP expression.")
        print("No bridge cell was attached.")
        return None

    if expression in self.v:
        print("A cell with this differential/index has already been attached.")
        print(f"Existing cell: {self.v[expression]}")
        return self.v[expression]

    internal_name = f"cell_{len(self.arrows) + 1}"

    while internal_name in self.arrows:
        internal_name = f"cell_{len(self.arrows) + 1}"

    height = 1

    try:
        height = max(
            sum(getattr(factor, "h", lambda: 0)() for factor in product.factors)
            for product in expression.terms
        ) + 1
    except Exception:
        height = 1

    new_cell = Arrow(
        self,
        internal_name,
        source,
        target,
        grading=None,
        height=height,
    )
    new_cell.index = expression
    new_cell.cell_prefix = "v"
    new_cell.display_name = f"v[{expression}]"
    new_cell.cell_kind = "bridge"
    new_cell.deferred_differential_expression = expression

    self.arrows[internal_name] = new_cell
    self.differential[new_cell] = None
    self.v[expression] = new_cell
    self._record_resolved_mp_expression(expression, new_cell)
    _record_virtual_massey_bridge_resolutions(self, expression, new_cell)
    self.attachment_record_for_cell(
        expression,
        None,
        self.v,
        expression,
        new_cell,
    )

    print(f"Attached new formal bridge cell {new_cell}")
    print(f"Internal arrow name: {internal_name}")
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Deferred concrete bridge differential.")

    return new_cell


def _is_virtual_massey_primitive(primitive):
    return bool(
        getattr(primitive, "virtual_primitive_cell", False)
        or getattr(primitive, "cell_kind", None) == "virtual_massey"
    )


def _is_bridge_promoted_massey_primitive_for_inputs(self, primitive, inputs):
    promoted_inputs = tuple(
        getattr(primitive, "bridge_virtual_massey_inputs", ()) or ()
    )

    if primitive is None or not promoted_inputs:
        return False

    try:
        target_key = self.mp_key(*tuple(self.normalize_mp_inputs(tuple(inputs))))
    except Exception:
        return True

    for promoted in promoted_inputs:
        try:
            promoted_key = self.mp_key(
                *tuple(self.normalize_mp_inputs(tuple(promoted)))
            )
        except Exception:
            continue

        if promoted_key == target_key:
            return True

    return False


def _single_virtual_massey_factor_from_product(self, product):
    factors = tuple(getattr(product, "factors", ()))

    if len(factors) != 1:
        return None

    factor = factors[0]

    if not isinstance(factor, MasseyProduct):
        return None

    if len(tuple(factor.inputs)) < 3:
        return None

    if _factor_is_virtual_massey(self, factor):
        return factor

    return None


def _bridge_product_can_resolve_virtual_massey(self, product):
    factors = tuple(getattr(product, "factors", ()))

    if len(factors) != 1:
        return True

    factor = factors[0]

    if not isinstance(factor, MasseyProduct):
        return True

    if len(tuple(factor.inputs)) <= 1:
        return True

    key = self.mp_key(*tuple(factor.inputs))

    return key in getattr(self, "resolved_massey_products", {})


def _record_virtual_massey_bridge_resolutions(self, expression, cell):
    if not isinstance(expression, MPElement) or len(expression.terms) < 2:
        return []

    products = tuple(expression.terms.keys())
    promoted = []

    for product in products:
        M = _single_virtual_massey_factor_from_product(self, product)

        if M is None:
            continue

        resolving_products = [
            other
            for other in products
            if other is not product
            and _bridge_product_can_resolve_virtual_massey(self, other)
        ]

        if not resolving_products:
            continue

        inputs = tuple(self.normalize_mp_inputs(tuple(M.inputs)))
        key = self.mp_key(*inputs)

        if key in getattr(self, "resolved_massey_products", {}):
            continue

        cell.virtual_primitive_cell = True
        promoted_inputs = list(getattr(cell, "bridge_virtual_massey_inputs", ()))
        promoted_inputs.append(inputs)
        cell.bridge_virtual_massey_inputs = tuple(promoted_inputs)
        self._record_resolved_mp(M, cell, check=False)
        promoted.append(inputs)

    return promoted


def _next_cell_internal_name(self):
    index = len(getattr(self, "arrows", {})) + 1

    while f"cell_{index}" in getattr(self, "arrows", {}):
        index += 1

    return f"cell_{index}"


def _massey_virtual_cell_height(M):
    heights = []

    for factor in getattr(M, "inputs", ()):
        height_fn = getattr(factor, "h", None)

        if callable(height_fn):
            try:
                heights.append(height_fn())
            except Exception:
                pass

    if heights:
        return max(heights) + 1

    return 1


def _attach_virtual_massey_cell(self, M):
    if not isinstance(M, MasseyProduct):
        print("The virtual MP cell index must be a MasseyProduct.")
        print("No cell was attached.")
        return None

    if M.Q is not self:
        print("Warning: this MasseyProduct belongs to a different quiver.")
        return None

    inputs = tuple(self.normalize_mp_inputs(M.inputs))
    key = self.mp_key(*inputs)

    existing = getattr(self, "resolved_massey_products", {}).get(key, None)

    if existing is not None:
        print("A primitive for this Massey product has already been recorded.")
        print(f"Existing cell: {existing}")
        return existing

    if getattr(self, "_loading_replay", False):
        try:
            primitive_keys, _primitive_records, _source_by_key = (
                _fast_known_mp_primitive_records(self)
            )
            tower_records = _fast_tower_records(self)
            defined = _fast_can_define_mp_from_certificates(
                self,
                inputs,
                primitive_keys,
                tower_records=tower_records,
                allow_bridge_replacements=True,
            )
        except Exception:
            defined = False

        if not defined:
            try:
                defined = self.can_define_mp(*inputs)
            except Exception:
                defined = False
    else:
        defined = self.can_define_mp(*inputs)

    if not defined:
        print(f"Warning: {M} is not defined yet.")
        return None

    if M in self.v:
        print("A cell with this differential/index has already been attached.")
        print(f"Existing cell: {self.v[M]}")
        return self.v[M]

    source = M.source
    target = M.target

    internal_name = _next_cell_internal_name(self)
    new_cell = Arrow(
        self,
        internal_name,
        source,
        target,
        grading=None,
        height=_massey_virtual_cell_height(M),
    )
    new_cell.index = M
    new_cell.cell_prefix = "v"
    new_cell.display_name = f"v[{M}]"
    new_cell.cell_kind = "virtual_massey"
    new_cell.virtual_primitive_cell = True
    new_cell.deferred_differential_expression = M
    new_cell.virtual_massey_inputs = inputs

    self.arrows[internal_name] = new_cell
    self.differential[new_cell] = None
    self.v[M] = new_cell
    self._record_resolved_mp(M, new_cell, check=False)
    self.attachment_record_for_cell(
        M,
        None,
        self.v,
        M,
        new_cell,
    )

    print(f"Attached new virtual Massey cell {new_cell}")
    print(f"Internal arrow name: {internal_name}")
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("Deferred concrete Massey differential.")

    return new_cell


def direct_mp_block_primitive(self, *inputs):
    base = getattr(type(self), "_cyclic_base_direct_mp_block_primitive", None)

    if base is None:
        return None

    if _massey_formula_disabled(self):
        inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

        if len(inputs) == 1 and _is_higher_massey_factor(inputs[0]):
            key = self.mp_key(*tuple(inputs[0].inputs))
            return getattr(self, "resolved_massey_products", {}).get(key, None)

        if any(_is_higher_massey_factor(item) for item in inputs):
            try:
                factors = self.canonical_mp_factors(inputs)
                expr_key = self.mp_expression_key(MPProduct(self, factors))
            except Exception:
                expr_key = None

            if expr_key is not None:
                return getattr(self, "resolved_mp_expressions", {}).get(
                    expr_key,
                    None,
                )

            return None

    primitive = base(self, *inputs)

    if _is_virtual_massey_primitive(primitive):
        return None

    if _is_absorbing_higher_product(primitive):
        return None

    return primitive


def _eval_mp_cell_arg(self, value):
    if not isinstance(value, str):
        return value

    try:
        return eval(value, self.mp_eval_environment())
    except Exception as exc:
        print("Could not understand this MP expression.")
        print("Python error:", exc)
        return None


def _attach_massey_product_cell(self, M):
    if M is None:
        return None

    if not isinstance(M, MasseyProduct):
        return None

    self.last_refused_mp_cell = None
    inputs = tuple(self.normalize_mp_inputs(M.inputs))

    equivalent_resolution = None

    if not getattr(self, "_loading_replay", False):
        equivalent_resolution = self.mp_presentation_equivalent_primitive_report(
            inputs,
            include_self=False,
        )

    if equivalent_resolution is not None:
        try:
            current_str = self.format_mp_input_product(inputs)
            equivalent_str = self.format_mp_input_product(
                equivalent_resolution.get("equivalent_inputs", ())
            )
        except Exception:
            current_str = str(inputs)
            equivalent_str = str(equivalent_resolution.get("equivalent_inputs", ()))

        print("An equivalent Massey presentation already has a primitive.")
        print(f"Current presentation: {current_str}")
        print(f"Equivalent resolved presentation: {equivalent_str}")
        print(f"Existing cell: {equivalent_resolution.get('primitive')}")
        print("No cell was attached.")
        self.last_refused_mp_cell = {
            "reason": "equivalent_resolved",
            "inputs": inputs,
            "equivalent_resolution": equivalent_resolution,
        }
        return None

    has_product_value_input = _mp_input_contains_product_value(M)

    if has_product_value_input:
        direct_defined = False
    else:
        try:
            direct_defined = self.can_define_mp_direct(*inputs)
        except Exception:
            direct_defined = False

    base = getattr(type(self), "_cyclic_base_attach_one_cell", None)

    if (
        direct_defined
        and base is not None
        and not getattr(self, "_suppress_primitive_expansion", False)
        and not _massey_formula_disabled(self)
    ):
        return base(self, M)

    if getattr(self, "_loading_replay", False):
        try:
            primitive_keys, primitive_records, _source_by_key = (
                _fast_known_mp_primitive_records(self)
            )
            tower_records = _fast_tower_records(self)
            defined = _fast_can_define_mp_from_certificates(
                self,
                inputs,
                primitive_keys,
                tower_records=tower_records,
                allow_bridge_replacements=True,
            )
        except Exception:
            defined = False

        if not defined:
            try:
                defined = self.can_define_mp(*inputs)
            except Exception:
                defined = False
    else:
        try:
            defined = self.can_define_mp(*inputs)
        except Exception:
            defined = False

        if not defined:
            try:
                primitive_keys, primitive_records, _source_by_key = (
                    _fast_known_mp_primitive_records(self)
                )
                tower_records = _fast_tower_records(self)
                defined = _fast_can_define_mp_from_certificates(
                    self,
                    inputs,
                    primitive_keys,
                    tower_records=tower_records,
                    allow_bridge_replacements=True,
                )
            except Exception:
                defined = False

    if defined:
        return _attach_virtual_massey_cell(self, M)

    print(f"Warning: {M} is not defined yet.")
    return None


def attach_one_cell(self, f):
    if isinstance(f, MasseyProduct):
        return _attach_massey_product_cell(self, f)

    base = getattr(type(self), "_cyclic_base_attach_one_cell", None)

    if base is None:
        print("No base cell-attachment method is available.")
        return None

    return base(self, f)


def attach_mp_cell(self, f=None):
    if f is None:
        base = getattr(type(self), "_cyclic_base_attach_mp_cell", None)

        if base is not None:
            return base(self, f)

        return None

    f = _eval_mp_cell_arg(self, f)

    if f is None:
        return None

    if isinstance(f, MasseyProduct):
        return _attach_massey_product_cell(self, f)

    if not isinstance(f, (MPProduct, MPElement)):
        print("The MP cell index must be a MasseyProduct, MPProduct, or MPElement.")
        print("No cell was attached.")
        return None

    base = getattr(type(self), "_cyclic_base_attach_mp_cell", None)

    if base is None:
        print("No base MP-cell attachment method is available.")
        return None

    return base(self, f)


def attach_bridge(self, g1, g2=None):
    self.last_refused_bridge_cell = None
    left = _eval_bridge_expression_arg(self, g1, "first")

    if left is None:
        return None

    has_second_arg = g2 is not None
    right = _eval_bridge_expression_arg(self, g2, "second")

    if has_second_arg and right is None:
        return None

    redundancy_report = _generator_bridge_redundancy_report(
        self,
        left,
        right if has_second_arg else None,
    )

    if redundancy_report is not None:
        warning = _format_generator_bridge_redundancy_warning(
            self,
            redundancy_report,
        )
        print(warning)
        print("No bridge cell was attached.")
        self.last_refused_bridge_cell = redundancy_report
        return None

    if not (
        getattr(self, "_suppress_primitive_expansion", False)
        or getattr(self, "defer_bridge_expansion", False)
    ):
        base = getattr(type(self), "_cyclic_base_attach_bridge", None)

        if base is not None:
            before = len(getattr(self, "attachment_history", ()))
            cell = base(self, left, right if has_second_arg else None)

            if cell is not None:
                return cell

            if len(getattr(self, "attachment_history", ())) != before:
                return cell

            expression = _bridge_mp_difference(
                self,
                left,
                right if has_second_arg else None,
            )

            if (
                expression is None
                or not _bridge_expression_has_virtual_massey_factor(self, expression)
            ):
                return cell

            return _attach_deferred_bridge_cell(self, expression)

    expression = _bridge_mp_difference(self, left, right if has_second_arg else None)

    if expression is None:
        return None

    return _attach_deferred_bridge_cell(self, expression)


def attach_bridge_cell(self, g1, g2=None):
    return self.attach_bridge(g1, g2)


def cyclic_factor_key(self, factor):
    return self.mp_factor_key(factor)


def cyclic_factor_tuple_key(self, factors):
    return tuple(self.cyclic_factor_key(factor) for factor in tuple(factors))


def cyclic_rotations(self, factors):
    factors = tuple(factors)

    if not factors:
        return []

    return [
        factors[i:] + factors[:i]
        for i in range(len(factors))
    ]


def canonical_cyclic_factor_tuple(self, factors):
    rotations = self.cyclic_rotations(tuple(factors))

    if not rotations:
        return ()

    return min(
        rotations,
        key=lambda rotation: repr(self.cyclic_factor_tuple_key(rotation))
    )


def canonical_cyclic_factor_key(self, factors):
    return self.cyclic_factor_tuple_key(
        self.canonical_cyclic_factor_tuple(factors)
    )


def mp_factors_composable(self, factors, cyclic=False):
    factors = tuple(factors)

    if not factors:
        return False

    for left, right in zip(factors, factors[1:]):
        if left.target != right.source:
            return False

    if cyclic and factors[-1].target != factors[0].source:
        return False

    return True


def cyclic_factor_alphabet(
    self,
    include_arrows=True,
    include_cells=True,
    include_higher_massey_products=True,
    resolved_higher_only=False,
):
    factors = []

    if include_arrows:
        for name in sorted(getattr(self, "arrows", {}).keys()):
            arrow = self.arrows[name]

            if not include_cells and (
                hasattr(arrow, "cell_prefix") or hasattr(arrow, "index")
            ):
                continue

            mp_arrow = self.mp(arrow)

            if mp_arrow is not None:
                factors.append(mp_arrow)

    if include_higher_massey_products:
        mp_items = sorted(
            getattr(self, "massey_products", {}).items(),
            key=lambda item: repr(item[0])
        )

        for key, M in mp_items:
            if isinstance(M, MasseyProduct) and len(M.inputs) >= 3:
                if resolved_higher_only and key not in getattr(self, "resolved_massey_products", {}):
                    continue

                if _mp_input_contains_product_value(M):
                    continue

                primitive = getattr(self, "resolved_massey_products", {}).get(key, None)

                if _is_virtual_massey_primitive(primitive):
                    continue

                factors.append(M)

    out = []
    seen = set()

    for factor in factors:
        factor_key = self.cyclic_factor_key(factor)

        if factor_key in seen:
            continue

        seen.add(factor_key)
        out.append(factor)

    return tuple(out)


def _inverse_coeff(self, coeff):
    if hasattr(self, "coeff_inverse_if_unit"):
        return self.coeff_inverse_if_unit(coeff)

    try:
        return simplify_coeff(1 / coeff)
    except Exception:
        return None


def _element_scalar_multiple(self, numerator, denominator):
    if hasattr(self, "element_scalar_multiple"):
        return self.element_scalar_multiple(numerator, denominator)

    numerator = to_element(numerator)
    denominator = to_element(denominator)

    if not denominator.terms:
        return None

    scalar = None

    for path, denominator_coeff in denominator.terms.items():
        numerator_coeff = numerator.terms.get(path, 0)

        try:
            quotient = simplify_coeff(numerator_coeff / denominator_coeff)
        except Exception:
            return None

        if scalar is None:
            scalar = quotient
        elif not is_zero_coeff(simplify_coeff(quotient - scalar)):
            return None

    for path, coeff in numerator.terms.items():
        if path not in denominator.terms and not is_zero_coeff(coeff):
            return None

    if scalar is None:
        return None

    if (numerator - scalar * denominator).is_zero():
        return simplify_coeff(scalar)

    return None


def _dedupe_primitives(self, primitive_records):
    out = []
    seen = set()

    for record in primitive_records:
        primitive = record["primitive"]
        primitive_key = primitive.key() if hasattr(primitive, "key") else repr(primitive)
        key = (record.get("source"), primitive_key)

        if key in seen:
            continue

        seen.add(key)
        out.append(record)

    return out


def exact_product_block_resolution(self, block, verify=True):
    """
    Return data for an exact product block primitive.

    This only accepts primitives whose differential is a scalar multiple of the
    expanded product of the block. A single resolved higher Massey factor is
    also a resolved length-one formal product block, even when bridge-certified
    lower blocks keep its expansion unavailable.
    """

    try:
        factors = self.canonical_mp_factors(tuple(block))
    except Exception:
        return {
            "resolved": False,
            "factors": tuple(block),
            "reason": "could not canonicalize block",
        }

    if len(factors) < 1:
        return {
            "resolved": False,
            "factors": factors,
            "reason": "product blocks must be nonempty",
        }

    if not self.mp_factors_composable(factors, cyclic=False):
        return {
            "resolved": False,
            "factors": factors,
            "reason": "block is not composable",
        }

    absorbing_resolution = _absorbing_higher_product_resolution_for_block(
        self,
        factors,
    )

    if absorbing_resolution is not None:
        primitive = absorbing_resolution.get("primitive")

        if primitive is not None:
            return {
                "resolved": True,
                "factors": factors,
                "target": MPProduct(self, factors),
                "primitive": primitive,
                "raw_primitive": primitive,
                "coefficient": 1,
                "source": "absorbing_higher_product",
                "verified": False,
                "absorbing_higher_product": True,
                "formal_product_certificate": True,
                "virtual_primitive": True,
                "deferred_primitive": True,
                "resolution_group_key": absorbing_resolution.get(
                    "resolution_group_key"
                ),
                "absorbed_product_factors": tuple(
                    absorbing_resolution.get("absorbed_product_factors", ())
                ),
                "bridge_relation": absorbing_resolution.get("bridge_relation"),
                "reason": "absorbing higher product certificate",
            }

    resolved_massey_factor_record = None

    if len(factors) == 1 and isinstance(factors[0], MasseyProduct):
        key = self.mp_key(*factors[0].inputs)
        primitive = getattr(self, "resolved_massey_products", {}).get(
            key,
            None
        )

        if primitive is not None:
            resolved_massey_factor_record = {
                "source": "resolved_massey_factor",
                "primitive": primitive,
            }

            if (
                _is_virtual_massey_primitive(primitive)
                or getattr(self, "_suppress_primitive_expansion", False)
            ):
                return {
                    "resolved": True,
                    "factors": factors,
                    "target": factors[0],
                    "primitive": primitive,
                    "raw_primitive": primitive,
                    "coefficient": 1,
                    "source": "resolved_massey_factor",
                    "verified": False,
                    "formal_massey_factor": True,
                    "formal_product_certificate": True,
                    "virtual_primitive": _is_virtual_massey_primitive(primitive),
                    "deferred_primitive": True,
                    "reason": "resolved Massey factor certificate",
                }

    product = MPProduct(self, factors)
    expression_key = self.mp_expression_key(product)
    primitive = getattr(self, "resolved_mp_expressions", {}).get(
        expression_key,
        None
    )

    if (
        primitive is not None
        and getattr(self, "_suppress_primitive_expansion", False)
    ):
        return {
            "resolved": True,
            "factors": factors,
            "target": product,
            "primitive": primitive,
            "raw_primitive": primitive,
            "coefficient": 1,
            "source": "mp_product_cell",
            "verified": False,
            "formal_product_certificate": True,
            "deferred_primitive": True,
            "virtual_primitive": _is_virtual_massey_primitive(primitive),
            "reason": "recorded MP product primitive certificate",
        }

    if getattr(self, "_suppress_primitive_expansion", False):
        return {
            "resolved": False,
            "factors": factors,
            "target": None,
            "reason": "no formal exact product certificate in certificate mode",
        }

    target = self.mp_factors_to_element(factors)

    if target is None or target.is_zero():
        if resolved_massey_factor_record is not None:
            primitive = resolved_massey_factor_record["primitive"]

            return {
                "resolved": True,
                "factors": factors,
                "target": factors[0],
                "primitive": primitive,
                "raw_primitive": primitive,
                "coefficient": 1,
                "source": resolved_massey_factor_record["source"],
                "verified": False,
                "formal_massey_factor": True,
                "reason": "resolved Massey factor has no expanded target",
            }

        return {
            "resolved": False,
            "factors": factors,
            "target": target,
            "reason": "target product does not expand to a nonzero element",
        }

    primitive_records = []

    if primitive is not None:
        primitive_records.append({
            "source": "mp_product_cell",
            "primitive": primitive,
        })

    if resolved_massey_factor_record is not None:
        primitive_records.append(resolved_massey_factor_record)

    try:
        block_key = self.mp_product_block_key(factors)
        primitive = self.direct_mp_block_primitive(*block_key)
    except Exception:
        primitive = None

    if primitive is not None:
        primitive_records.append({
            "source": "direct_mp_block",
            "primitive": primitive,
        })

    if len(target.terms) == 1:
        path, coeff = next(iter(target.terms.items()))

        if coeff == 1:
            path_key = tuple(path.arrows)
            primitive = getattr(self, "cells", {}).get(path_key, None)

            if primitive is not None:
                primitive_records.append({
                    "source": "ordinary_cell",
                    "primitive": primitive,
                })

    for record in _dedupe_primitives(self, primitive_records):
        primitive = record["primitive"]

        try:
            differential = self.d(primitive)
        except Exception:
            continue

        coefficient = _element_scalar_multiple(self, differential, target)

        if coefficient is None:
            continue

        inverse = _inverse_coeff(self, coefficient)

        if inverse is None:
            continue

        scaled_primitive = inverse * primitive

        if verify and not (self.d(scaled_primitive) - target).is_zero():
            continue

        return {
            "resolved": True,
            "factors": factors,
            "target": target,
            "primitive": scaled_primitive,
            "raw_primitive": primitive,
            "coefficient": coefficient,
            "source": record.get("source"),
            "verified": True,
        }

    return {
        "resolved": False,
        "factors": factors,
        "target": target,
        "reason": "no verified exact product primitive",
    }


def _bridge_candidate_original_context(candidate):
    for context in tuple(candidate.get("profile_contexts", ())):
        if context.get("context") == "original":
            span = context.get("span", None)

            if span is None:
                continue

            try:
                start, stop = int(span[0]), int(span[1])
            except Exception:
                continue

            if start < 0 or stop <= start:
                continue

            return {
                "span": (start, stop),
                "block": tuple(context.get("block", ())),
                "context": context,
            }

    return None


def _bridge_candidate_spans_whole_original(candidate, factors):
    context = _bridge_candidate_original_context(candidate)

    if context is None:
        return False

    return context["span"] == (0, len(tuple(factors)))


def _bridge_replacement_product_resolution_candidates(
    self,
    factors,
    minimal_only=True,
):
    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return []

    if len(factors) < 2:
        return []

    if not self.mp_factors_composable(factors, cyclic=False):
        return []

    try:
        cache_key = (
            tuple(self.mp_factor_key(factor) for factor in factors),
            bool(minimal_only),
            _tower_cache_state_signature(self),
        )
    except Exception:
        cache_key = None

    cache = getattr(self, "_bridge_replacement_product_resolution_cache", None)

    if cache is None:
        cache = {}
        self._bridge_replacement_product_resolution_cache = cache

    if cache_key is not None and cache_key in cache:
        return [dict(candidate) for candidate in cache[cache_key]]

    # Game-state checks only need existence certificates.  Use the metadata
    # search directly so bridge/A_inf replacement logic does not materialize
    # the potentially enormous primitive formulas.
    try:
        bridge_candidates = _metadata_bridge_replacement_primitive_candidates(
            self,
            MPProduct(self, factors),
            record=False,
            minimal_only=minimal_only,
            max_depth=_BRIDGE_REPLACEMENT_DEPTH_UNSET,
        )
    except Exception:
        return []

    out = []
    seen = set()

    for candidate in bridge_candidates:
        context = _bridge_candidate_original_context(candidate)

        if context is None:
            continue

        start, stop = context["span"]

        if stop > len(factors):
            continue

        block = tuple(factors[start:stop])
        candidate_key = (
            (start, stop),
            tuple(self.mp_factor_key(factor) for factor in block),
            tuple(
                (
                    record.get("occurrence_span_before"),
                    record.get("target_key"),
                    record.get("replacement_key"),
                )
                for record in tuple(candidate.get("bridge_path", ()))
            ),
            candidate.get("primitive_block_span", None),
        )

        if candidate_key in seen:
            continue

        seen.add(candidate_key)
        resolution = dict(candidate)
        resolution.update({
            "left": factors[:start],
            "block": block,
            "right": factors[stop:],
            "source": "bridge_replacement",
            "block_span": (start, stop),
            "minimal": start == 0 and stop == len(factors),
            "sign_source": factors[:start],
            "verified": bool(
                candidate.get("deferred_primitive")
                or candidate.get("virtual_primitive")
                or candidate.get("primitive_element") is not None
            ),
            "bridge_resolved": True,
            "original_context": context.get("context"),
        })

        primitive_element = self.primitive_candidate_to_element(candidate)

        if primitive_element is not None:
            target = self.mp_factors_to_element(factors)

            if target is not None:
                resolution["primitive_element"] = primitive_element
                resolution["verified"] = (self.d(primitive_element) - target).is_zero()

        out.append(resolution)

    out.extend(
        _tower_replacement_product_resolution_candidates(
            self,
            factors,
            minimal_only=minimal_only,
        )
    )

    if cache_key is not None:
        cache[cache_key] = tuple(dict(candidate) for candidate in out)

    return out


def _bridge_pure_orbit_product_candidate(self, factors):
    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return None

    if len(factors) != 1:
        return None

    try:
        relations = self.bridge_product_relations()
    except Exception:
        relations = ()

    for relation in tuple(relations or ()):
        sides = (
            (tuple(relation.get("left", ())), tuple(relation.get("right", ()))),
            (tuple(relation.get("right", ())), tuple(relation.get("left", ()))),
        )

        for source_word, target_word in sides:
            try:
                source_word = self.canonical_mp_factors(tuple(source_word))
                target_word = self.canonical_mp_factors(tuple(target_word))
            except Exception:
                continue

            if not self.mp_factors_equal(target_word, factors):
                continue

            orbit_resolution = _single_massey_factor_orbit_resolution(
                self,
                source_word,
            )

            if orbit_resolution is None:
                continue

            return {
                "kind": "bridge_pure_massey_orbit",
                "source": "bridge_pure_massey_orbit",
                "virtual_primitive": True,
                "deferred_primitive": True,
                "left": (),
                "block": factors,
                "right": (),
                "block_span": (0, 1),
                "minimal": True,
                "sign_source": (),
                "primitive": None,
                "source_product_factors": source_word,
                "bridge_relation": relation,
                "pure_orbit_resolution": orbit_resolution,
                "verified": False,
            }

    return None


def product_word_resolution_candidates(
    self,
    factors,
    verify=True,
    use_bridge_replacements=True,
    use_ainf_replacements=True,
):
    """
    Find exact sub-block primitives resolving one linear product word.
    """

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return []

    if not self.mp_factors_composable(factors, cyclic=False):
        return []

    n = len(factors)
    suppress_expansion = bool(getattr(self, "_suppress_primitive_expansion", False))
    target = None
    target_expanded = False

    def expanded_target():
        nonlocal target, target_expanded

        if not target_expanded:
            target = self.mp_factors_to_element(factors)
            target_expanded = True

        return target

    if use_ainf_replacements:
        stasheff_zero_candidates = _stasheff_zero_product_resolution_candidates(
            self,
            factors,
        )
    else:
        stasheff_zero_candidates = []

    if not suppress_expansion and expanded_target() is None:
        return stasheff_zero_candidates

    candidates = list(stasheff_zero_candidates)

    bridge_orbit_candidate = _bridge_pure_orbit_product_candidate(
        self,
        factors,
    )

    if bridge_orbit_candidate is not None:
        candidates.append(bridge_orbit_candidate)

    for start in range(n):
        for stop in range(start + 1, n + 1):
            block = factors[start:stop]
            resolution = self.exact_product_block_resolution(
                block,
                verify=verify
            )

            if not resolution.get("resolved"):
                continue

            candidate = {
                "left": factors[:start],
                "block": block,
                "right": factors[stop:],
                "primitive": resolution["primitive"],
                "raw_primitive": resolution.get("raw_primitive"),
                "coefficient": resolution.get("coefficient", 1),
                "source": resolution.get("source"),
                "block_span": (start, stop),
                "minimal": start == 0 and stop == n,
                "sign_source": factors[:start],
            }

            if resolution.get("resolution_group_key") is not None:
                candidate["resolution_group_key"] = resolution.get(
                    "resolution_group_key"
                )

            if resolution.get("absorbing_higher_product"):
                candidate["absorbing_higher_product"] = True
                candidate["absorbed_product_factors"] = tuple(
                    resolution.get("absorbed_product_factors", ())
                )

            if (
                resolution.get("formal_product_certificate")
                or (
                    resolution.get("formal_massey_factor")
                    and resolution.get("virtual_primitive")
                )
            ):
                if resolution.get("formal_massey_factor"):
                    candidate["formal_massey_factor"] = True
                if resolution.get("formal_product_certificate"):
                    candidate["formal_product_certificate"] = True
                candidate["virtual_primitive"] = bool(
                    resolution.get("virtual_primitive")
                )
                candidate["deferred_primitive"] = True
                candidate["verified"] = False
                candidates.append(candidate)
                continue

            target_value = expanded_target()

            if target_value is None:
                continue

            primitive_element = self.primitive_candidate_to_element(candidate)

            if primitive_element is None:
                continue

            candidate["primitive_element"] = primitive_element
            candidate["verified"] = (self.d(primitive_element) - target_value).is_zero()

            if candidate["verified"]:
                candidates.append(candidate)

    if use_bridge_replacements:
        try:
            candidates.extend(
                _virtual_tower_primitive_candidates_for_product(
                    self,
                    MPProduct(self, factors),
                    minimal_only=True,
                )
            )
        except Exception:
            pass

        candidates.extend(
            _bridge_replacement_product_resolution_candidates(
                self,
                factors,
                minimal_only=True,
            )
        )

    return candidates


def _candidate_block_span(candidate):
    span = candidate.get("block_span", None)

    if span is not None:
        try:
            start, stop = int(span[0]), int(span[1])
        except Exception:
            start = stop = None

        if start is not None and 0 <= start < stop:
            return (start, stop)

    left = tuple(candidate.get("left", ()) or ())
    block = tuple(candidate.get("block", ()) or ())

    if not block:
        return None

    start = len(left)
    return (start, start + len(block))


def _candidate_resolution_group_key(self, candidate):
    if candidate.get("resolution_group_key") is not None:
        return candidate.get("resolution_group_key")

    source = candidate.get("source", "")
    kind = candidate.get("kind", "")

    if source == "completed_massey_tower" or kind == "completed_massey_tower":
        tower_record = candidate.get("tower_record")

        if tower_record is None and isinstance(candidate.get("tower_report"), dict):
            tower_record = candidate["tower_report"].get("record")

        if isinstance(tower_record, dict):
            return (
                "completed_massey_tower",
                _completed_tower_record_key(self, tower_record),
            )

    if (
        source == "completed_massey_pair_tower"
        or kind == "completed_massey_pair_tower"
    ):
        pair_record = candidate.get("pair_tower_record")

        if pair_record is None and isinstance(candidate.get("pair_tower_report"), dict):
            pair_record = candidate["pair_tower_report"].get("record")

        if isinstance(pair_record, dict):
            return (
                "completed_massey_pair_tower",
                _completed_pair_tower_record_key(self, pair_record),
            )

    block = tuple(candidate.get("block", ()) or ())

    try:
        block_key = self.cyclic_factor_tuple_key(block)
    except Exception:
        block_key = tuple(repr(item) for item in block)

    return ("primitive_block", block_key, source or kind)


def _minimal_resolution_sources_for_rotation(self, rotation_index, rotation, candidates):
    usable = []

    for candidate in tuple(candidates or ()):
        if not isinstance(candidate, dict):
            continue

        block = tuple(candidate.get("block", ()) or ())

        if not block:
            continue

        span = _candidate_block_span(candidate)

        if span is None:
            continue

        usable.append((candidate, span, block))

    minimal = []

    for candidate, span, block in usable:
        start, stop = span
        has_smaller = False

        for other, other_span, _other_block in usable:
            if other is candidate:
                continue

            other_start, other_stop = other_span

            if (
                start <= other_start
                and other_stop <= stop
                and (start, stop) != (other_start, other_stop)
            ):
                has_smaller = True
                break

        if has_smaller:
            continue

        try:
            block_key = self.cyclic_factor_tuple_key(block)
        except Exception:
            block_key = tuple(repr(item) for item in block)

        minimal.append({
            "rotation_index": rotation_index,
            "rotation": tuple(rotation),
            "block": block,
            "span": span,
            "source": candidate.get("source") or candidate.get("kind") or "",
            "kind": candidate.get("kind", ""),
            "candidate": candidate,
            "block_key": block_key,
            "resolution_group_key": _candidate_resolution_group_key(self, candidate),
        })

    deduped = []
    seen = set()

    for item in minimal:
        key = (
            item["rotation_index"],
            item["span"],
            repr(item["block_key"]),
            repr(item["resolution_group_key"]),
        )

        if key in seen:
            continue

        seen.add(key)
        deduped.append(item)

    return tuple(deduped)


def _product_resolution_compatibility_summary(self, sources):
    sources = tuple(sources or ())
    block_keys = set()
    group_keys = set()

    for source in sources:
        block = tuple(source.get("block", ()) or ())

        try:
            block_keys.add(repr(self.cyclic_factor_tuple_key(block)))
        except Exception:
            block_keys.add(repr(tuple(repr(item) for item in block)))

        group_key = source.get("resolution_group_key")

        if group_key is None:
            group_key = _product_resolution_group_key(self, source)

        group_keys.add(repr(group_key))

    return {
        "minimal_resolution_count": len(sources),
        "minimal_resolution_block_count": len(block_keys),
        "resolution_group_count": len(group_keys),
        "compatible_resolutions": len(sources) >= 2 and len(block_keys) <= 1,
        "incompatible_resolution_count": len(block_keys),
    }


def _pair_tower_seed_key_pair(self, source):
    source = source if isinstance(source, dict) else {}

    if (source.get("source") or source.get("kind") or "") != "bridge_replacement":
        return None

    candidate = source.get("candidate", {})

    if not isinstance(candidate, dict):
        return None

    source_primitive = candidate.get("source_primitive", {})

    if not isinstance(source_primitive, dict):
        return None

    source_name = source_primitive.get("source") or source_primitive.get("kind")

    if source_name != "completed_massey_pair_tower":
        return None

    pair_report = source_primitive.get("pair_tower_report", {})

    if not isinstance(pair_report, dict):
        pair_report = {}

    left_seed = tuple(pair_report.get("left_seed_inputs", ()) or ())
    right_seed = tuple(pair_report.get("right_seed_inputs", ()) or ())

    if not left_seed or not right_seed:
        pair_record = source_primitive.get("pair_tower_record", {})

        if isinstance(pair_record, dict):
            left_record = pair_record.get("left_record", {})
            right_record = pair_record.get("right_record", {})

            if isinstance(left_record, dict):
                left_seed = tuple(left_record.get("seed_inputs", ()) or ())

            if isinstance(right_record, dict):
                right_seed = tuple(right_record.get("seed_inputs", ()) or ())

    if not left_seed or not right_seed:
        return None

    try:
        return (
            tuple(self.mp_factor_key(item) for item in left_seed),
            tuple(self.mp_factor_key(item) for item in right_seed),
        )
    except Exception:
        return (
            tuple(repr(item) for item in left_seed),
            tuple(repr(item) for item in right_seed),
        )


def _opposite_pair_tower_bridge_resolution_report(self, sources):
    sources = tuple(
        source
        for source in tuple(sources or ())
        if isinstance(source, dict)
    )

    for left_index, left_source in enumerate(sources):
        left_pair = _pair_tower_seed_key_pair(self, left_source)

        if left_pair is None:
            continue

        left_seed, right_seed = left_pair

        if left_seed == right_seed:
            continue

        for right_source in sources[left_index + 1:]:
            right_pair = _pair_tower_seed_key_pair(self, right_source)

            if right_pair != (right_seed, left_seed):
                continue

            if left_source.get("rotation_index") == right_source.get("rotation_index"):
                continue

            chain_report = _cyclic_resolution_chain_report(
                self,
                left_source,
                right_source,
                relations=(),
            )

            return {
                "likely_over": True,
                "reason": "opposite completed pair-tower bridge resolutions",
                "sources": (left_source, right_source),
                "left_seed_key": left_seed,
                "right_seed_key": right_seed,
                "chain_report": chain_report,
            }

    return None


def _product_minimal_source_is_inherited(source):
    source_name = source.get("source") or source.get("kind") or ""
    return source_name in {
        "absorbing_higher_product",
        "bridge_pure_massey_orbit",
        "bridge_replacement",
        "completed_massey_pair_tower",
        "completed_massey_tower",
        "resolved_massey_factor",
        "stasheff_zero",
    }


def _product_cycle_candidate_is_direct(candidate):
    if not isinstance(candidate, dict):
        return False

    if candidate.get("virtual_primitive") or candidate.get("deferred_primitive"):
        return False

    source_name = candidate.get("source") or candidate.get("kind") or ""
    return source_name not in {
        "absorbing_higher_product",
        "bridge_replacement",
        "completed_massey_tower",
        "resolved_massey_factor",
        "resolved_massey_product",
        "resolved_massey_factor_product",
        "stasheff_zero",
    }


def _product_cycle_candidate_primitive_key(self, candidate):
    primitive = (
        candidate.get("raw_primitive")
        or candidate.get("primitive")
        or candidate.get("primitive_element")
    )

    if primitive is None:
        return ("primitive", None)

    try:
        return ("primitive", self.mp_factor_key(primitive))
    except Exception:
        return ("primitive", repr(primitive), id(primitive))


def _product_cycle_candidate_summary(self, candidate):
    return {
        "left": tuple(candidate.get("left", ()) or ()),
        "block": tuple(candidate.get("block", ()) or ()),
        "right": tuple(candidate.get("right", ()) or ()),
        "block_span": _candidate_block_span(candidate),
        "primitive": candidate.get("primitive"),
        "raw_primitive": candidate.get("raw_primitive"),
        "source": candidate.get("source") or candidate.get("kind") or "",
        "primitive_key": _product_cycle_candidate_primitive_key(self, candidate),
    }


def _replacement_relation_is_ainf_equivalence(relation):
    if not isinstance(relation, dict):
        return False

    if relation.get("virtual_stasheff"):
        return True

    replacement_type = str(relation.get("replacement_type") or "")

    return replacement_type == "ainf"


def _replacement_relation_summary(self, relation):
    relation = relation if isinstance(relation, dict) else {}

    return {
        "left": tuple(relation.get("left", ()) or ()),
        "right": tuple(relation.get("right", ()) or ()),
        "replacement_type": relation.get("replacement_type", ""),
        "ainf_kind": relation.get("ainf_kind", ""),
        "virtual_stasheff": bool(relation.get("virtual_stasheff")),
        "source_relation": relation.get("source_relation"),
        "edge": relation.get("edge"),
        "cell": relation.get("cell"),
        "expression": relation.get("expression"),
    }


def _linear_replacement_path_between(
    self,
    start,
    target,
    relations,
    max_depth=6,
):
    try:
        start = self.canonical_mp_factors(tuple(start))
        target = self.canonical_mp_factors(tuple(target))
        target_key = self.cyclic_factor_tuple_key(target)
    except Exception:
        return None

    queue = [(start, ())]
    seen = {self.cyclic_factor_tuple_key(start)}

    try:
        max_depth = max(0, int(max_depth))
    except Exception:
        max_depth = 6

    while queue:
        word, path = queue.pop(0)

        if len(path) >= max_depth:
            continue

        n = len(word)

        for relation in tuple(relations or ()):
            directions = (
                (("left", "right"),)
                if relation.get("directed")
                else (("left", "right"), ("right", "left"))
            )

            for source_name, target_name in directions:
                source = tuple(relation.get(source_name, ()) or ())
                replacement = tuple(relation.get(target_name, ()) or ())
                m = len(source)

                if m == 0 or m > n:
                    continue

                for start_index in range(0, n - m + 1):
                    if not self.mp_factors_equal(
                        word[start_index:start_index + m],
                        source,
                    ):
                        continue

                    next_word = (
                        word[:start_index]
                        + replacement
                        + word[start_index + m:]
                    )

                    if next_word and not self.mp_factors_composable(
                        next_word,
                        cyclic=False,
                    ):
                        continue

                    try:
                        next_key = self.cyclic_factor_tuple_key(next_word)
                    except Exception:
                        continue

                    if next_key in seen:
                        continue

                    step = {
                        "from": tuple(word),
                        "to": tuple(next_word),
                        "span": (start_index, start_index + m),
                        "relation": _replacement_relation_summary(
                            self,
                            relation,
                        ),
                    }

                    next_path = path + (step,)

                    if next_key == target_key:
                        return next_path

                    seen.add(next_key)
                    queue.append((next_word, next_path))

    return None


def replacement_relation_cycle_class_reports(self, relations=None, record=True):
    """
    Detect replacement-equivalence cycles, especially A_inf plus bridge paths.

    These are not new primitive cells, but they do mean the presentation has two
    independent reasons for an equivalence: a virtual Stasheff relation and an
    already-existing non-A_inf replacement path.
    """

    if relations is None:
        try:
            relations = self.product_replacement_relations(
                include_bridge=True,
                include_ainf=True,
            )
        except Exception:
            relations = ()

    relations = tuple(relations or ())
    non_ainf_relations = tuple(
        relation
        for relation in relations
        if not _replacement_relation_is_ainf_equivalence(relation)
    )
    classes = []
    seen = set()

    for relation in relations:
        if not _replacement_relation_is_ainf_equivalence(relation):
            continue

        left = tuple(relation.get("left", ()) or ())
        right = tuple(relation.get("right", ()) or ())

        if not left or not right:
            continue

        path = _linear_replacement_path_between(
            self,
            left,
            right,
            non_ainf_relations,
        )

        if path is None:
            reverse_path = _linear_replacement_path_between(
                self,
                right,
                left,
                non_ainf_relations,
            )

            if reverse_path is None:
                continue

            path = reverse_path
            left, right = right, left

        try:
            left_key = self.cyclic_factor_tuple_key(left)
            right_key = self.cyclic_factor_tuple_key(right)
        except Exception:
            continue

        class_key = (
            "replacement_relation_cycle",
            tuple(sorted((repr(left_key), repr(right_key)))),
            tuple(
                repr(self.cyclic_factor_tuple_key(tuple(step.get("to", ()))))
                for step in path
            ),
        )

        if class_key in seen:
            continue

        seen.add(class_key)
        classes.append({
            "kind": "replacement_relation_cycle",
            "factors": left,
            "length": len(left),
            "resolved": True,
            "likely_over": True,
            "likely_over_reason": (
                "A_inf equivalence is already connected by non-A_inf replacements"
            ),
            "left": left,
            "right": right,
            "ainf_relation": _replacement_relation_summary(self, relation),
            "non_ainf_path": path,
        })

    if record:
        self.replacement_relation_cycle_classes = tuple(classes)

    return {
        "won": len(classes) == 0,
        "source_count": len(relations),
        "classes": classes,
        "unresolved_classes": [],
        "likely_over_classes": classes,
    }


def _product_cycle_class_key(self, factors, first, second):
    try:
        word_key = self.canonical_cyclic_factor_key(factors)
    except Exception:
        word_key = self.cyclic_factor_tuple_key(factors)

    first_span = _candidate_block_span(first)
    second_span = _candidate_block_span(second)
    first_key = _product_cycle_candidate_primitive_key(self, first)
    second_key = _product_cycle_candidate_primitive_key(self, second)
    pair = tuple(sorted(
        ((first_span, repr(first_key)), (second_span, repr(second_key))),
        key=repr,
    ))

    return (word_key, pair)


def generated_product_cycle_class_reports(
    self,
    product_factors=None,
    unresolved_only=False,
    record=True,
):
    """
    Detect non-Massey product cycles from overlapping primitive resolutions.

    If a cyclic product word has two concrete primitive resolutions whose
    touched blocks overlap, their contextual primitives form a new cycle even
    when the class is not an m_n generated by disjoint lower products.
    """

    seed_words = []
    seen_words = set()

    def remember_word(word):
        try:
            factors = self.canonical_mp_factors(tuple(word))
        except Exception:
            return

        if len(factors) < 2:
            return

        if not self.mp_factors_composable(factors, cyclic=True):
            return

        try:
            key = self.canonical_cyclic_factor_key(factors)
        except Exception:
            key = self.cyclic_factor_tuple_key(factors)

        key_repr = repr(key)

        if key_repr in seen_words:
            return

        seen_words.add(key_repr)
        seed_words.append(factors)

    for block in self.known_resolved_product_blocks():
        remember_word(block.get("factors", ()))

    if product_factors is not None:
        for word in tuple(product_factors or ()):
            if isinstance(word, (tuple, list)):
                remember_word(word)

    classes = []
    seen_classes = set()

    for factors in seed_words:
        candidates = [
            candidate
            for candidate in self.product_word_resolution_candidates(
                factors,
                verify=False,
                use_bridge_replacements=False,
            )
            if _product_cycle_candidate_is_direct(candidate)
        ]

        for first_index, first in enumerate(candidates):
            first_span = _candidate_block_span(first)

            if first_span is None:
                continue

            for second in candidates[first_index + 1:]:
                second_span = _candidate_block_span(second)

                if second_span is None:
                    continue

                if self.spans_are_disjoint(first_span, second_span):
                    continue

                if (
                    _product_cycle_candidate_primitive_key(self, first)
                    == _product_cycle_candidate_primitive_key(self, second)
                ):
                    continue

                class_key = _product_cycle_class_key(self, factors, first, second)
                key_repr = repr(class_key)

                if key_repr in seen_classes:
                    continue

                seen_classes.add(key_repr)
                classes.append({
                    "kind": "generated_product_cycle",
                    "factors": factors,
                    "length": len(factors),
                    "resolved": False,
                    "likely_over": False,
                    "candidates": (
                        _product_cycle_candidate_summary(self, first),
                        _product_cycle_candidate_summary(self, second),
                    ),
                    "spans": (first_span, second_span),
                })

    relation_cycle_result = self.replacement_relation_cycle_class_reports(
        record=record,
    )
    relation_cycles = tuple(
        relation_cycle_result.get("likely_over_classes", ()) or ()
    )

    if record:
        self.generated_product_cycle_classes = tuple(classes)

    return {
        "won": len(classes) == 0 and len(relation_cycles) == 0,
        "source_count": len(seed_words),
        "classes": [] if unresolved_only else classes + list(relation_cycles),
        "unresolved_classes": classes,
        "likely_over_classes": list(relation_cycles),
    }


def cyclic_product_class_report(self, P, verify=True):
    """
    Resolve a product-type cyclic class by checking all actual rotations.
    """

    try:
        factors = self.canonical_mp_factors(P)
    except Exception:
        factors = self.canonical_mp_factors((P,))

    rotations = self.cyclic_rotations(factors)
    rotation_records = []
    resolved_rotation_indices = []
    minimal_rotation_indices = []
    minimal_rotation_keys = set()
    minimal_resolution_sources = []

    for index, rotation in enumerate(rotations):
        composable = self.mp_factors_composable(rotation, cyclic=False)
        candidates = []

        if composable:
            candidates = self.product_word_resolution_candidates(
                rotation,
                verify=verify
            )

        resolved = len(candidates) > 0
        rotation_minimal_sources = _minimal_resolution_sources_for_rotation(
            self,
            index,
            rotation,
            candidates,
        )
        minimally_resolved = any(
            candidate.get("minimal", False)
            for candidate in candidates
        )

        if resolved:
            resolved_rotation_indices.append(index)

        if minimally_resolved:
            minimal_rotation_indices.append(index)
            minimal_rotation_keys.add(repr(self.cyclic_factor_tuple_key(rotation)))

        if rotation_minimal_sources:
            minimal_resolution_sources.extend(
                dict(source, word=factors)
                for source in rotation_minimal_sources
            )

        rotation_records.append({
            "index": index,
            "factors": rotation,
            "composable": composable,
            "resolved": resolved,
            "minimally_resolved": minimally_resolved,
            "candidates": candidates,
            "minimal_resolution_sources": rotation_minimal_sources,
        })

    compatibility = _product_resolution_compatibility_summary(
        self,
        minimal_resolution_sources,
    )
    direct_minimal_resolution_sources = tuple(
        source
        for source in minimal_resolution_sources
        if not _product_minimal_source_is_inherited(source)
    )
    direct_compatibility = _product_resolution_compatibility_summary(
        self,
        direct_minimal_resolution_sources,
    )
    direct_rotation_indices = []

    for source in direct_minimal_resolution_sources:
        try:
            rotation_index = int(source.get("rotation_index", -1))
        except Exception:
            continue

        if rotation_index >= 0:
            direct_rotation_indices.append(rotation_index)

    direct_minimal_rotation_indices = tuple(dict.fromkeys(direct_rotation_indices))
    chain_compatibility = _cyclic_resolution_chain_compatibility_summary(
        self,
        direct_minimal_resolution_sources,
        relations=(),
    )
    pair_tower_bridge_over_resolution = (
        _opposite_pair_tower_bridge_resolution_report(
            self,
            minimal_resolution_sources,
        )
    )
    likely_over = (
        (
            len(direct_minimal_rotation_indices) >= 2
            and direct_compatibility["resolution_group_count"] >= 2
            and chain_compatibility["noncompatible_resolution_pair_count"] >= 1
        )
        or pair_tower_bridge_over_resolution is not None
    )

    report = {
        "kind": "product_cyclic_class",
        "factors": factors,
        "rotations": rotation_records,
        "resolved": len(resolved_rotation_indices) > 0,
        "resolved_rotation_indices": tuple(resolved_rotation_indices),
        "minimal_rotation_indices": tuple(minimal_rotation_indices),
        "minimal_resolution_sources": tuple(minimal_resolution_sources),
        "direct_minimal_resolution_sources": direct_minimal_resolution_sources,
        "direct_minimal_rotation_indices": direct_minimal_rotation_indices,
        "direct_minimal_resolution_count": direct_compatibility["minimal_resolution_count"],
        "direct_minimal_resolution_block_count": direct_compatibility["minimal_resolution_block_count"],
        **compatibility,
        **chain_compatibility,
        "pair_tower_bridge_over_resolution": pair_tower_bridge_over_resolution,
        "likely_over": likely_over,
        "likely_over_reason": (
            pair_tower_bridge_over_resolution.get("reason")
            if pair_tower_bridge_over_resolution is not None
            else "cyclic class has non-compatible cyclic resolutions"
            if likely_over
            else ""
        ),
    }

    if compatibility["minimal_resolution_count"] >= 2:
        report["compatible_resolutions"] = bool(
            chain_compatibility["chain_compatible_resolutions"]
        )

    return report


def _add_known_block(self, blocks, seen, block, source):
    try:
        factors = self.canonical_mp_factors(tuple(block))
    except Exception:
        return

    if len(factors) == 0:
        return

    try:
        resolution = self.exact_product_block_resolution(factors, verify=True)
    except Exception:
        return

    if not resolution.get("resolved"):
        return

    key = self.cyclic_factor_tuple_key(factors)

    if key in seen:
        return

    seen.add(key)
    blocks.append({
        "factors": factors,
        "key": key,
        "source": source,
        "resolution": resolution,
    })


def _resolved_mp_key_product_blocks(self, key):
    key = self.normalize_mp_inputs(tuple(key))

    if len(key) >= 3:
        M = getattr(self, "massey_products", {}).get(key, None)

        if isinstance(M, MasseyProduct):
            if _mp_input_contains_product_value(M):
                return []

            return [(M,)]

    return [key]


def _completed_tower_terminal_product_blocks(self):
    """
    Virtual product blocks killed by a completed pointed Massey tower.

    For a completed tower based at the leave word (x, y, z, ...), the unresolved
    leave Massey factor squared is eliminated by the tower relation:
    m2(m3(x,y,z), m3(x,y,z)).  After flattening the two leave factors, the word
    xyzxyz is a periodic subword of ...xyzxyzxyz....  These are not new attached
    cells, so they are recorded as virtual resolved product blocks for the
    product automaton rather than as exact primitives.

    The bare terminal arrow square x*x is intentionally not recorded here.  It
    should only inherit the tower elimination when an actual bridge relation
    identifies x with the leave Massey product.
    """

    try:
        records = self.completed_massey_tower_elimination_records()
    except Exception:
        return []

    blocks = []
    seen = set()

    for record in records:
        seed_inputs = tuple(record.get("seed_inputs", ()))

        if len(seed_inputs) < 3:
            continue

        terminal_candidates = []
        seed_key = record.get("seed_key")
        seed_massey = getattr(self, "massey_products", {}).get(seed_key, None)

        if not isinstance(seed_massey, MasseyProduct) and seed_key:
            try:
                seed_massey = MasseyProduct(self, seed_key)
            except Exception:
                seed_massey = None

        if isinstance(seed_massey, MasseyProduct):
            terminal_candidates.append(seed_massey)

        terminal_candidates.extend(
            self.normalize_mp_input(alias)
            for alias in tuple(record.get("aliases", ()))
        )

        for terminal in terminal_candidates:
            try:
                factors = self.canonical_mp_factors((terminal, terminal))
            except Exception:
                continue

            if len(factors) != 2:
                continue

            if not self.mp_factors_composable(factors, cyclic=False):
                continue

            key = self.cyclic_factor_tuple_key(factors)

            if key in seen:
                continue

            seen.add(key)
            blocks.append({
                "factors": factors,
                "key": key,
                "source": "completed_massey_tower",
                "resolution": {
                    "resolved": True,
                    "virtual": True,
                    "source": "completed_massey_tower",
                    "record": record,
                    "terminal": terminal,
                },
            })

    return blocks


def _tower_record_seed_massey_factor(self, record):
    seed_key = record.get("seed_key")
    seed_inputs = tuple(record.get("seed_inputs", ()))
    seed_massey = getattr(self, "massey_products", {}).get(seed_key, None)

    if not isinstance(seed_massey, MasseyProduct) and seed_inputs:
        try:
            seed_massey = MasseyProduct(self, seed_inputs)
        except Exception:
            seed_massey = None

    return seed_massey if isinstance(seed_massey, MasseyProduct) else None


def _tower_record_terminal_factors(self, record):
    terminals = []
    seen = set()

    def remember(factor):
        try:
            factor = self.normalize_mp_input(factor)
            key = repr(self.mp_factor_key(factor))
        except Exception:
            return

        if key in seen:
            return

        seen.add(key)
        terminals.append(factor)

    seed_massey = _tower_record_seed_massey_factor(self, record)

    if seed_massey is not None:
        remember(seed_massey)

    for alias in tuple(record.get("aliases", ()) or ()):
        remember(alias)

    return tuple(terminals)


def _completed_pair_tower_terminal_product_blocks(self):
    try:
        pair_records = self.completed_massey_pair_tower_elimination_records()
    except Exception:
        return []

    blocks = []
    seen = set()

    for record in pair_records:
        left = _tower_record_seed_massey_factor(
            self,
            record.get("left_record", {}),
        )
        right = _tower_record_seed_massey_factor(
            self,
            record.get("right_record", {}),
        )

        if left is None or right is None:
            continue

        try:
            factors = self.canonical_mp_factors((left, right))
        except Exception:
            continue

        if len(factors) != 2:
            continue

        if not self.mp_factors_composable(factors, cyclic=False):
            continue

        key = self.cyclic_factor_tuple_key(factors)

        if key in seen:
            continue

        seen.add(key)
        blocks.append({
            "factors": factors,
            "key": key,
            "source": "completed_massey_pair_tower",
            "resolution": {
                "resolved": True,
                "virtual": True,
                "source": "completed_massey_pair_tower",
                "record": record,
                "left_terminal": left,
                "right_terminal": right,
            },
        })

    return blocks


def _pair_tower_flat_word_precompute_limit(self, pair_records):
    raw_limit = getattr(self, "lemma1_flattened_product_max_length", None)

    if raw_limit in ("infinity", "Infinity", "inf", "Inf"):
        return None

    if raw_limit is not None:
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError):
            limit = None

        if limit is not None and limit >= 2:
            return limit

    limit = 2

    for record in tuple(pair_records or ()):
        limit = max(
            limit,
            len(tuple(record.get("left_seed_inputs", ()) or ()))
            + len(tuple(record.get("right_seed_inputs", ()) or ())),
        )

    return limit


def _pair_tower_admissible_flat_words(self, record, max_flat_length):
    left_seed = tuple(record.get("left_seed_inputs", ()) or ())
    right_seed = tuple(record.get("right_seed_inputs", ()) or ())

    if len(left_seed) < 2 or len(right_seed) < 2:
        return ()

    if max_flat_length is None:
        max_flat_length = len(left_seed) + len(right_seed)

    try:
        max_flat_length = max(2, int(max_flat_length))
    except (TypeError, ValueError):
        max_flat_length = len(left_seed) + len(right_seed)

    words = []
    seen = set()

    for length in range(2, max_flat_length + 1):
        for split in range(1, length):
            left_part = tuple(
                left_seed[(len(left_seed) - split + index) % len(left_seed)]
                for index in range(split)
            )
            right_part = tuple(
                right_seed[index % len(right_seed)]
                for index in range(length - split)
            )
            flat_word = left_part + right_part

            if not (
                _tower_word_contains_subword(self, flat_word, left_seed)
                or _tower_word_contains_subword(self, flat_word, right_seed)
            ):
                continue

            try:
                if not _fast_key_is_composable(self, flat_word):
                    continue
            except Exception:
                continue

            key = repr(_tower_word_keys(self, flat_word))

            if key in seen:
                continue

            seen.add(key)
            words.append(flat_word)

    return tuple(words)


def _pair_tower_collapsed_factor_words(
    self,
    flat_word,
    collapse_specs,
    max_options=2048,
):
    flat_word = tuple(self.normalize_mp_inputs(tuple(flat_word)))
    collapse_specs = tuple(collapse_specs or ())
    options = []
    seen = set()

    try:
        max_options = max(1, int(max_options))
    except (TypeError, ValueError):
        max_options = 2048

    def remember(factors):
        try:
            canonical = self.canonical_mp_factors(tuple(factors))
        except Exception:
            return

        if len(canonical) < 2:
            return

        if not self.mp_factors_composable(canonical, cyclic=False):
            return

        try:
            key = repr(self.cyclic_factor_tuple_key(canonical))
        except Exception:
            key = repr(tuple(repr(factor) for factor in canonical))

        if key in seen:
            return

        seen.add(key)
        options.append(canonical)

    def walk(index, factors):
        if len(options) >= max_options:
            return

        if index >= len(flat_word):
            remember(factors)
            return

        for seed, terminals in collapse_specs:
            seed = tuple(seed)

            if (
                not seed
                or index + len(seed) > len(flat_word)
                or not self.mp_factors_equal(
                    flat_word[index:index + len(seed)],
                    seed,
                )
            ):
                continue

            for terminal in tuple(terminals or ()):
                walk(index + len(seed), factors + (terminal,))

                if len(options) >= max_options:
                    return

        walk(index + 1, factors + (flat_word[index],))

    walk(0, ())
    return tuple(options)


def _completed_pair_tower_collapsed_product_blocks(self):
    if not getattr(self, "enable_lemma1_collapsed_product_blocks", False):
        return []

    try:
        pair_records = self.completed_massey_pair_tower_elimination_records()
    except Exception:
        return []

    max_flat_length = _pair_tower_flat_word_precompute_limit(self, pair_records)
    raw_max_options = getattr(self, "lemma1_collapsed_word_max_options", 2048)
    raw_block_limit = getattr(self, "lemma1_collapsed_product_block_limit", 4096)

    try:
        block_limit = max(1, int(raw_block_limit))
    except (TypeError, ValueError):
        block_limit = 4096

    blocks = []
    seen = set()

    for record in tuple(pair_records or ()):
        left_record = record.get("left_record", {})
        right_record = record.get("right_record", {})
        left_seed = tuple(record.get("left_seed_inputs", ()) or ())
        right_seed = tuple(record.get("right_seed_inputs", ()) or ())
        collapse_specs = (
            (left_seed, _tower_record_terminal_factors(self, left_record)),
            (right_seed, _tower_record_terminal_factors(self, right_record)),
        )
        collapse_specs = tuple(
            (seed, terminals)
            for seed, terminals in collapse_specs
            if seed and terminals
        )

        for flat_word in _pair_tower_admissible_flat_words(
            self,
            record,
            max_flat_length,
        ):
            for factors in _pair_tower_collapsed_factor_words(
                self,
                flat_word,
                collapse_specs,
                max_options=raw_max_options,
            ):
                try:
                    key = self.cyclic_factor_tuple_key(factors)
                except Exception:
                    continue

                if key in seen:
                    continue

                seen.add(key)
                blocks.append({
                    "factors": factors,
                    "key": key,
                    "source": "completed_massey_pair_tower",
                    "resolution": {
                        "resolved": True,
                        "virtual": True,
                        "source": "completed_massey_pair_tower",
                        "record": record,
                        "flat_word": flat_word,
                        "collapsed_factors": factors,
                    },
                })

                if len(blocks) >= block_limit:
                    return blocks

    return blocks


def _bridge_replacement_product_blocks(self):
    """
    Finite bridge-implied product blocks whose whole word has a certificate.

    This records the bridge sides themselves.  Longer contextual products are
    still recognized by mp_block_has_primitive(), but are not enumerated here
    because there are infinitely many possible contexts.
    """

    blocks = []
    seen = set()
    candidate_words = []

    try:
        for relation in self.bridge_product_relations():
            candidate_words.append(tuple(relation.get("left", ())))
            candidate_words.append(tuple(relation.get("right", ())))
    except Exception:
        return blocks

    for word in candidate_words:
        try:
            factors = self.canonical_mp_factors(tuple(word))
        except Exception:
            continue

        if len(factors) < 2:
            continue

        key = self.cyclic_factor_tuple_key(factors)

        if key in seen:
            continue

        candidates = _bridge_replacement_product_resolution_candidates(
            self,
            factors,
            minimal_only=True,
        )
        candidate = next(
            (
                item
                for item in candidates
                if item.get("minimal")
                and _bridge_candidate_spans_whole_original(item, factors)
            ),
            None,
        )

        if candidate is None:
            continue

        seen.add(key)
        blocks.append({
            "factors": factors,
            "key": key,
            "source": "bridge_replacement",
            "resolution": {
                "resolved": True,
                "deferred_primitive": True,
                "source": "bridge_replacement",
                "candidate": candidate,
            },
        })

    return blocks


def known_resolved_product_blocks(self):
    """
    Return exact product blocks that are known to have genuine primitives.
    """

    _ensure_absorbing_higher_products(self)

    cache_key = (
        _tower_cache_state_signature(self),
        len(getattr(self, "massey_products", {})),
        tuple(sorted(
            repr(key)
            for key in getattr(self, "_absorbing_higher_product_resolved_keys", set())
        )),
        bool(getattr(self, "enable_lemma1_collapsed_product_blocks", False)),
        getattr(self, "lemma1_flattened_product_max_length", None),
        getattr(self, "lemma1_collapsed_word_max_options", None),
        getattr(self, "lemma1_collapsed_product_block_limit", None),
    )
    cache = getattr(self, "_known_resolved_product_blocks_cache", None)

    if cache is not None and cache.get("key") == cache_key:
        return list(cache.get("blocks", ()))

    blocks = []
    seen = set()

    for key in getattr(self, "resolved_massey_products", {}).keys():
        for block in _resolved_mp_key_product_blocks(self, key):
            _add_known_block(
                self,
                blocks,
                seen,
                block,
                "resolved_massey_product"
            )

    for entry in getattr(self, "attachment_history", []):
        expression = entry.get("expression", None)

        if isinstance(expression, MPProduct):
            _add_known_block(
                self,
                blocks,
                seen,
                expression.factors,
                entry.get("kind", "mp_product_cell")
            )

        elif isinstance(expression, MPElement) and len(expression.terms) == 1:
            product, coeff = next(iter(expression.terms.items()))

            if not is_zero_coeff(coeff):
                _add_known_block(
                    self,
                    blocks,
                    seen,
                    product.factors,
                    entry.get("kind", "mp_expression_cell")
                )

        elif isinstance(expression, MasseyProduct):
            for block in _resolved_mp_key_product_blocks(self, expression.inputs):
                _add_known_block(
                    self,
                    blocks,
                    seen,
                    block,
                    entry.get("kind", "mp_cell")
                )

        elif isinstance(expression, (Arrow, Path, Element)):
            product = self.path_to_mp_product(expression)

            if product is not None:
                _add_known_block(
                    self,
                    blocks,
                    seen,
                    product.factors,
                    entry.get("kind", "ordinary_cell")
                )

    for path_key in getattr(self, "cells", {}).keys():
        try:
            factors = tuple(
                self.mp(self.arrows[name])
                for name in path_key
            )
        except Exception:
            continue

        _add_known_block(self, blocks, seen, factors, "ordinary_cell")

    for block in _completed_tower_terminal_product_blocks(self):
        key = block["key"]

        if key in seen:
            continue

        seen.add(key)
        blocks.append(block)

    for block in _completed_pair_tower_terminal_product_blocks(self):
        key = block["key"]

        if key in seen:
            continue

        seen.add(key)
        blocks.append(block)

    for block in _completed_pair_tower_collapsed_product_blocks(self):
        key = block["key"]

        if key in seen:
            continue

        seen.add(key)
        blocks.append(block)

    for block in _bridge_replacement_product_blocks(self):
        key = block["key"]

        if key in seen:
            continue

        seen.add(key)
        blocks.append(block)

    for record in tuple(
        (getattr(self, "absorbing_higher_product_resolutions", {}) or {}).values()
    ):
        _add_known_block(
            self,
            blocks,
            seen,
            record.get("target_product_factors", ()),
            "absorbing_higher_product",
        )

    self._known_resolved_product_blocks_cache = {
        "key": cache_key,
        "blocks": tuple(blocks),
    }

    return blocks


def product_word_contains_forbidden_block(
    self,
    factors,
    forbidden_blocks=None,
    forbidden_keys=None,
    cyclic=False,
):
    factors = tuple(factors)

    if forbidden_keys is None:
        if forbidden_blocks is None:
            forbidden_blocks = [
                item["factors"]
                for item in self.known_resolved_product_blocks()
            ]

        forbidden_keys = [
            self.cyclic_factor_tuple_key(block)
            for block in forbidden_blocks
            if len(block) > 0
        ]

    factor_keys = self.cyclic_factor_tuple_key(factors)

    words = [factor_keys]

    if cyclic and factors:
        words = [
            self.cyclic_factor_tuple_key(rotation)
            for rotation in self.cyclic_rotations(factors)
        ]

    for word in words:
        for block in forbidden_keys:
            block_len = len(block)

            if block_len == 0 or block_len > len(word):
                continue

            for start in range(0, len(word) - block_len + 1):
                if word[start:start + block_len] == block:
                    return True

    return False


def bridge_product_relations(self):
    """
    Two-term MP bridge relations, usable as cyclic word replacements.
    """

    relations = []

    for entry in getattr(self, "attachment_history", []):
        expression = entry.get("expression", None)

        if not isinstance(expression, MPElement) or len(expression.terms) != 2:
            continue

        terms = []

        for product, coeff in expression.terms.items():
            if not isinstance(product, MPProduct):
                continue

            if _inverse_coeff(self, coeff) is None:
                continue

            try:
                factors = self.canonical_mp_factors(product.factors)
            except Exception:
                continue

            terms.append((factors, coeff))

        if len(terms) != 2:
            continue

        (left_factors, left_coeff), (right_factors, right_coeff) = terms

        if len(left_factors) != len(right_factors):
            continue

        relations.append({
            "left": left_factors,
            "right": right_factors,
            "left_coeff": left_coeff,
            "right_coeff": right_coeff,
            "cell": entry.get("cell"),
            "expression": expression,
        })

    return relations


def _valid_product_replacement_relation(self, left, right):
    if len(left) == 0 or len(right) == 0:
        return False

    if not self.mp_factors_composable(left, cyclic=False):
        return False

    if not self.mp_factors_composable(right, cyclic=False):
        return False

    return left[0].source == right[0].source and left[-1].target == right[-1].target


def _add_product_replacement_relation(self, relations, seen, left, right, data=None):
    try:
        left = self.canonical_mp_factors(tuple(left))
        right = self.canonical_mp_factors(tuple(right))
    except Exception:
        return

    if not _valid_product_replacement_relation(self, left, right):
        return

    left_key = self.cyclic_factor_tuple_key(left)
    right_key = self.cyclic_factor_tuple_key(right)

    if left_key == right_key:
        return

    directed = bool(data and data.get("directed"))

    if directed:
        pair_key = ("directed", repr(left_key), repr(right_key))
    else:
        pair_key = ("undirected",) + tuple(sorted((repr(left_key), repr(right_key))))

    if pair_key in seen:
        return

    seen.add(pair_key)
    record = {
        "left": left,
        "right": right,
        "left_key": left_key,
        "right_key": right_key,
        "directed": directed,
    }

    if data:
        record.update(data)

    relations.append(record)


def _replacement_factor_complexity(self, factor, seen=None):
    if seen is None:
        seen = set()

    marker = id(factor)

    if marker in seen:
        return 1

    seen.add(marker)

    if isinstance(factor, MPProduct):
        return sum(
            _replacement_factor_complexity(self, item, seen=seen)
            for item in tuple(factor.factors)
        )

    if isinstance(factor, MasseyProduct):
        inputs = tuple(getattr(factor, "inputs", ()))

        if len(inputs) == 1:
            return _replacement_factor_complexity(self, inputs[0], seen=seen)

        return 1 + sum(
            _replacement_factor_complexity(self, item, seen=seen)
            for item in inputs
        )

    return 1


def _replacement_factors_complexity(self, factors):
    return sum(
        _replacement_factor_complexity(self, factor)
        for factor in tuple(factors)
    )


def _recursive_replacement_factor_keys(self, factor, seen=None):
    if seen is None:
        seen = set()

    marker = id(factor)

    if marker in seen:
        return []

    seen.add(marker)

    keys = []

    try:
        normalized = self.normalize_mp_input(factor)
    except Exception:
        normalized = factor

    try:
        keys.append(self.mp_factor_key(normalized))
    except Exception:
        pass

    if isinstance(normalized, MPProduct):
        for item in tuple(normalized.factors):
            keys.extend(
                _recursive_replacement_factor_keys(self, item, seen=seen)
            )

    elif isinstance(normalized, MasseyProduct):
        for item in tuple(getattr(normalized, "inputs", ())):
            keys.extend(
                _recursive_replacement_factor_keys(self, item, seen=seen)
            )

    return keys


def _replacement_dependency_graph(self, edges):
    graph = {}

    for edge in tuple(edges or ()):
        if edge.get("replacement_type", "bridge") != "bridge":
            continue

        target_keys = _replacement_target_letter_key_reprs(
            self,
            edge.get("target_factors", ()),
        )
        replacement_keys = _replacement_top_level_key_reprs(
            self,
            edge.get("replacement_factors", ()),
        )

        for target_key in target_keys:
            graph.setdefault(target_key, set()).update(replacement_keys)

    return graph


def _replacement_dependency_reaches_any(graph, start_keys, target_keys):
    target_keys = frozenset(target_keys or ())

    if not target_keys:
        return False

    queue = list(start_keys or ())
    seen = set()

    while queue:
        key = queue.pop(0)

        if key in target_keys:
            return True

        if key in seen:
            continue

        seen.add(key)
        queue.extend(
            neighbor
            for neighbor in tuple(graph.get(key, ()) or ())
            if neighbor not in seen
        )

    return False


def _edge_has_top_level_dependency_loop(self, edge, dependency_graph):
    target_factors = tuple(edge.get("target_factors", ()) or ())
    replacement_factors = tuple(edge.get("replacement_factors", ()) or ())

    if not target_factors or not replacement_factors:
        return False

    target_complexity = _replacement_factors_complexity(self, target_factors)
    replacement_complexity = _replacement_factors_complexity(
        self,
        replacement_factors,
    )

    if replacement_complexity <= target_complexity:
        return False

    target_keys = _replacement_top_level_key_reprs(self, target_factors)
    replacement_keys = _replacement_top_level_key_reprs(
        self,
        replacement_factors,
    )

    return _replacement_dependency_reaches_any(
        dependency_graph or {},
        replacement_keys,
        target_keys,
    )


def _edge_is_self_expanding_replacement(self, edge, dependency_graph=None):
    if edge.get("self_expanding_replacement"):
        return True

    target_factors = tuple(edge.get("target_factors", ()) or ())
    replacement_factors = tuple(edge.get("replacement_factors", ()) or ())

    if not target_factors or not replacement_factors:
        return False

    target_complexity = _replacement_factors_complexity(self, target_factors)
    replacement_complexity = _replacement_factors_complexity(
        self,
        replacement_factors,
    )

    if replacement_complexity <= target_complexity:
        return False

    target_keys = []

    for factor in target_factors:
        try:
            normalized = self.normalize_mp_input(factor)
            target_keys.append(self.mp_factor_key(normalized))
        except Exception:
            return False

    replacement_keys = set()

    for factor in replacement_factors:
        replacement_keys.update(
            _recursive_replacement_factor_keys(self, factor)
        )

    directly_recursive = all(
        target_key in replacement_keys
        for target_key in target_keys
    )

    if directly_recursive:
        return True

    if dependency_graph is None:
        return False

    return _edge_has_top_level_dependency_loop(
        self,
        edge,
        dependency_graph,
    )


def _replacement_top_level_key_reprs(self, factors):
    key_reprs = set()

    for factor in tuple(factors or ()):
        try:
            normalized = self.normalize_mp_input(factor)
            key_reprs.add(repr(self.mp_factor_key(normalized)))
        except Exception:
            key_reprs.add(repr(factor))

    return frozenset(key_reprs)


def _replacement_target_letter_key_reprs(self, factors):
    factors = tuple(factors or ())

    if len(factors) != 1:
        return frozenset()

    return _replacement_top_level_key_reprs(self, factors)


def _replacement_edge_target_key_reprs(self, edge):
    keys = edge.get("target_recursive_key_reprs", None)

    if keys is not None:
        return frozenset(keys)

    return _replacement_target_letter_key_reprs(
        self,
        edge.get("target_factors", ()),
    )


def _replacement_edge_replacement_key_reprs(self, edge):
    keys = edge.get("replacement_recursive_key_reprs", None)

    if keys is not None:
        return frozenset(keys)

    return _replacement_top_level_key_reprs(
        self,
        edge.get("replacement_factors", ()),
    )


def _replacement_edge_reintroduces_replaced_key(self, edge, replaced_key_reprs):
    replaced_key_reprs = frozenset(replaced_key_reprs or ())

    if not replaced_key_reprs:
        return False

    return bool(
        _replacement_edge_replacement_key_reprs(self, edge)
        & replaced_key_reprs
    )


def _virtual_resolved_massey_keys(self):
    keys = []

    for key, primitive in getattr(self, "resolved_massey_products", {}).items():
        if _is_virtual_massey_primitive(primitive):
            keys.append(key)

    return tuple(keys)


def _call_base_replacement_edge_records(
    self,
    base,
    only_bridge_cell=None,
    excluded_bridge_cells=None,
    include_ainf=True,
):
    try:
        return list(base(
            self,
            only_bridge_cell=only_bridge_cell,
            excluded_bridge_cells=excluded_bridge_cells,
            include_ainf=include_ainf,
        ))
    except TypeError:
        try:
            return list(base(
                self,
                only_bridge_cell=only_bridge_cell,
                excluded_bridge_cells=excluded_bridge_cells,
            ))
        except TypeError:
            return list(base(self))


def _safe_ainf_edges_without_virtual_massey_sources(self, bridge_edges, virtual_keys):
    saved_massey_products = getattr(self, "massey_products", None)
    saved_resolved_massey_products = getattr(self, "resolved_massey_products", None)

    try:
        if isinstance(saved_massey_products, dict):
            self.massey_products = {
                key: value
                for key, value in saved_massey_products.items()
                if key not in virtual_keys
            }

        if isinstance(saved_resolved_massey_products, dict):
            self.resolved_massey_products = {
                key: value
                for key, value in saved_resolved_massey_products.items()
                if key not in virtual_keys
            }

        return []
    finally:
        if saved_massey_products is not None:
            self.massey_products = saved_massey_products

        if saved_resolved_massey_products is not None:
            self.resolved_massey_products = saved_resolved_massey_products


def _ainf_outer_arity_limit(self):
    raw_limit = getattr(self, "ainf_replacement_max_outer_arity", 3)

    if raw_limit is None:
        return None

    if isinstance(raw_limit, str):
        normalized = raw_limit.strip().lower()

        if normalized in {"infinity", "inf", "unbounded", "legacy", "full"}:
            return None

        if normalized in {"off", "disabled", "false"}:
            return 0

        raw_limit = normalized

    try:
        return max(0, int(raw_limit))
    except (TypeError, ValueError):
        return 3


def _ainf_outer_arity_allowed(self, outer_arity):
    limit = _ainf_outer_arity_limit(self)

    if limit is None:
        return True

    try:
        return int(outer_arity) <= limit
    except (TypeError, ValueError):
        return True


def _ainf_edge_outer_arity(edge):
    value = edge.get("ainf_outer_arity", None)

    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    replacement_type = edge.get("replacement_type", "bridge")

    if replacement_type == "bridge":
        return None

    target = tuple(edge.get("target_factors", ()) or ())
    replacement = tuple(edge.get("replacement_factors", ()) or ())

    if target or replacement:
        return max(len(target), len(replacement))

    return None


def _filter_ainf_edges_by_outer_arity(self, edges):
    limit = _ainf_outer_arity_limit(self)

    if limit is None:
        self.filtered_ainf_outer_arity_edges = []
        return list(edges)

    filtered = []
    skipped = []

    for edge in edges:
        replacement_type = edge.get("replacement_type", "bridge")
        outer_arity = _ainf_edge_outer_arity(edge)

        if (
            replacement_type != "bridge"
            and outer_arity is not None
            and outer_arity > limit
        ):
            skipped_edge = dict(edge)
            skipped_edge["filtered_reason"] = "ainf_outer_arity_limit"
            skipped_edge["ainf_outer_arity_limit"] = limit
            skipped.append(skipped_edge)
            continue

        filtered.append(edge)

    self.filtered_ainf_outer_arity_edges = skipped
    return filtered


def replacement_edge_records(
    self,
    only_bridge_cell=None,
    excluded_bridge_cells=None,
    include_ainf=True,
    filter_self_expanding=None,
):
    base = getattr(type(self), "_cyclic_base_replacement_edge_records", None)

    if base is None:
        return []

    if filter_self_expanding is None:
        filter_self_expanding = getattr(
            self,
            "filter_self_expanding_replacements",
            True,
        )

    cache_key = None

    if only_bridge_cell is None and not excluded_bridge_cells:
        cache_key = (
            bool(include_ainf),
            bool(filter_self_expanding),
            len(tuple(getattr(self, "attachment_history", ()))),
            len(getattr(self, "resolved_massey_products", {})),
            len(getattr(self, "resolved_mp_expressions", {})),
            getattr(self, "bridge_replacement_max_depth", None),
            getattr(self, "ainf_replacement_max_outer_arity", 3),
        )
        cache = getattr(self, "_replacement_edge_records_cache", {})

        if cache.get("key") == cache_key:
            self.filtered_self_expanding_replacement_edges = list(
                cache.get("skipped", ())
            )
            return list(cache.get("edges", ()))

    virtual_keys = _virtual_resolved_massey_keys(self)

    if include_ainf and only_bridge_cell is None and virtual_keys:
        edges = _call_base_replacement_edge_records(
            self,
            base,
            only_bridge_cell=only_bridge_cell,
            excluded_bridge_cells=excluded_bridge_cells,
            include_ainf=False,
        )
        edges.extend(
            _safe_ainf_edges_without_virtual_massey_sources(
                self,
                edges,
                virtual_keys,
            )
        )
    else:
        edges = _call_base_replacement_edge_records(
            self,
            base,
            only_bridge_cell=only_bridge_cell,
            excluded_bridge_cells=excluded_bridge_cells,
                include_ainf=include_ainf,
        )

    edges = [dict(edge) for edge in edges]
    edges = _filter_ainf_edges_by_outer_arity(self, edges)
    dependency_graph = _replacement_dependency_graph(self, edges)

    for edge in edges:
        edge["target_recursive_key_reprs"] = tuple(sorted(
            _replacement_target_letter_key_reprs(
                self,
                edge.get("target_factors", ()),
            )
        ))
        edge["replacement_recursive_key_reprs"] = tuple(sorted(
            _replacement_top_level_key_reprs(
                self,
                edge.get("replacement_factors", ()),
            )
        ))

        if (
            edge.get("replacement_type", "bridge") == "bridge"
            and _edge_is_self_expanding_replacement(
                self,
                edge,
                dependency_graph=dependency_graph,
            )
        ):
            edge["self_expanding_replacement"] = True
            edge["guarded_self_expanding"] = True

    if not filter_self_expanding:
        if cache_key is not None:
            self._replacement_edge_records_cache = {
                "key": cache_key,
                "edges": tuple(edges),
                "skipped": (),
            }
        return edges

    filtered = []
    skipped = []

    for edge in edges:
        if (
            edge.get("replacement_type", "bridge") == "bridge"
            and edge.get("self_expanding_replacement")
        ):
            skipped_edge = dict(edge)
            skipped_edge["filtered_reason"] = "self_expanding_replacement"
            skipped.append(skipped_edge)
            continue

        filtered.append(edge)

    self.filtered_self_expanding_replacement_edges = skipped

    if cache_key is not None:
        self._replacement_edge_records_cache = {
            "key": cache_key,
            "edges": tuple(filtered),
            "skipped": tuple(skipped),
        }

    return filtered


def _stasheff_simplify_coeff(value):
    try:
        return simplify_coeff(value)
    except Exception:
        return value


def _stasheff_coeff_is_zero(value):
    try:
        return is_zero_coeff(value)
    except Exception:
        return value == 0


def _stasheff_known_massey_index(self):
    items = []

    try:
        items.extend(getattr(self, "massey_products", {}).values())
    except Exception:
        pass

    try:
        items.extend(getattr(self, "generated_massey_products", ()) or ())
    except Exception:
        pass

    index = {}

    for item in items:
        if not isinstance(item, MasseyProduct):
            continue

        inputs = tuple(self.normalize_mp_inputs(tuple(item.inputs)))

        if len(inputs) < 3:
            continue

        try:
            key = self.mp_key(*inputs)
        except Exception:
            continue

        index[key] = item

    return index


def _stasheff_iter_outer_massey_products(self):
    seen = set()

    for item in tuple(_stasheff_known_massey_index(self).values()):
        if not isinstance(item, MasseyProduct):
            continue

        inputs = tuple(getattr(item, "inputs", ()) or ())

        if len(inputs) < 3:
            continue

        if not any(
            isinstance(factor, MasseyProduct)
            and len(tuple(getattr(factor, "inputs", ()) or ())) >= 2
            for factor in inputs
        ):
            continue

        try:
            key = self.mp_key(*self.normalize_mp_inputs(inputs))
        except Exception:
            key = item.key()

        if key in seen:
            continue

        seen.add(key)
        yield item


def _stasheff_block_has_zero_value(self, block):
    block = tuple(self.normalize_mp_inputs(tuple(block)))

    if len(block) < 2:
        return False

    try:
        cache_key = (
            tuple(repr(self.mp_factor_key(factor)) for factor in block),
            len(tuple(getattr(self, "attachment_history", ()) or ())),
            len(getattr(self, "resolved_massey_products", {}) or {}),
            len(getattr(self, "resolved_mp_expressions", {}) or {}),
            len(getattr(self, "massey_products", {}) or {}),
            len(tuple(getattr(self, "generated_massey_products", ()) or ())),
            getattr(self, "ainf_replacement_max_outer_arity", 3),
            _tower_cache_state_signature(self),
        )
    except Exception:
        cache_key = None

    cache = getattr(self, "_stasheff_zero_value_cache", None)

    if cache is None:
        cache = {}
        self._stasheff_zero_value_cache = cache

    if cache_key is not None and cache_key in cache:
        return cache[cache_key]

    had_guard = hasattr(self, "_suppress_tower_alias_stasheff_zero")
    old_guard = getattr(self, "_suppress_tower_alias_stasheff_zero", False)
    self._suppress_tower_alias_stasheff_zero = True

    try:
        try:
            value = bool(self.mp_block_has_primitive(
                block,
                allow_bridge_replacements=False,
            ))
        except TypeError:
            try:
                value = bool(self.mp_block_has_primitive(block))
            except Exception:
                value = False
        except Exception:
            value = False
    finally:
        if had_guard:
            self._suppress_tower_alias_stasheff_zero = old_guard
        elif hasattr(self, "_suppress_tower_alias_stasheff_zero"):
            delattr(self, "_suppress_tower_alias_stasheff_zero")

    if cache_key is not None:
        cache[cache_key] = value

    return value


def _stasheff_get_or_create_mp(self, massey_index, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return None

    try:
        key = self.mp_key(*inputs)
    except Exception:
        return None

    existing = massey_index.get(key)

    if isinstance(existing, MasseyProduct):
        return existing

    try:
        if not self.can_define_mp(*inputs):
            return None
    except Exception:
        return None

    factory = getattr(self, "virtual_mp", None)

    try:
        if callable(factory):
            created = factory(*inputs, record=True)
        else:
            created = self.mp(*inputs)
    except Exception:
        return None

    if isinstance(created, MasseyProduct):
        massey_index[key] = created
        return created

    return None


def _stasheff_product_term_factors(self, inputs):
    try:
        factors = self.canonical_mp_factors(tuple(inputs))
    except Exception:
        return None

    if not factors or not self.mp_factors_composable(factors, cyclic=False):
        return None

    try:
        resolution = self.exact_product_block_resolution(factors, verify=False)
    except Exception:
        resolution = None

    if isinstance(resolution, dict) and resolution.get("resolved"):
        return None

    return tuple(factors)


def _stasheff_insertion_coefficient(self, inputs, start, stop):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    n = len(inputs)

    if start <= 0 and stop >= n:
        return Sign.one()

    try:
        if start <= 0:
            return _stasheff_simplify_coeff(
                self.mp_split_coefficient_for_inputs(inputs, stop)
            )

        prefix_coeff = self.mp_split_coefficient_for_inputs(inputs, start)
        suffix_coeff = _stasheff_insertion_coefficient(
            self,
            inputs[start:],
            0,
            stop - start,
        )
        return _stasheff_simplify_coeff(prefix_coeff * suffix_coeff)
    except Exception:
        return Sign.one()


def _stasheff_inner_operation_for_interval(
    self,
    letters,
    start,
    stop,
    massey_index,
):
    block = tuple(self.normalize_mp_inputs(tuple(letters[start:stop])))
    arity = len(block)

    if arity < 2:
        return None

    forced_inner_operations = getattr(
        self,
        "_stasheff_forced_inner_operations",
        None,
    )

    if isinstance(forced_inner_operations, dict):
        forced_operation = forced_inner_operations.get((start, stop))

        if forced_operation is not None:
            return forced_operation

    if _stasheff_block_has_zero_value(self, block):
        return None

    if arity == 2:
        try:
            if not self.are_composable(block[0], block[1]):
                return None
        except Exception:
            return None

        factors = _stasheff_product_term_factors(self, block)

        if factors is None:
            return None

        return MPProduct(self, factors)

    return _stasheff_get_or_create_mp(self, massey_index, block)


def _stasheff_term_for_interval(
    self,
    letters,
    start,
    stop,
    massey_index,
):
    n = len(letters)

    if start == 0 and stop == n:
        return None

    inner_operation = _stasheff_inner_operation_for_interval(
        self,
        letters,
        start,
        stop,
        massey_index,
    )

    if inner_operation is None:
        return None

    outer_inputs = (
        tuple(letters[:start])
        + (inner_operation,)
        + tuple(letters[stop:])
    )
    outer_arity = len(outer_inputs)

    if outer_arity < 2:
        return None

    if not _ainf_outer_arity_allowed(self, outer_arity):
        return {
            "blocked_by_outer_arity": True,
            "outer_arity": outer_arity,
            "span": (start, stop),
            "inner_operation": inner_operation,
        }

    if outer_arity == 2:
        factors = _stasheff_product_term_factors(self, outer_inputs)

        if factors is None:
            return None
    else:
        if _stasheff_block_has_zero_value(self, outer_inputs):
            return None

        outer_operation = _stasheff_get_or_create_mp(
            self,
            massey_index,
            outer_inputs,
        )

        if outer_operation is None:
            return None

        factors = (outer_operation,)

    return {
        "factors": tuple(factors),
        "coefficient": _stasheff_insertion_coefficient(
            self,
            letters,
            start,
            stop,
        ),
        "span": (start, stop),
        "inner_arity": stop - start,
        "outer_arity": outer_arity,
        "inner_operation": inner_operation,
        "outer_inputs": tuple(outer_inputs),
    }


def _stasheff_live_terms_for_letters(self, letters, massey_index):
    letters = tuple(self.normalize_mp_inputs(tuple(letters)))
    n = len(letters)
    terms = []
    blocked = []
    active_intervals = []

    for left in range(0, max(0, n - 1)):
        shadow_stop = max(
            (
                stop
                for start, stop in active_intervals
                if start < left < stop
            ),
            default=left + 1,
        )
        first_stop = max(left + 2, shadow_stop + 1)

        for stop in range(first_stop, n + 1):
            term = _stasheff_term_for_interval(
                self,
                letters,
                left,
                stop,
                massey_index,
            )

            if term is None:
                continue

            if term.get("blocked_by_outer_arity"):
                blocked.append(term)
                break

            terms.append(term)
            active_intervals.append((left, stop))
            break

    return terms, blocked


def _stasheff_combine_terms(self, terms):
    combined = {}

    for term in tuple(terms):
        factors = tuple(term.get("factors", ()) or ())

        if not factors:
            continue

        try:
            key = self.mp_factor_tuple_key(factors)
        except Exception:
            key = tuple(repr(factor) for factor in factors)

        if key not in combined:
            combined[key] = dict(term)
            continue

        old_coeff = combined[key].get("coefficient", Sign.one())
        new_coeff = term.get("coefficient", Sign.one())
        coeff = _stasheff_simplify_coeff(old_coeff + new_coeff)

        if _stasheff_coeff_is_zero(coeff):
            del combined[key]
        else:
            combined[key]["coefficient"] = coeff

    return tuple(combined.values())


def _stasheff_factor_presentation_key(self, factor):
    factor = self.normalize_mp_input(factor)

    if isinstance(factor, MasseyProduct):
        return (
            "MasseyProduct",
            tuple(
                _stasheff_factor_presentation_key(self, item)
                for item in tuple(getattr(factor, "inputs", ()) or ())
            ),
        )

    if isinstance(factor, MPProduct):
        try:
            factors = tuple(self.canonical_mp_factors(factor))
        except Exception:
            factors = tuple(getattr(factor, "factors", ()) or ())

        return (
            "MPProduct",
            tuple(
                _stasheff_factor_presentation_key(self, item)
                for item in factors
            ),
        )

    return self.mp_factor_key(factor)


def _stasheff_zero_massey_presentation_report(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return None

    if not any(
        isinstance(factor, MasseyProduct)
        and len(tuple(getattr(factor, "inputs", ()) or ())) >= 2
        for factor in inputs
    ):
        return None

    try:
        target_key = tuple(
            _stasheff_factor_presentation_key(self, item)
            for item in inputs
        )
    except Exception:
        return None

    massey_index = _stasheff_known_massey_index(self)

    for nested_index, nested_factor in enumerate(inputs):
        if not isinstance(nested_factor, MasseyProduct):
            continue

        nested_inputs = tuple(self.normalize_mp_inputs(
            tuple(getattr(nested_factor, "inputs", ()) or ())
        ))

        if len(nested_inputs) < 2:
            continue

        flat_letters = (
            inputs[:nested_index]
            + nested_inputs
            + inputs[nested_index + 1:]
        )
        had_guard = hasattr(self, "_suppress_tower_alias_stasheff_zero")
        old_guard = getattr(self, "_suppress_tower_alias_stasheff_zero", False)
        had_allowed_arity = hasattr(
            self,
            "_tower_alias_stasheff_zero_allowed_below_arity",
        )
        old_allowed_arity = getattr(
            self,
            "_tower_alias_stasheff_zero_allowed_below_arity",
            None,
        )
        had_suppress_expansion = hasattr(self, "_suppress_primitive_expansion")
        old_suppress_expansion = getattr(self, "_suppress_primitive_expansion", False)
        had_forced_inner = hasattr(self, "_stasheff_forced_inner_operations")
        old_forced_inner = getattr(self, "_stasheff_forced_inner_operations", None)
        self._suppress_tower_alias_stasheff_zero = True
        allowed_arity = len(inputs)

        if old_allowed_arity is not None:
            try:
                allowed_arity = min(int(old_allowed_arity), allowed_arity)
            except (TypeError, ValueError):
                pass

        self._tower_alias_stasheff_zero_allowed_below_arity = allowed_arity
        self._suppress_primitive_expansion = True
        forced_inner = {}

        if isinstance(old_forced_inner, dict):
            forced_inner.update(old_forced_inner)

        forced_inner[
            (nested_index, nested_index + len(nested_inputs))
        ] = nested_factor
        self._stasheff_forced_inner_operations = forced_inner

        try:
            terms, blocked = _stasheff_live_terms_for_letters(
                self,
                flat_letters,
                massey_index,
            )
        finally:
            if had_guard:
                self._suppress_tower_alias_stasheff_zero = old_guard
            elif hasattr(self, "_suppress_tower_alias_stasheff_zero"):
                delattr(self, "_suppress_tower_alias_stasheff_zero")

            if had_allowed_arity:
                self._tower_alias_stasheff_zero_allowed_below_arity = old_allowed_arity
            elif hasattr(self, "_tower_alias_stasheff_zero_allowed_below_arity"):
                delattr(self, "_tower_alias_stasheff_zero_allowed_below_arity")

            if had_suppress_expansion:
                self._suppress_primitive_expansion = old_suppress_expansion
            elif hasattr(self, "_suppress_primitive_expansion"):
                delattr(self, "_suppress_primitive_expansion")

            if had_forced_inner:
                self._stasheff_forced_inner_operations = old_forced_inner
            elif hasattr(self, "_stasheff_forced_inner_operations"):
                delattr(self, "_stasheff_forced_inner_operations")

        if blocked:
            continue

        terms = _stasheff_combine_terms(self, terms)

        if len(terms) != 1:
            continue

        term = terms[0]
        term_factors = tuple(term.get("factors", ()) or ())

        if len(term_factors) != 1:
            continue

        term_factor = term_factors[0]

        if not isinstance(term_factor, MasseyProduct):
            continue

        try:
            term_key = tuple(
                _stasheff_factor_presentation_key(self, item)
                for item in tuple(self.normalize_mp_inputs(
                    tuple(term_factor.inputs)
                ))
            )
        except Exception:
            continue

        if term_key != target_key:
            continue

        return {
            "resolved": True,
            "source": "stasheff_zero_massey_presentation",
            "virtual_primitive": True,
            "virtual_zero": True,
            "inputs": inputs,
            "flattened_inputs": flat_letters,
            "flattened_factor_index": nested_index,
            "flattened_factor": nested_factor,
            "flattened_factor_inputs": nested_inputs,
            "term": term,
            "coefficient": term.get("coefficient", Sign.one()),
            "stasheff_terms": tuple(
                _stasheff_term_summary(self, item)
                for item in terms
            ),
        }

    return None


def _stasheff_relation_replacement_coeff(self, left_coeff, right_coeff):
    numerator = _stasheff_simplify_coeff(-right_coeff)

    quotient = None

    try:
        quotient = self.coeff_quotient_if_possible(numerator, left_coeff)
    except Exception:
        quotient = None

    if quotient is not None:
        return quotient

    try:
        return _stasheff_simplify_coeff(numerator / left_coeff)
    except Exception:
        return None


def _stasheff_term_summary(self, term):
    return {
        "factors": tuple(term.get("factors", ()) or ()),
        "coefficient": term.get("coefficient", Sign.one()),
        "span": tuple(term.get("span", ()) or ()),
        "inner_arity": term.get("inner_arity"),
        "outer_arity": term.get("outer_arity"),
        "outer_inputs": tuple(term.get("outer_inputs", ()) or ()),
    }


def _stasheff_product_zero_cache_key(self, factors):
    try:
        factor_key = tuple(repr(self.mp_factor_key(factor)) for factor in factors)
    except Exception:
        return None

    try:
        state_key = (
            len(tuple(getattr(self, "attachment_history", ()) or ())),
            len(getattr(self, "resolved_massey_products", {}) or {}),
            len(getattr(self, "resolved_mp_expressions", {}) or {}),
            len(getattr(self, "massey_products", {}) or {}),
            len(tuple(getattr(self, "generated_massey_products", ()) or ())),
            getattr(self, "ainf_replacement_max_outer_arity", 3),
            _tower_cache_state_signature(self),
        )
    except Exception:
        state_key = None

    return (factor_key, state_key)


def _stasheff_zero_product_resolution_candidates(self, factors):
    if _ainf_outer_arity_limit(self) == 0:
        return []

    if not _ainf_outer_arity_allowed(self, 2):
        return []

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return []

    if len(factors) < 2:
        return []

    if not self.mp_factors_composable(factors, cyclic=False):
        return []

    if not any(
        isinstance(factor, MasseyProduct)
        and len(tuple(getattr(factor, "inputs", ()) or ())) >= 2
        for factor in factors
    ):
        return []

    cache_key = _stasheff_product_zero_cache_key(self, factors)
    cache = getattr(self, "_stasheff_product_zero_resolution_cache", None)

    if cache is None:
        cache = {}
        self._stasheff_product_zero_resolution_cache = cache

    if cache_key is not None and cache_key in cache:
        return [dict(candidate) for candidate in cache[cache_key]]

    try:
        original_key = self.mp_factor_tuple_key(factors)
    except Exception:
        original_key = tuple(repr(factor) for factor in factors)

    massey_index = _stasheff_known_massey_index(self)
    out = []
    seen = set()

    for factor_index, factor in enumerate(factors):
        if not isinstance(factor, MasseyProduct):
            continue

        nested_inputs = tuple(self.normalize_mp_inputs(
            tuple(getattr(factor, "inputs", ()) or ())
        ))

        if len(nested_inputs) < 2:
            continue

        flat_letters = (
            tuple(factors[:factor_index])
            + nested_inputs
            + tuple(factors[factor_index + 1:])
        )
        terms, blocked = _stasheff_live_terms_for_letters(
            self,
            flat_letters,
            massey_index,
        )

        if blocked:
            continue

        terms = _stasheff_combine_terms(self, terms)

        if len(terms) != 1:
            continue

        term = terms[0]
        term_factors = tuple(term.get("factors", ()) or ())

        if not term_factors:
            continue

        try:
            term_key = self.mp_factor_tuple_key(term_factors)
        except Exception:
            term_key = tuple(repr(item) for item in term_factors)

        if term_key != original_key:
            continue

        candidate_key = (
            repr(original_key),
            tuple(self.mp_factor_key(letter) for letter in flat_letters),
        )

        if candidate_key in seen:
            continue

        seen.add(candidate_key)
        coefficient = term.get("coefficient", Sign.one())
        out.append({
            "kind": "stasheff_zero",
            "source": "stasheff_zero",
            "virtual_primitive": True,
            "virtual_zero": True,
            "left": (),
            "block": factors,
            "right": (),
            "block_span": (0, len(factors)),
            "minimal": True,
            "sign_source": (),
            "verified": True,
            "ainf_resolved": True,
            "ainf_outer_arity": 2,
            "coefficient": coefficient,
            "term_coefficient": coefficient,
            "flattened_inputs": tuple(flat_letters),
            "flattened_factor_index": factor_index,
            "flattened_factor": factor,
            "flattened_factor_inputs": nested_inputs,
            "stasheff_terms": tuple(
                _stasheff_term_summary(self, item)
                for item in terms
            ),
            "profile_contexts": ({
                "context": "original",
                "context_factors": factors,
                "context_key": ("original", original_key),
                "span": (0, len(factors)),
                "block": factors,
                "prefix_length": 0,
            },),
        })

        break

    if cache_key is not None:
        cache[cache_key] = tuple(dict(candidate) for candidate in out)

    return out


def _stasheff_ainf_replacement_relations(self):
    if _ainf_outer_arity_limit(self) == 0:
        return []

    massey_index = _stasheff_known_massey_index(self)
    relations = []
    seen = set()

    for outer_massey in tuple(_stasheff_iter_outer_massey_products(self)):
        outer_inputs = tuple(self.normalize_mp_inputs(tuple(outer_massey.inputs)))

        if _stasheff_block_has_zero_value(self, outer_inputs):
            continue

        for nested_index, nested_input in enumerate(outer_inputs):
            if not isinstance(nested_input, MasseyProduct):
                continue

            nested_inputs = tuple(self.normalize_mp_inputs(tuple(nested_input.inputs)))

            if len(nested_inputs) < 2:
                continue

            flat_letters = (
                outer_inputs[:nested_index]
                + nested_inputs
                + outer_inputs[nested_index + 1:]
            )
            terms, blocked = _stasheff_live_terms_for_letters(
                self,
                flat_letters,
                massey_index,
            )

            if blocked:
                continue

            terms = _stasheff_combine_terms(self, terms)

            if len(terms) != 2:
                continue

            left, right = terms
            left_factors = tuple(left["factors"])
            right_factors = tuple(right["factors"])

            try:
                left_key = self.mp_factor_tuple_key(left_factors)
                right_key = self.mp_factor_tuple_key(right_factors)
            except Exception:
                continue

            if left_key == right_key:
                continue

            relation_key = (
                "stasheff_ainf",
                tuple(sorted((repr(left_key), repr(right_key)))),
                tuple(self.mp_factor_key(letter) for letter in flat_letters),
            )

            if relation_key in seen:
                continue

            seen.add(relation_key)
            left_coeff = left.get("coefficient", Sign.one())
            right_coeff = right.get("coefficient", Sign.one())
            relation_coeff = _stasheff_relation_replacement_coeff(
                self,
                left_coeff,
                right_coeff,
            )
            relations.append({
                "replacement_type": "ainf",
                "ainf_kind": "stasheff",
                "virtual_stasheff": True,
                "left": left_factors,
                "right": right_factors,
                "left_key": left_key,
                "right_key": right_key,
                "left_coeff": left_coeff,
                "right_coeff": right_coeff,
                "relation_replacement_coeff": relation_coeff,
                "ainf_inputs": tuple(flat_letters),
                "ainf_outer_arity": max(
                    int(left.get("outer_arity", 0) or 0),
                    int(right.get("outer_arity", 0) or 0),
                ),
                "stasheff_terms": tuple(
                    _stasheff_term_summary(self, term)
                    for term in terms
                ),
                "stasheff_nested_index": nested_index,
                "stasheff_nested_inputs": nested_inputs,
            })

    return relations


def product_replacement_relations(
    self,
    include_bridge=True,
    include_ainf=True,
):
    """
    Product replacements used by cyclic quotient searches.

    Bridge cells give relations such as A ~ B.  When the notebook also exposes
    replacement_edge_records(), we additionally import its bridge, A_inf, and
    compatible A_inf-bridge edges.  Replacements may change product length, but
    both sides must be composable products with matching endpoints.
    """

    try:
        cache_key = (
            bool(include_bridge),
            bool(include_ainf),
            len(tuple(getattr(self, "attachment_history", ()))),
            len(getattr(self, "resolved_massey_products", {})),
            len(getattr(self, "resolved_mp_expressions", {})),
            len(getattr(self, "massey_products", {})),
            len(getattr(self, "generated_massey_products", ()) or ()),
            getattr(self, "bridge_replacement_max_depth", None),
            getattr(self, "ainf_replacement_max_outer_arity", 3),
            bool(getattr(self, "filter_self_expanding_replacements", True)),
        )
        cache = getattr(self, "_product_replacement_relations_cache", {})

        if cache.get("key") == cache_key:
            return list(cache.get("relations", ()))
    except Exception:
        cache_key = None

    relations = []
    seen = set()

    if include_bridge:
        for relation in self.bridge_product_relations():
            replacement_type = relation.get("replacement_type", "bridge")
            left_to_right = {
                "target_factors": relation["left"],
                "replacement_factors": relation["right"],
                "replacement_type": replacement_type,
            }
            right_to_left = {
                "target_factors": relation["right"],
                "replacement_factors": relation["left"],
                "replacement_type": replacement_type,
            }

            if (
                replacement_type == "bridge"
                and (
                    _edge_is_self_expanding_replacement(self, left_to_right)
                    or _edge_is_self_expanding_replacement(self, right_to_left)
                )
            ):
                continue

            _add_product_replacement_relation(
                self,
                relations,
                seen,
                relation["left"],
                relation["right"],
                {
                    "replacement_type": replacement_type,
                    "left_coeff": relation.get("left_coeff"),
                    "right_coeff": relation.get("right_coeff"),
                    "cell": relation.get("cell"),
                    "expression": relation.get("expression"),
                    "source_relation": relation,
                }
            )

    edge_records = []

    if hasattr(self, "replacement_edge_records"):
        try:
            edge_records = self.replacement_edge_records(include_ainf=include_ainf)
        except TypeError:
            try:
                edge_records = self.replacement_edge_records()
            except Exception:
                edge_records = []
        except Exception:
            edge_records = []

    for edge in edge_records:
        replacement_type = edge.get("replacement_type", "bridge")

        if replacement_type == "bridge" and not include_bridge:
            continue

        if replacement_type != "bridge" and not include_ainf:
            continue

        target = edge.get("target_factors", None)
        replacement = edge.get("replacement_factors", None)

        if target is None or replacement is None:
            continue

        _add_product_replacement_relation(
            self,
            relations,
            seen,
            target,
            replacement,
            {
                "replacement_type": replacement_type,
                "directed": replacement_type == "bridge",
                "cell": edge.get("bridge_cell"),
                "expression": edge.get("bridge_expression"),
                "edge": edge,
            }
        )

    if include_ainf:
        for relation in _stasheff_ainf_replacement_relations(self):
            _add_product_replacement_relation(
                self,
                relations,
                seen,
                relation["left"],
                relation["right"],
                relation,
            )

    if cache_key is not None:
        self._product_replacement_relations_cache = {
            "key": cache_key,
            "relations": tuple(relations),
        }

    return relations


def mp_presentation_replacement_relations(
    self,
    include_bridge=True,
    include_ainf=True,
    include_self_expanding=True,
):
    """
    Replacement relations for equality of MP presentations.

    Cyclic product searches deliberately filter self-expanding bridges such as
    f -> m3(f,x,y).  Presentation equality needs the same bridge as an
    equality, because the reverse move m3(f,x,y) -> f identifies a newly
    created nested presentation with an old one.  The bounded BFS using these
    relations supplies the guard against runaway expansion.
    """

    try:
        cache_key = (
            bool(include_bridge),
            bool(include_ainf),
            bool(include_self_expanding),
            len(tuple(getattr(self, "attachment_history", ()))),
            tuple(sorted(
                repr(key)
                for key in getattr(self, "resolved_massey_products", {}).keys()
            )),
            tuple(sorted(
                repr(key)
                for key in getattr(self, "resolved_mp_expressions", {}).keys()
            )),
            len(getattr(self, "massey_products", {})),
            len(getattr(self, "generated_massey_products", ()) or ()),
            getattr(self, "bridge_replacement_max_depth", None),
            getattr(self, "ainf_replacement_max_outer_arity", 3),
        )
        cache = getattr(self, "_mp_presentation_replacement_relations_cache", {})

        if cache.get("key") == cache_key:
            return list(cache.get("relations", ()))
    except Exception:
        cache_key = None

    relations = []
    seen = set()

    if include_bridge:
        try:
            bridge_relations = self.bridge_product_relations()
        except Exception:
            bridge_relations = ()

        for relation in tuple(bridge_relations or ()):
            _add_product_replacement_relation(
                self,
                relations,
                seen,
                relation.get("left", ()),
                relation.get("right", ()),
                {
                    "replacement_type": relation.get("replacement_type", "bridge"),
                    "left_coeff": relation.get("left_coeff"),
                    "right_coeff": relation.get("right_coeff"),
                    "cell": relation.get("cell"),
                    "expression": relation.get("expression"),
                    "source_relation": relation,
                },
            )

    edge_records = []

    if hasattr(self, "replacement_edge_records"):
        try:
            edge_records = self.replacement_edge_records(
                include_ainf=include_ainf,
                filter_self_expanding=not include_self_expanding,
            )
        except TypeError:
            try:
                edge_records = self.replacement_edge_records(
                    include_ainf=include_ainf,
                )
            except TypeError:
                try:
                    edge_records = self.replacement_edge_records()
                except Exception:
                    edge_records = []
            except Exception:
                edge_records = []
        except Exception:
            edge_records = []

    for edge in tuple(edge_records or ()):
        replacement_type = edge.get("replacement_type", "bridge")

        if replacement_type == "bridge" and not include_bridge:
            continue

        if replacement_type != "bridge" and not include_ainf:
            continue

        target = edge.get("target_factors", None)
        replacement = edge.get("replacement_factors", None)

        if target is None or replacement is None:
            continue

        _add_product_replacement_relation(
            self,
            relations,
            seen,
            target,
            replacement,
            {
                "replacement_type": replacement_type,
                "cell": edge.get("bridge_cell"),
                "expression": edge.get("bridge_expression"),
                "edge": edge,
            },
        )

    if include_ainf:
        for relation in _stasheff_ainf_replacement_relations(self):
            _add_product_replacement_relation(
                self,
                relations,
                seen,
                relation["left"],
                relation["right"],
                relation,
            )

    if cache_key is not None:
        self._mp_presentation_replacement_relations_cache = {
            "key": cache_key,
            "relations": tuple(relations),
        }

    return relations


def linear_replacement_neighbors(self, factors, relations=None):
    factors = tuple(factors)

    if relations is None:
        relations = self.product_replacement_relations()

    if not factors:
        return []

    neighbors = []
    seen = set()
    n = len(factors)

    def add_neighbor(word):
        word = tuple(word)

        if word and not self.mp_factors_composable(word, cyclic=False):
            return

        key = self.cyclic_factor_tuple_key(word)

        if key in seen:
            return

        seen.add(key)
        neighbors.append(word)

    for relation in relations:
        directions = (
            (("left", "right"),)
            if relation.get("directed")
            else (("left", "right"), ("right", "left"))
        )

        for source_name, target_name in directions:
            source = tuple(relation[source_name])
            target = tuple(relation[target_name])
            m = len(source)

            if m == 0 or m > n:
                continue

            for start in range(0, n - m + 1):
                if not self.mp_factors_equal(factors[start:start + m], source):
                    continue

                add_neighbor(factors[:start] + target + factors[start + m:])

    return neighbors


def _mp_presentation_equivalence_cache_signature(self):
    return (
        len(tuple(getattr(self, "attachment_history", ()))),
        tuple(sorted(
            repr(key)
            for key in getattr(self, "resolved_massey_products", {}).keys()
        )),
        tuple(sorted(
            repr(key)
            for key in getattr(self, "resolved_mp_expressions", {}).keys()
        )),
        getattr(self, "bridge_replacement_max_depth", None),
    )


def mp_presentation_equivalent_primitive_report(
    self,
    inputs,
    max_depth=None,
    max_complexity=None,
    include_self=True,
    include_bridge=True,
    include_ainf=True,
):
    """
    Find a resolved MP presentation equivalent to ``inputs``.

    The search is linear, not cyclic: it identifies m3(x,y,m3(f,x,y)) with
    m3(x,y,f), but it does not identify cyclic rotations unless a replacement
    path actually produces that exact linear presentation.
    """

    resolved = getattr(self, "resolved_massey_products", {}) or {}

    if not resolved:
        return None

    try:
        inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
        start = self.canonical_mp_factors(inputs)
        start_key = self.mp_product_block_key(start)
    except Exception:
        return None

    try:
        start_word_key = self.cyclic_factor_tuple_key(start)
    except Exception:
        return None

    if include_self:
        primitive = resolved.get(start_key, None)

        if primitive is not None:
            return {
                "resolved": True,
                "source": "same_massey_presentation",
                "inputs": start_key,
                "equivalent_inputs": start_key,
                "presentation_factors": start,
                "primitive": primitive,
                "path": (start,),
                "depth": 0,
            }

    if max_depth is None:
        max_depth = _bridge_replacement_depth_limit(self)

    if max_depth is None:
        max_depth = 4

    try:
        max_depth = max(0, int(max_depth))
    except (TypeError, ValueError):
        max_depth = 4

    if max_depth <= 0:
        return None

    start_complexity = _replacement_factors_complexity(self, start)

    if max_complexity is None:
        max_complexity = start_complexity

    try:
        max_complexity = max(start_complexity, int(max_complexity))
    except (TypeError, ValueError):
        max_complexity = start_complexity

    cache_key = None

    try:
        cache_key = (
            _mp_presentation_equivalence_cache_signature(self),
            repr(start_word_key),
            int(max_depth),
            int(max_complexity),
            bool(include_self),
            bool(include_bridge),
            bool(include_ainf),
        )
        cache = getattr(self, "_mp_presentation_equivalence_cache", {})

        if cache_key in cache:
            return cache[cache_key]
    except Exception:
        cache_key = None

    def remember(result):
        if cache_key is not None:
            cache = getattr(self, "_mp_presentation_equivalence_cache", {})
            cache[cache_key] = result
            self._mp_presentation_equivalence_cache = cache

        return result

    try:
        relations = self.mp_presentation_replacement_relations(
            include_bridge=include_bridge,
            include_ainf=include_ainf,
            include_self_expanding=True,
        )
    except Exception:
        relations = ()

    if not relations:
        return remember(None)

    queue = [(start, 0, (start,))]
    seen = {start_word_key}

    while queue:
        word, depth, path = queue.pop(0)

        if depth > 0 or include_self:
            try:
                key = self.mp_product_block_key(word)
            except Exception:
                key = None

            if key is not None:
                primitive = resolved.get(key, None)

                if primitive is not None and (include_self or key != start_key):
                    return remember({
                        "resolved": True,
                        "source": "equivalent_massey_presentation",
                        "inputs": start_key,
                        "equivalent_inputs": key,
                        "presentation_factors": word,
                        "primitive": primitive,
                        "path": path,
                        "depth": depth,
                    })

        if depth >= max_depth:
            continue

        try:
            neighbors = self.linear_replacement_neighbors(
                word,
                relations=relations,
            )
        except Exception:
            neighbors = ()

        for neighbor in tuple(neighbors or ()):
            try:
                neighbor = self.canonical_mp_factors(neighbor)
            except Exception:
                continue

            if (
                _replacement_factors_complexity(self, neighbor)
                > max_complexity
            ):
                continue

            try:
                neighbor_key = self.cyclic_factor_tuple_key(neighbor)
            except Exception:
                continue

            if neighbor_key in seen:
                continue

            seen.add(neighbor_key)
            queue.append((neighbor, depth + 1, path + (neighbor,)))

    return remember(None)


def linear_replacement_component(self, factors, relations=None):
    factors = tuple(factors)

    if relations is None:
        relations = self.product_replacement_relations()

    queue = [factors]
    seen = {self.cyclic_factor_tuple_key(factors)}
    component = [factors]

    while queue:
        word = queue.pop(0)

        for neighbor in self.linear_replacement_neighbors(word, relations=relations):
            key = self.cyclic_factor_tuple_key(neighbor)

            if key in seen:
                continue

            seen.add(key)
            component.append(neighbor)
            queue.append(neighbor)

    return _sorted_linear_words(self, component)


def _normalize_rotation_index(length, rotation_index):
    if length <= 0:
        return 0

    try:
        rotation_index = int(rotation_index)
    except Exception:
        rotation_index = 0

    return rotation_index % length


def _cyclic_rotated_tuple(factors, rotation_index):
    factors = tuple(factors)

    if not factors:
        return ()

    rotation_index = _normalize_rotation_index(len(factors), rotation_index)
    return factors[rotation_index:] + factors[:rotation_index]


def _rotation_span_preserved_in_source_word(word, rotation_index, span):
    word = tuple(word)

    if not word:
        return False

    try:
        start, stop = int(span[0]), int(span[1])
    except Exception:
        return False

    if start < 0 or stop <= start or stop > len(word):
        return False

    rotation_index = _normalize_rotation_index(len(word), rotation_index)
    original_indices = [
        (rotation_index + position) % len(word)
        for position in range(start, stop)
    ]

    first = original_indices[0]
    expected = list(range(first, first + len(original_indices)))

    return (
        expected[-1] < len(word)
        and original_indices == expected
    )


def _cyclic_block_occurrence_preserved_by_rotation(
    self,
    word,
    block,
    rotation_index,
):
    word = tuple(word)
    block = tuple(block)

    if not word or not block or len(block) > len(word):
        return False

    rotation = _cyclic_rotated_tuple(word, rotation_index)

    for span in _product_word_block_occurrences(self, rotation, block):
        if _rotation_span_preserved_in_source_word(
            word,
            rotation_index,
            span,
        ):
            return True

    return False


def cyclic_rotation_preserves_block(self, factors, block, rotation_index):
    """
    Return True when a cyclic rotation keeps an ordered touched block linear.

    For example, x1*x2 is preserved by x1*x2*x3 -> x3*x1*x2,
    while x2*x3 is broken across the cyclic cut.
    """

    try:
        factors = self.canonical_mp_factors(tuple(factors))
        block = self.canonical_mp_factors(tuple(block))
    except Exception:
        return False

    return _cyclic_block_occurrence_preserved_by_rotation(
        self,
        factors,
        block,
        rotation_index,
    )


def _cyclic_operation_preservation_failures(self, operation, rotation_indices):
    operation = operation if isinstance(operation, dict) else {}
    word = tuple(operation.get("word", ()) or ())
    block = tuple(operation.get("block", ()) or ())

    if not word or not block:
        return tuple(rotation_indices or ())

    failures = []
    own_rotation = _normalize_rotation_index(
        len(word),
        operation.get("rotation_index", 0),
    )
    span = operation.get("span")

    for rotation_index in tuple(dict.fromkeys(rotation_indices or ())):
        rotation_index = _normalize_rotation_index(len(word), rotation_index)
        preserved = False

        if rotation_index == own_rotation and span is not None:
            preserved = _rotation_span_preserved_in_source_word(
                word,
                rotation_index,
                span,
            )
        else:
            preserved = _cyclic_block_occurrence_preserved_by_rotation(
                self,
                word,
                block,
                rotation_index,
            )

        if not preserved:
            failures.append(rotation_index)

    return tuple(failures)


def _cyclic_source_operation(source):
    source = source if isinstance(source, dict) else {}
    word = tuple(source.get("word", ()) or ())
    rotation_index = source.get("rotation_index", 0)

    if not word and source.get("rotation"):
        word = tuple(source.get("rotation", ()) or ())
        rotation_index = 0

    return {
        "kind": "primitive_resolution",
        "word": word,
        "rotation": tuple(source.get("rotation", ()) or ()),
        "rotation_index": rotation_index,
        "block": tuple(source.get("block", ()) or ()),
        "span": source.get("span"),
        "source": source.get("source", "") or source.get("kind", ""),
        "resolution_group_key": source.get("resolution_group_key"),
    }


def bridge_cyclic_neighbor_records(self, factors, relations=None):
    factors = tuple(factors)

    if relations is None:
        relations = self.product_replacement_relations()

    if not factors:
        return []

    records = []
    seen = set()

    def add_record(record):
        word = tuple(record["neighbor"])

        if not self.mp_factors_composable(word, cyclic=True):
            return

        key = self.canonical_cyclic_factor_key(word)
        record_key = (
            repr(key),
            record["rotation_index"],
            record["span"],
            repr(self.cyclic_factor_tuple_key(record["source_block"])),
            repr(self.cyclic_factor_tuple_key(record["target_block"])),
            record.get("source_name"),
            record.get("target_name"),
            id(record.get("relation")),
        )

        if record_key in seen:
            return

        seen.add(record_key)
        canonical = self.canonical_cyclic_factor_tuple(word)
        record["canonical_neighbor"] = canonical
        record["canonical_neighbor_key"] = key
        record["preserved"] = _rotation_span_preserved_in_source_word(
            factors,
            record["rotation_index"],
            record["span"],
        )
        records.append(record)

    for rotation_index, rotation in enumerate(self.cyclic_rotations(factors)):
        n = len(rotation)

        for relation in relations:
            directions = (
                (("left", "right"),)
                if relation.get("directed")
                else (("left", "right"), ("right", "left"))
            )

            for source_name, target_name in directions:
                source = tuple(relation[source_name])
                target = tuple(relation[target_name])
                m = len(source)

                if m == 0 or m > n:
                    continue

                for start in range(0, n - m + 1):
                    if not self.mp_factors_equal(rotation[start:start + m], source):
                        continue

                    if len(target) != m and (start != 0 or m != n):
                        continue

                    neighbor = rotation[:start] + target + rotation[start + m:]
                    add_record({
                        "kind": "cyclic_replacement",
                        "word": factors,
                        "rotation": tuple(rotation),
                        "rotation_index": rotation_index,
                        "source_name": source_name,
                        "target_name": target_name,
                        "source_block": source,
                        "target_block": target,
                        "block": source,
                        "span": (start, start + m),
                        "replacement": target,
                        "neighbor": neighbor,
                        "relation": relation,
                        "replacement_type": relation.get(
                            "replacement_type",
                            "bridge",
                        ),
                        "cell": relation.get("cell"),
                    })

    return records


def bridge_cyclic_neighbors(self, factors, relations=None):
    neighbors = []
    seen = set()

    for record in self.bridge_cyclic_neighbor_records(
        factors,
        relations=relations,
    ):
        word = tuple(record.get("neighbor", ()))

        try:
            key = self.canonical_cyclic_factor_key(word)
        except Exception:
            key = self.cyclic_factor_tuple_key(word)

        if key in seen:
            continue

        seen.add(key)
        neighbors.append(word)

    return neighbors


def bridge_cyclic_component_paths(self, factors, relations=None):
    factors = tuple(factors)

    if relations is None:
        relations = self.product_replacement_relations(include_ainf=False)

    start = self.canonical_cyclic_factor_tuple(factors)
    start_key = self.canonical_cyclic_factor_key(start)
    queue = [start]
    seen = {repr(start_key)}
    entries = {
        repr(start_key): {
            "word": start,
            "path": (),
        }
    }

    while queue:
        word = queue.pop(0)
        word_key = repr(self.canonical_cyclic_factor_key(word))
        base_path = tuple(entries[word_key]["path"])

        for record in self.bridge_cyclic_neighbor_records(word, relations=relations):
            canonical = tuple(record["canonical_neighbor"])
            key = repr(record["canonical_neighbor_key"])

            if key in seen:
                continue

            path_record = dict(record)
            path_record["from_word"] = tuple(word)
            path_record["to_word"] = canonical
            path_record["path_index"] = len(base_path)
            seen.add(key)
            entries[key] = {
                "word": canonical,
                "path": base_path + (path_record,),
            }
            queue.append(canonical)

    return entries


def bridge_cyclic_component(self, factors, relations=None):
    factors = tuple(factors)

    if relations is None:
        relations = self.product_replacement_relations(include_ainf=False)

    start_key = self.canonical_cyclic_factor_key(factors)
    queue = [self.canonical_cyclic_factor_tuple(factors)]
    seen = {start_key}
    component = list(queue)

    while queue:
        word = queue.pop(0)

        for neighbor in self.bridge_cyclic_neighbors(word, relations=relations):
            key = self.canonical_cyclic_factor_key(neighbor)

            if key in seen:
                continue

            seen.add(key)
            canonical = self.canonical_cyclic_factor_tuple(neighbor)
            component.append(canonical)
            queue.append(canonical)

    return component


def _bridge_cyclic_path_between(self, start, target, relations=None):
    if relations is None:
        relations = self.product_replacement_relations()

    try:
        start = self.canonical_cyclic_factor_tuple(start)
        target_key = repr(self.canonical_cyclic_factor_key(target))
    except Exception:
        return None

    start_key = repr(self.canonical_cyclic_factor_key(start))
    queue = [(start, ())]
    seen = {start_key}

    while queue:
        word, path = queue.pop(0)

        if repr(self.canonical_cyclic_factor_key(word)) == target_key:
            return path

        for record in self.bridge_cyclic_neighbor_records(word, relations=relations):
            canonical = tuple(record["canonical_neighbor"])
            key = repr(record["canonical_neighbor_key"])

            if key in seen:
                continue

            path_record = dict(record)
            path_record["from_word"] = tuple(word)
            path_record["to_word"] = canonical
            path_record["path_index"] = len(path)
            next_path = path + (path_record,)

            if key == target_key:
                return next_path

            seen.add(key)
            queue.append((canonical, next_path))

    return None


def _relation_path_operation(record):
    record = record if isinstance(record, dict) else {}
    return {
        "kind": "cyclic_replacement",
        "word": tuple(record.get("word", ()) or record.get("from_word", ()) or ()),
        "rotation": tuple(record.get("rotation", ()) or ()),
        "rotation_index": record.get("rotation_index", 0),
        "block": tuple(record.get("block", ()) or record.get("source_block", ()) or ()),
        "span": record.get("span"),
        "replacement": tuple(record.get("replacement", ()) or ()),
        "replacement_type": record.get("replacement_type", ""),
        "source_name": record.get("source_name", ""),
        "target_name": record.get("target_name", ""),
        "preserved": record.get("preserved"),
    }


def _cyclic_resolution_chain_report(self, left_source, right_source, relations=None):
    left_source = left_source if isinstance(left_source, dict) else {}
    right_source = right_source if isinstance(right_source, dict) else {}
    left_group = left_source.get("resolution_group_key")
    right_group = right_source.get("resolution_group_key")

    if left_group is None:
        left_group = _product_resolution_group_key(self, left_source)

    if right_group is None:
        right_group = _product_resolution_group_key(self, right_source)

    if repr(left_group) == repr(right_group):
        return {
            "compatible": True,
            "same_resolution_group": True,
            "operations": (
                _cyclic_source_operation(left_source),
                _cyclic_source_operation(right_source),
            ),
            "incompatible_operations": (),
            "path": (),
        }

    left_word = tuple(left_source.get("word", ()) or ())
    right_word = tuple(right_source.get("word", ()) or ())
    path = None
    reversed_order = False

    if left_word and right_word:
        try:
            same_word = (
                repr(self.canonical_cyclic_factor_key(left_word))
                == repr(self.canonical_cyclic_factor_key(right_word))
            )
        except Exception:
            same_word = self.cyclic_factor_tuple_key(left_word) == self.cyclic_factor_tuple_key(right_word)

        if same_word:
            path = ()
        else:
            path = _bridge_cyclic_path_between(
                self,
                left_word,
                right_word,
                relations=relations,
            )

            if path is None:
                reverse_path = _bridge_cyclic_path_between(
                    self,
                    right_word,
                    left_word,
                    relations=relations,
                )

                if reverse_path is not None:
                    path = reverse_path
                    reversed_order = True

    if path is None:
        path = ()

    if reversed_order:
        ordered_sources = (right_source, left_source)
    else:
        ordered_sources = (left_source, right_source)

    operations = [_cyclic_source_operation(ordered_sources[0])]
    operations.extend(
        _relation_path_operation(record)
        for record in tuple(path or ())
    )
    operations.append(_cyclic_source_operation(ordered_sources[1]))

    incompatible = []

    for index, operation in enumerate(operations):
        rotation_indices = [operation.get("rotation_index", 0)]

        if index > 0:
            rotation_indices.append(operations[index - 1].get("rotation_index", 0))

        if index + 1 < len(operations):
            rotation_indices.append(operations[index + 1].get("rotation_index", 0))

        failures = _cyclic_operation_preservation_failures(
            self,
            operation,
            rotation_indices,
        )

        if failures:
            failed_operation = dict(operation)
            failed_operation["failed_rotation_indices"] = failures
            incompatible.append(failed_operation)

    return {
        "compatible": len(incompatible) == 0,
        "same_resolution_group": False,
        "reversed_path": reversed_order,
        "operations": tuple(operations),
        "incompatible_operations": tuple(incompatible),
        "path": tuple(path or ()),
    }


def _cyclic_resolution_chain_compatibility_summary(
    self,
    sources,
    relations=None,
):
    sources = tuple(
        source
        for source in tuple(sources or ())
        if isinstance(source, dict)
    )
    pair_reports = []
    incompatible_pairs = []

    for left_index, left_source in enumerate(sources):
        for right_source in sources[left_index + 1:]:
            report = _cyclic_resolution_chain_report(
                self,
                left_source,
                right_source,
                relations=relations,
            )
            pair_reports.append(report)

            if not report.get("compatible"):
                incompatible_pairs.append(report)

    return {
        "chain_compatible_resolutions": len(incompatible_pairs) == 0,
        "noncompatible_resolution_pair_count": len(incompatible_pairs),
        "noncompatible_resolution_chain": (
            incompatible_pairs[0]
            if incompatible_pairs
            else None
        ),
        "resolution_chain_pair_reports": tuple(pair_reports),
    }


def _single_massey_factor_orbit_resolution(self, word):
    word = tuple(word)

    if len(word) != 1 or not isinstance(word[0], MasseyProduct):
        return None

    factor = word[0]

    if len(tuple(getattr(factor, "inputs", ()))) < 3:
        return None

    try:
        report = self.pure_massey_cyclic_class_report(
            factor,
            require_direct_primitives=True,
            record=False,
            search_bridge_resolvers=False,
        )
    except Exception:
        return None

    if not report.get("resolved") or report.get("likely_over"):
        return None

    if report.get("directly_resolved"):
        return None

    if not report.get("preferred_resolved_by_other_rotations"):
        return None

    return {
        "resolved": True,
        "source": "pure_massey_cyclic_orbit",
        "report": report,
    }


def _pure_massey_orbit_resolved_product_blocks(self, factors=None, relations=None):
    candidate_words = []
    bridge_neighbor_words = []

    for factor in tuple(factors or ()):
        candidate_words.append((factor,))

    for relation in tuple(relations or ()):
        left = tuple(relation.get("left", ()))
        right = tuple(relation.get("right", ()))
        candidate_words.append(left)
        candidate_words.append(right)
        bridge_neighbor_words.append((left, right))
        bridge_neighbor_words.append((right, left))

    blocks = []
    seen = set()

    def remember(word):
        try:
            word = self.canonical_mp_factors(tuple(word))
        except Exception:
            return

        if _single_massey_factor_orbit_resolution(self, word) is None:
            return

        key = self.cyclic_factor_tuple_key(word)

        if key in seen:
            return

        seen.add(key)
        blocks.append(word)

    for word in candidate_words:
        remember(word)

    for source_word, neighbor_word in bridge_neighbor_words:
        try:
            source_word = self.canonical_mp_factors(tuple(source_word))
            neighbor_word = self.canonical_mp_factors(tuple(neighbor_word))
        except Exception:
            continue

        if _single_massey_factor_orbit_resolution(self, source_word) is None:
            continue

        if len(neighbor_word) != 1:
            continue

        key = self.cyclic_factor_tuple_key(neighbor_word)

        if key in seen:
            continue

        seen.add(key)
        blocks.append(neighbor_word)

    return blocks


def _stasheff_zero_resolved_product_blocks(self, factors=None):
    if _ainf_outer_arity_limit(self) == 0:
        return []

    if not _ainf_outer_arity_allowed(self, 2):
        return []

    factors = tuple(factors or ())
    blocks = []
    seen = set()

    for left in factors:
        for right in factors:
            try:
                word = self.canonical_mp_factors((left, right))
            except Exception:
                continue

            if not self.mp_factors_composable(word, cyclic=False):
                continue

            candidates = _stasheff_zero_product_resolution_candidates(
                self,
                word,
            )

            if not any(
                candidate.get("source") == "stasheff_zero"
                for candidate in candidates
            ):
                continue

            try:
                key = self.cyclic_factor_tuple_key(word)
            except Exception:
                continue

            if key in seen:
                continue

            seen.add(key)
            blocks.append(word)

    return blocks


def _should_precompute_stasheff_zero_product_blocks(self, factors):
    raw_limit = getattr(self, "stasheff_zero_precompute_factor_limit", 48)

    if raw_limit in (None, "infinity", "Infinity", "inf", "Inf"):
        return True

    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        limit = 48

    if limit < 0:
        return True

    try:
        return len(tuple(factors or ())) <= limit
    except Exception:
        return True


def _product_report_has_stasheff_zero_resolution(report):
    for rotation in tuple(report.get("rotations", ()) or ()):
        for candidate in tuple(rotation.get("candidates", ()) or ()):
            if candidate.get("source") == "stasheff_zero":
                return True

    return False


def product_cyclic_class_is_bridge_resolved(
    self,
    factors,
    forbidden_blocks=None,
    relations=None,
):
    if forbidden_blocks is None:
        forbidden_blocks = [
            item["factors"]
            for item in self.known_resolved_product_blocks()
        ]

    if relations is None:
        relations = self.product_replacement_relations()

    component = self.bridge_cyclic_component(
        factors,
        relations=relations,
    )
    self_expanding_bridge_relations = None

    for word in component:
        if self.product_word_contains_forbidden_block(
            word,
            forbidden_blocks=forbidden_blocks,
            cyclic=True,
        ):
            return {
                "resolved": True,
                "component": component,
                "resolved_word": word,
            }

        pure_orbit_resolution = _single_massey_factor_orbit_resolution(self, word)

        if pure_orbit_resolution is not None:
            return {
                "resolved": True,
                "component": component,
                "resolved_word": word,
                "pure_orbit_resolution": pure_orbit_resolution,
            }

        stasheff_zero_candidates = _stasheff_zero_product_resolution_candidates(
            self,
            word,
        )

        if any(
            candidate.get("source") == "stasheff_zero"
            for candidate in stasheff_zero_candidates
        ):
            return {
                "resolved": True,
                "component": component,
                "resolved_word": word,
                "stasheff_zero_resolution": stasheff_zero_candidates[0],
            }

        tower_resolution = _product_word_tower_replacement_resolution(
            self,
            word,
            cyclic=True,
        )

        if tower_resolution is not None:
            return {
                "resolved": True,
                "component": component,
                "resolved_word": word,
                "tower_resolution": tower_resolution,
            }

        periodic_resolution = _periodic_product_class_tower_replacement_resolution(
            self,
            word,
        )

        if periodic_resolution is not None:
            return {
                "resolved": True,
                "component": component,
                "resolved_word": word,
                "tower_resolution": periodic_resolution,
            }

        if self_expanding_bridge_relations is None:
            try:
                self_expanding_bridge_relations = (
                    self.mp_presentation_replacement_relations(
                        include_bridge=True,
                        include_ainf=False,
                        include_self_expanding=True,
                    )
                )
            except Exception:
                self_expanding_bridge_relations = []

        for expanded_word in self.linear_replacement_neighbors(
            word,
            relations=self_expanding_bridge_relations,
        ):
            if self.mp_factors_equal(expanded_word, word):
                continue

            expanded_stasheff_candidates = (
                _stasheff_zero_product_resolution_candidates(
                    self,
                    expanded_word,
                )
            )

            if any(
                candidate.get("source") == "stasheff_zero"
                for candidate in expanded_stasheff_candidates
            ):
                return {
                    "resolved": True,
                    "component": component,
                    "resolved_word": expanded_word,
                    "bridge_expanded_word": expanded_word,
                    "bridge_expanded_from": word,
                    "stasheff_zero_resolution": (
                        expanded_stasheff_candidates[0]
                    ),
                }

    return {
        "resolved": False,
        "component": component,
        "resolved_word": None,
    }


def _bridge_direct_primitive_redundancy_resolution(self, factor):
    try:
        factor = self.canonical_mp_factors((factor,))[0]
    except Exception:
        return None

    factor_word = (factor,)
    generator = _single_generator_arrow_from_bridge_side(self, factor)

    if generator is None:
        return None

    blocked = _generator_dependency_arrow_names(self, generator)

    try:
        relations = self.bridge_product_relations()
    except Exception:
        relations = ()

    for relation in tuple(relations or ()):
        sides = (
            (tuple(relation.get("left", ())), tuple(relation.get("right", ()))),
            (tuple(relation.get("right", ())), tuple(relation.get("left", ()))),
        )

        for source, target in sides:
            try:
                source = self.canonical_mp_factors(source)
                target = self.canonical_mp_factors(target)
            except Exception:
                continue

            if len(source) != 1 or not self.mp_factors_equal(source, factor_word):
                continue

            if not target or self.mp_factors_equal(target, factor_word):
                continue

            target_product = MPProduct(self, target)
            primitive_resolution = _concrete_primitive_resolution_for_product(
                self,
                target_product,
                excluded_primitives=(relation.get("cell"),),
            )

            if primitive_resolution is not None:
                return {
                    "resolved": True,
                    "factors": factor_word,
                    "target_factors": target,
                    "bridge_relation": relation,
                    "target_resolution": primitive_resolution,
                    "target_has_primitive": True,
                    "removed_arrow_names": tuple(sorted(blocked, key=str)),
                }

            stasheff_resolution = _stasheff_zero_primitive_resolution_for_product(
                self,
                target_product,
            )

            if stasheff_resolution is not None:
                return {
                    "resolved": True,
                    "factors": factor_word,
                    "target_factors": target,
                    "bridge_relation": relation,
                    "target_resolution": stasheff_resolution,
                    "target_has_stasheff_zero_primitive": True,
                    "removed_arrow_names": tuple(sorted(blocked, key=str)),
                }

            if not _mp_product_defined_without_arrow_names(
                self,
                target_product,
                blocked,
                memo={},
            ):
                continue

            resolution = self.exact_product_block_resolution(
                target,
                verify=False,
            )

            return {
                "resolved": True,
                "factors": factor_word,
                "target_factors": target,
                "bridge_relation": relation,
                "target_resolution": resolution,
                "target_defined_without_generator": True,
                "removed_arrow_names": tuple(sorted(blocked, key=str)),
            }

    return None


def _bridge_substituted_massey_primitive_redundancy_resolution(self, factor):
    try:
        factor = self.canonical_mp_factors((factor,))[0]
    except Exception:
        return None

    factor_word = (factor,)

    try:
        relations = self.bridge_product_relations()
    except Exception:
        relations = ()

    resolved_massey_products = getattr(self, "resolved_massey_products", {}) or {}
    massey_products = getattr(self, "massey_products", {}) or {}

    if not resolved_massey_products or not massey_products:
        return None

    def input_key_tuple(inputs):
        return tuple(
            self.mp_factor_key(self.normalize_mp_input(item))
            for item in tuple(inputs or ())
        )

    factor_input_keys = input_key_tuple(factor_word)

    for relation in tuple(relations or ()):
        sides = (
            (tuple(relation.get("left", ())), tuple(relation.get("right", ()))),
            (tuple(relation.get("right", ())), tuple(relation.get("left", ()))),
        )

        for source, target in sides:
            try:
                source = self.canonical_mp_factors(source)
                target = self.canonical_mp_factors(target)
            except Exception:
                continue

            if len(source) != 1 or not self.mp_factors_equal(source, factor_word):
                continue

            if len(target) != 1 or not isinstance(target[0], MasseyProduct):
                continue

            target_massey = target[0]
            target_key = self.mp_factor_key(target_massey)
            target_input_keys = input_key_tuple(target_massey.inputs)

            if target_input_keys == factor_input_keys:
                continue

            for resolved_key, primitive in resolved_massey_products.items():
                candidate = massey_products.get(resolved_key)

                if not isinstance(candidate, MasseyProduct):
                    continue

                candidate_inputs = tuple(candidate.inputs)

                for index, item in enumerate(candidate_inputs):
                    try:
                        item_key = self.mp_factor_key(self.normalize_mp_input(item))
                    except Exception:
                        continue

                    if item_key != target_key:
                        continue

                    substituted_inputs = (
                        candidate_inputs[:index]
                        + tuple(self.normalize_mp_input(part) for part in source)
                        + candidate_inputs[index + 1:]
                    )

                    if input_key_tuple(substituted_inputs) != target_input_keys:
                        continue

                    return {
                        "resolved": True,
                        "factors": factor_word,
                        "target_factors": target,
                        "substituted_factors": (candidate,),
                        "substitution_source": source,
                        "substitution_index": index,
                        "bridge_relation": relation,
                        "primitive": primitive,
                        "raw_primitive": primitive,
                    }

    return None


def _termination_record_uses_arrow_names(self, record, arrow_names):
    return (
        _primitive_uses_arrow_names(self, record.get("cell", None), arrow_names)
        or _mp_expression_uses_arrow_names(self, record.get("expression", None), arrow_names)
    )


def _bridge_replacement_primitive_avoids_arrow_names(self, candidate, arrow_names):
    for key in (
        "source_product_factors",
        "replacement_block",
        "primitive_block",
    ):
        if _mp_expression_uses_arrow_names(self, candidate.get(key, ()), arrow_names):
            return False

    termination_records = tuple(candidate.get("termination_records", ()) or ())

    if termination_records:
        return any(
            not _termination_record_uses_arrow_names(self, record, arrow_names)
            for record in termination_records
        )

    source_primitive = candidate.get("source_primitive", None)

    if isinstance(source_primitive, dict):
        return not _mp_expression_uses_arrow_names(
            self,
            source_primitive.get("block", ()),
            arrow_names,
        )

    return False


def _bridge_replacement_primitive_redundancy_resolution(self, factor):
    try:
        factor = self.canonical_mp_factors((factor,))[0]
    except Exception:
        return None

    factor_word = (factor,)
    generator = _single_generator_arrow_from_bridge_side(self, factor)

    if generator is None:
        return None

    blocked = _generator_dependency_arrow_names(self, generator)

    try:
        candidates = _metadata_bridge_replacement_primitive_candidates(
            self,
            MPProduct(self, factor_word),
            record=False,
            minimal_only=True,
            max_depth=_BRIDGE_REPLACEMENT_DEPTH_UNSET,
            allow_single_factor=True,
            allow_guarded_self_expanding_after_replacement=True,
        )
    except Exception:
        candidates = []

    for candidate in candidates:
        if not _bridge_candidate_spans_whole_original(candidate, factor_word):
            continue

        if not _bridge_replacement_primitive_avoids_arrow_names(
            self,
            candidate,
            blocked,
        ):
            continue

        return {
            "resolved": True,
            "factors": factor_word,
            "target_factors": tuple(candidate.get("source_product_factors", ())),
            "primitive_block": tuple(candidate.get("primitive_block", ())),
            "bridge_path": tuple(candidate.get("bridge_path", ())),
            "bridge_replacements": tuple(candidate.get("bridge_replacements", ())),
            "primitive_resolution": candidate,
            "target_defined_without_generator": True,
            "removed_arrow_names": tuple(sorted(blocked, key=str)),
        }

    return None


def redundant_generator_report(self):
    """
    Report original generators that have an actual primitive.

    Resolving the cyclic class [x] is not the same as producing a primitive
    whose differential is x, so bridge/tower class resolutions are reported by
    the product stage but do not make a generator redundant here.
    """

    entries = []

    for name, arrow in sorted(getattr(self, "arrows", {}).items(), key=lambda item: str(item[0])):
        if hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"):
            continue

        try:
            factor = self.mp(arrow)
        except Exception:
            continue

        if factor is None:
            continue

        factors = (factor,)
        resolution = self.exact_product_block_resolution(
            factors,
            verify=False,
        )

        if not resolution.get("resolved"):
            bridge_resolution = _bridge_direct_primitive_redundancy_resolution(
                self,
                factor,
            )

            if bridge_resolution is None:
                bridge_resolution = _bridge_substituted_massey_primitive_redundancy_resolution(
                    self,
                    factor,
                )

            if bridge_resolution is None:
                bridge_resolution = _bridge_replacement_primitive_redundancy_resolution(
                    self,
                    factor,
                )

            if bridge_resolution is None:
                continue

            if bridge_resolution.get("bridge_path"):
                reason = "bridge-replacement path to primitive"
            elif bridge_resolution.get("target_has_stasheff_zero_primitive"):
                reason = "bridge to A-inf primitive"
            elif bridge_resolution.get("substituted_factors"):
                reason = "bridge to substituted Massey primitive"
            else:
                reason = "bridge to direct primitive"

            entries.append({
                "kind": "redundant_generator",
                "name": name,
                "arrow": arrow,
                "factors": factors,
                "cyclic": self.mp_factors_composable(factors, cyclic=True),
                "reason": reason,
                "resolution": bridge_resolution,
            })
            continue

        entries.append({
            "kind": "redundant_generator",
            "name": name,
            "arrow": arrow,
            "factors": factors,
            "cyclic": self.mp_factors_composable(factors, cyclic=True),
            "reason": "direct primitive",
            "resolution": resolution,
        })

    return {
        "won": len(entries) == 0,
        "redundant_generators": entries,
    }


def _canonical_forbidden_block_records(self, forbidden_blocks=None):
    known_by_key = {}

    try:
        known_blocks = list(self.known_resolved_product_blocks())
    except Exception:
        known_blocks = []

    for known in known_blocks:
        try:
            known_block = self.canonical_mp_factors(tuple(known.get("factors", ())))
            known_key = self.cyclic_factor_tuple_key(known_block)
        except Exception:
            continue

        known_by_key[repr(known_key)] = known

    if forbidden_blocks is None:
        raw_blocks = known_blocks
    else:
        raw_blocks = list(forbidden_blocks)

    records = []
    seen = set()

    for index, item in enumerate(raw_blocks):
        if isinstance(item, dict):
            raw_factors = item.get("factors", ())
            source = item.get("source", "")
        else:
            raw_factors = item
            source = ""

        try:
            block = self.canonical_mp_factors(tuple(raw_factors))
        except Exception:
            continue

        if not block:
            continue

        try:
            key = self.cyclic_factor_tuple_key(block)
        except Exception:
            key = tuple(repr(item) for item in block)

        key_token = repr(key)
        known = known_by_key.get(key_token, {})

        if not isinstance(item, dict):
            source = known.get("source", "")

        resolution = (
            item.get("resolution", {})
            if isinstance(item, dict)
            else known.get("resolution", {})
        )

        if not source:
            try:
                zero_candidates = _stasheff_zero_product_resolution_candidates(
                    self,
                    block,
                )
            except Exception:
                zero_candidates = ()

            if any(
                candidate.get("source") == "stasheff_zero"
                for candidate in zero_candidates
            ):
                source = "stasheff_zero"
                resolution = {
                    "source": "stasheff_zero",
                    "candidates": tuple(zero_candidates),
                }

        if key_token in seen:
            continue

        seen.add(key_token)
        records.append({
            "index": index,
            "factors": block,
            "key": key,
            "source": source,
            "resolution": resolution,
        })

    return records


def _product_word_block_occurrences(self, word, block):
    word = tuple(word)
    block = tuple(block)
    block_len = len(block)

    if block_len == 0 or block_len > len(word):
        return []

    occurrences = []

    for start in range(0, len(word) - block_len + 1):
        if self.mp_factors_equal(word[start:start + block_len], block):
            occurrences.append((start, start + block_len))

    return occurrences


def _cyclic_rotation_matching_word(self, block, word):
    block = tuple(block)
    word = tuple(word)

    if len(block) != len(word):
        return None

    for rotation in self.cyclic_rotations(block):
        if self.mp_factors_equal(rotation, word):
            return rotation

    return None


def _contextual_primitive_witness_for_side(self, side, block, source):
    side = tuple(side)
    block = tuple(block)
    doubled = side + side
    occurrences = _product_word_block_occurrences(self, doubled, block)

    if not occurrences:
        return None

    start, stop = next(
        (
            span
            for span in occurrences
            if span[0] > 0 and span[1] < len(doubled)
        ),
        occurrences[0],
    )

    resolution = source.get("resolution", {}) if isinstance(source, dict) else {}
    return {
        "word": doubled,
        "side": side,
        "block": block,
        "left_context": doubled[:start],
        "right_context": doubled[stop:],
        "span": (start, stop),
        "primitive": resolution.get("primitive"),
        "raw_primitive": resolution.get("raw_primitive"),
        "source": source.get("source", "") if isinstance(source, dict) else "",
    }


def _product_over_resolution_witness(self, sources, relations):
    sources = tuple(sources or ())

    if len(sources) < 2:
        return None

    for left_index, left_source in enumerate(sources):
        left_block = tuple(left_source.get("block", ()))

        if len(left_block) < 2:
            continue

        for right_source in sources[left_index + 1:]:
            right_block = tuple(right_source.get("block", ()))

            if len(right_block) < 2:
                continue

            for relation in tuple(relations or ()):
                relation_pairs = (
                    (tuple(relation.get("left", ())), tuple(relation.get("right", ()))),
                    (tuple(relation.get("right", ())), tuple(relation.get("left", ()))),
                )

                for left_side, right_side in relation_pairs:
                    if (
                        _cyclic_rotation_matching_word(self, left_block, left_side) is None
                        or _cyclic_rotation_matching_word(self, right_block, right_side) is None
                    ):
                        continue

                    left_witness = _contextual_primitive_witness_for_side(
                        self,
                        left_side,
                        left_block,
                        left_source,
                    )
                    right_witness = _contextual_primitive_witness_for_side(
                        self,
                        right_side,
                        right_block,
                        right_source,
                    )

                    if left_witness is None or right_witness is None:
                        continue

                    return {
                        "kind": "contextual_bridge_square",
                        "left": left_witness,
                        "right": right_witness,
                        "relation": relation,
                    }

    return None


def _tower_resolution_group_key(self, source):
    resolution = source.get("resolution", {}) if isinstance(source, dict) else {}

    if resolution.get("source") != "completed_massey_tower":
        return None

    record = resolution.get("record", {})

    if not isinstance(record, dict):
        return None

    seed_key = record.get("seed_key")

    if seed_key is not None:
        return ("completed_massey_tower", seed_key)

    seed_inputs = record.get("seed_inputs")

    if seed_inputs is not None:
        try:
            return (
                "completed_massey_tower",
                tuple(self.mp_factor_key(item) for item in tuple(seed_inputs)),
            )
        except Exception:
            return ("completed_massey_tower", repr(tuple(seed_inputs)))

    return None


def _pair_tower_resolution_group_key(self, source):
    resolution = source.get("resolution", {}) if isinstance(source, dict) else {}

    if resolution.get("source") != "completed_massey_pair_tower":
        return None

    record = resolution.get("record", {})

    if not isinstance(record, dict):
        return None

    return _completed_pair_tower_record_key(self, record)


def _product_resolution_group_key(self, source):
    resolution = source.get("resolution", {}) if isinstance(source, dict) else {}

    if isinstance(resolution, dict) and resolution.get("resolution_group_key") is not None:
        return resolution.get("resolution_group_key")

    if source.get("resolution_group_key") is not None:
        return source.get("resolution_group_key")

    tower_key = _tower_resolution_group_key(self, source)

    if tower_key is not None:
        return tower_key

    pair_tower_key = _pair_tower_resolution_group_key(self, source)

    if pair_tower_key is not None:
        return pair_tower_key

    return (
        "primitive_block",
        source.get("key"),
    )


def product_cyclic_class_over_resolution_report(
    self,
    factors,
    forbidden_blocks=None,
    relations=None,
):
    """
    Detect cyclic product classes resolved by two distinct primitive sources.

    cyclic_product_class_report() only counts whole-word minimal primitives.
    A product class can also be resolved by wrapping a smaller primitive block
    in context, for example x2 d(v[x1*x2]) x1. If bridge/replacement closure
    puts two distinct wrapped primitive blocks in one cyclic class, the class is
    over-resolved even when no new Massey product is generated.
    """

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return None

    if not factors or not self.mp_factors_composable(factors, cyclic=True):
        return None

    if relations is None:
        relations = self.product_replacement_relations()

    direct_report = self.cyclic_product_class_report(factors, verify=False)
    component = self.bridge_cyclic_component(
        factors,
        relations=relations,
    )
    block_records = _canonical_forbidden_block_records(
        self,
        forbidden_blocks=forbidden_blocks,
    )
    sources = []
    seen_sources = set()

    def remember_source(source):
        key = repr(source.get("key"))

        if key in seen_sources:
            return

        seen_sources.add(key)
        sources.append(source)

    for component_word in component:
        for rotation_index, rotation in enumerate(self.cyclic_rotations(component_word)):
            for block_record in block_records:
                block = tuple(block_record["factors"])

                if len(block) < 2:
                    continue

                occurrences = _product_word_block_occurrences(
                    self,
                    rotation,
                    block,
                )

                if not occurrences:
                    continue

                start, stop = occurrences[0]
                remember_source({
                    "kind": "wrapped_block",
                    "key": ("wrapped_block", block_record["key"]),
                    "word": tuple(component_word),
                    "rotation": tuple(rotation),
                    "block": block,
                    "span": (start, stop),
                    "rotation_index": rotation_index,
                    "source": block_record.get("source", ""),
                    "resolution": block_record.get("resolution", {}),
                })

    report = dict(direct_report)
    report["bridge_component"] = tuple(component)
    report["resolution_sources"] = tuple(sources)
    direct_sources = tuple(
        source
        for source in sources
        if (source.get("source") or source.get("kind") or "") not in {
            "completed_massey_pair_tower",
            "stasheff_zero",
        }
    )
    report["direct_resolution_sources"] = direct_sources
    witness = _product_over_resolution_witness(
        self,
        direct_sources,
        relations,
    )
    report["over_resolution_witness"] = witness
    source_word_keys = set()

    for source in direct_sources:
        try:
            source_word_keys.add(repr(self.canonical_cyclic_factor_key(source["word"])))
        except Exception:
            source_word_keys.add(repr(self.cyclic_factor_tuple_key(source["word"])))

    compatibility = _product_resolution_compatibility_summary(self, direct_sources)
    chain_compatibility = _cyclic_resolution_chain_compatibility_summary(
        self,
        direct_sources,
        relations=relations,
    )
    report.update(compatibility)
    report.update(chain_compatibility)

    if compatibility["minimal_resolution_count"] >= 2:
        report["compatible_resolutions"] = bool(
            chain_compatibility["chain_compatible_resolutions"]
        )

    incompatible = (
        compatibility["resolution_group_count"] >= 2
        and chain_compatibility["noncompatible_resolution_pair_count"] >= 1
    )

    if witness is not None and incompatible:
        report["context_likely_over"] = True
        report["likely_over"] = True
        report["likely_over_reason"] = "cyclic class has non-compatible cyclic resolutions"
    elif (
        len(sources) >= 2
        and len(source_word_keys) >= 2
        and incompatible
    ):
        report["context_likely_over"] = True
        report["likely_over"] = True
        report["likely_over_reason"] = "cyclic class has non-compatible cyclic resolutions"
    else:
        report["context_likely_over"] = False

    return report


def _first_product_over_resolved_component_entry(
    self,
    factors,
    forbidden_blocks,
    relations,
    terminating_min_length,
):
    seeds = []
    seen = {}

    def remember_seed(raw_factors, source):
        try:
            seed = self.canonical_mp_factors(tuple(raw_factors))
        except Exception:
            return

        if not seed or not self.mp_factors_composable(seed, cyclic=True):
            return

        try:
            key = self.canonical_cyclic_factor_key(seed)
        except Exception:
            key = self.cyclic_factor_tuple_key(seed)

        key_token = repr(key)

        source_rank = {
            "forbidden": 0,
            "relation": 1,
            "factor": 2,
        }.get(source, 3)

        if key_token in seen:
            if source_rank < seen[key_token]["rank"]:
                seen[key_token]["source"] = source
                seen[key_token]["rank"] = source_rank
            return

        entry = {
            "factors": seed,
            "source": source,
            "rank": source_rank,
        }
        seen[key_token] = entry
        seeds.append(entry)

    for block in forbidden_blocks:
        remember_seed(block, "forbidden")

    for relation in tuple(relations or ()):
        remember_seed(relation.get("left", ()), "relation")
        remember_seed(relation.get("right", ()), "relation")

    for factor in tuple(factors or ()):
        remember_seed((factor,), "factor")

    seeds.sort(key=lambda item: (
        len(item["factors"]),
        item["rank"],
        repr(self.cyclic_factor_tuple_key(item["factors"])),
    ))

    for seed_entry in seeds:
        seed = seed_entry["factors"]
        report = self.product_cyclic_class_over_resolution_report(
            seed,
            forbidden_blocks=forbidden_blocks,
            relations=relations,
        )

        if not report:
            continue

        if not (
            report.get("context_likely_over")
            or report.get("pair_tower_bridge_over_resolution")
            or (
                seed_entry.get("source") == "forbidden"
                and report.get("likely_over")
                and report.get("resolution_group_count", 0) >= 2
            )
        ):
            continue

        return {
            "kind": "product",
            "length": len(tuple(seed)),
            "factors": tuple(seed),
            "report": report,
            "non_isolated": False,
            "bridge_resolution": {
                "resolved": True,
                "component": tuple(report.get("bridge_component", ())),
                "resolved_word": tuple(seed),
            },
            "likely_over": True,
            "resolution_sources": tuple(report.get("resolution_sources", ())),
        }

    return None


def _tower_replacement_cache_signature(self):
    state = (
        len(getattr(self, "massey_products", {}) or {}),
        len(getattr(self, "resolved_massey_products", {}) or {}),
        len(getattr(self, "resolved_mp_expressions", {}) or {}),
        len(getattr(self, "bridge_expressions", {}) or {}),
        len(getattr(self, "attachment_history", []) or []),
        getattr(self, "bridge_replacement_max_depth", None),
        bool(getattr(self, "filter_self_expanding_replacements", True)),
    )
    memo = getattr(self, "_tower_replacement_cache_signature_memo", None)

    if memo is not None and memo[0] == state:
        return memo[1]

    signature = (
        tuple(sorted(repr(key) for key in getattr(self, "massey_products", {}).keys())),
        tuple(sorted(repr(key) for key in getattr(self, "resolved_massey_products", {}).keys())),
        tuple(sorted(repr(key) for key in getattr(self, "resolved_mp_expressions", {}).keys())),
        tuple(sorted(repr(key) for key in getattr(self, "bridge_expressions", {}).keys())),
        len(getattr(self, "attachment_history", [])),
        getattr(self, "bridge_replacement_max_depth", None),
        bool(getattr(self, "filter_self_expanding_replacements", True)),
    )
    self._tower_replacement_cache_signature_memo = (state, signature)
    return signature


def _tower_replacement_detection_window(self, relations=None):
    if _skip_deep_tower_replacement_resolution(self):
        return 1

    max_seed = 1
    max_relation = 1

    try:
        records = self.completed_massey_tower_elimination_records(record=False)
    except Exception:
        records = ()

    for record in tuple(records or ()):
        max_seed = max(max_seed, len(tuple(record.get("seed_inputs", ()))))

    if relations is None:
        try:
            relations = self.product_replacement_relations()
        except Exception:
            relations = ()

    for relation in tuple(relations or ()):
        max_relation = max(
            max_relation,
            len(tuple(relation.get("left", ()))),
            len(tuple(relation.get("right", ()))),
        )

    try:
        edges = _metadata_replacement_edge_records(self)
    except Exception:
        edges = ()

    for edge in tuple(edges or ()):
        max_relation = max(
            max_relation,
            len(tuple(edge.get("target_factors", ()))),
            len(tuple(edge.get("replacement_factors", ()))),
        )

    return max(2, max_seed + max_relation)


def _skip_deep_tower_replacement_resolution(self):
    return bool(getattr(self, "skip_deep_tower_resolution", False))


def _product_block_tower_elimination_report(self, factors, records=None):
    factors = tuple(factors)

    if not getattr(self, "resolved_massey_products", {}):
        return None

    if len(factors) < 2:
        return None

    try:
        factors = self.canonical_mp_factors(factors)
    except Exception:
        return None

    if not self.mp_factors_composable(factors, cyclic=False):
        return None

    try:
        block_key = self.mp_product_block_key(factors)
    except Exception:
        return None

    try:
        return self.tower_elimination_report(*block_key, records=records)
    except Exception:
        return None


def _tower_replacement_resolution_for_product_block(
    self,
    factors,
    max_depth=None,
):
    if _skip_deep_tower_replacement_resolution(self):
        return None

    factors = tuple(factors)

    try:
        factors = self.canonical_mp_factors(factors)
    except Exception:
        return None

    if len(factors) < 2:
        return None

    if not self.mp_factors_composable(factors, cyclic=False):
        return None

    cache_key = (
        _tower_replacement_cache_signature(self),
        tuple(repr(self.mp_factor_key(factor)) for factor in factors),
        repr(max_depth),
    )
    cache = getattr(self, "_tower_replacement_product_resolution_cache", {})

    if cache_key in cache:
        return cache[cache_key]

    def remember(result):
        cache[cache_key] = result
        self._tower_replacement_product_resolution_cache = cache
        return result

    if not getattr(self, "resolved_massey_products", {}):
        return remember(None)

    try:
        tower_records = self.completed_massey_tower_elimination_records(record=False)
    except Exception:
        tower_records = ()

    if not tower_records:
        return remember(None)

    direct_report = _product_block_tower_elimination_report(
        self,
        factors,
        records=tower_records,
    )

    if direct_report is not None:
        return remember({
            "resolved": True,
            "source": "completed_massey_tower",
            "original_factors": factors,
            "presentation_factors": factors,
            "bridge_path": (),
            "tower_report": direct_report,
        })

    try:
        edges = _metadata_replacement_edge_records(self)
    except Exception:
        edges = ()

    if not edges:
        return remember(None)

    def factors_key(some_factors):
        return tuple(self.mp_factor_key(factor) for factor in tuple(some_factors))

    queue = [(
        factors,
        list(range(len(factors))),
        [],
        {factors_key(factors)},
        frozenset(),
    )]
    searched_states = 0
    state_limit = getattr(self, "tower_replacement_search_state_limit", 2000)

    try:
        state_limit = max(1, int(state_limit))
    except (TypeError, ValueError):
        state_limit = 2000

    while queue:
        searched_states += 1

        if searched_states > state_limit:
            return remember(None)

        (
            current_factors,
            current_origins,
            path_records,
            seen_state_keys,
            replaced_key_reprs,
        ) = queue.pop(0)

        if path_records:
            report = _product_block_tower_elimination_report(
                self,
                current_factors,
                records=tower_records,
            )

            if report is not None:
                return remember({
                    "resolved": True,
                    "source": "completed_massey_tower",
                    "original_factors": factors,
                    "presentation_factors": current_factors,
                    "bridge_path": tuple(path_records),
                    "tower_report": report,
                })

        state_len = len(current_factors)

        for edge in edges:
            target = tuple(edge.get("target_factors", ()))
            replacement = tuple(edge.get("replacement_factors", ()))
            target_len = len(target)

            if target_len == 0 or state_len < target_len:
                continue

            for start in range(0, state_len - target_len + 1):
                stop = start + target_len

                if not self.mp_factors_equal(current_factors[start:stop], target):
                    continue

                if not _metadata_can_apply_guarded_self_expansion(
                    edge,
                    current_origins,
                    start,
                    stop,
                    path_records,
                ):
                    continue

                if _replacement_edge_reintroduces_replaced_key(
                    self,
                    edge,
                    replaced_key_reprs,
                ):
                    continue

                next_factors = (
                    current_factors[:start]
                    + replacement
                    + current_factors[stop:]
                )

                if next_factors and not self.mp_factors_composable(
                    next_factors,
                    cyclic=False,
                ):
                    continue

                next_key = factors_key(next_factors)

                if next_key in seen_state_keys:
                    continue

                next_origins = (
                    current_origins[:start]
                    + [None] * len(replacement)
                    + current_origins[stop:]
                )
                path_record = dict(edge)
                path_record.update({
                    "from": target,
                    "to": replacement,
                    "occurrence_span_before": (start, stop),
                    "replacement_span_after": (start, start + len(replacement)),
                    "source_product_before": current_factors,
                    "source_product_after": next_factors,
                    "origins_before": tuple(current_origins),
                    "origins_after": tuple(next_origins),
                })
                queue.append((
                    next_factors,
                    next_origins,
                    path_records + [path_record],
                    seen_state_keys | {next_key},
                    (
                        replaced_key_reprs
                        | _replacement_edge_target_key_reprs(self, edge)
                    ),
                ))

    return remember(None)


def _tower_replacement_product_resolution_candidates(
    self,
    factors,
    minimal_only=True,
):
    resolution = _tower_replacement_resolution_for_product_block(self, factors)

    if resolution is None:
        return []

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return []

    path = tuple(resolution.get("bridge_path", ()))

    return [{
        "kind": "completed_massey_tower_replacement" if path else "completed_massey_tower",
        "virtual_primitive": True,
        "deferred_primitive": True,
        "source": "completed_massey_tower",
        "left": (),
        "block": factors,
        "right": (),
        "block_span": (0, len(factors)),
        "minimal": True,
        "sign_source": (),
        "verified": True,
        "bridge_resolved": bool(path),
        "original_product_factors": factors,
        "source_product_factors": tuple(resolution.get("presentation_factors", ())),
        "replacement_factors": tuple(resolution.get("presentation_factors", ())),
        "bridge_path": path,
        "profile_contexts": ({
            "context": "original",
            "context_factors": factors,
            "context_key": ("original", self.mp_factor_tuple_key(factors)),
            "span": (0, len(factors)),
            "block": factors,
            "prefix_length": 0,
        },),
        "tower_report": resolution.get("tower_report"),
        "tower_record": (
            resolution.get("tower_report", {}).get("record")
            if isinstance(resolution.get("tower_report"), dict)
            else None
        ),
    }]


def _product_word_tower_replacement_resolution(
    self,
    factors,
    cyclic=False,
):
    if _skip_deep_tower_replacement_resolution(self):
        return None

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return None

    if len(factors) < 2:
        return None

    rotations = self.cyclic_rotations(factors) if cyclic else (factors,)

    for rotation in rotations:
        n = len(rotation)

        for start in range(0, n):
            for stop in range(start + 2, n + 1):
                block = rotation[start:stop]

                if not self.mp_factors_composable(block, cyclic=False):
                    continue

                resolution = _tower_replacement_resolution_for_product_block(
                    self,
                    block,
                )

                if resolution is None:
                    continue

                result = dict(resolution)
                result.update({
                    "word": rotation,
                    "block": block,
                    "block_span": (start, stop),
                    "cyclic": bool(cyclic),
                })
                return result

    return None


def _periodic_product_class_tower_replacement_resolution(self, factors):
    if _skip_deep_tower_replacement_resolution(self):
        return None

    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return None

    if len(factors) != 1:
        return None

    factor = factors[0]

    if getattr(factor, "source", None) != getattr(factor, "target", None):
        return None

    max_repeat = max(2, _tower_replacement_detection_window(self))

    for repeat in range(2, max_repeat + 1):
        word = factors * repeat

        if not self.mp_factors_composable(word, cyclic=False):
            continue

        resolution = _product_word_tower_replacement_resolution(
            self,
            word,
            cyclic=False,
        )

        if resolution is None:
            continue

        result = dict(resolution)
        result.update({
            "periodic_class": factors,
            "periodic_word": word,
            "repeat": repeat,
        })
        return result

    return None


def _tower_replacement_resolved_periodic_class_blocks(self, factors, relations=None):
    if _skip_deep_tower_replacement_resolution(self):
        return []

    blocks = []
    seen = set()

    for factor in tuple(factors or ()):
        try:
            word = self.canonical_mp_factors((factor,))
        except Exception:
            continue

        if len(word) != 1:
            continue

        factor = word[0]

        if getattr(factor, "source", None) != getattr(factor, "target", None):
            continue

        word = (factor,)

        if _periodic_product_class_tower_replacement_resolution(self, word) is None:
            continue

        try:
            key = self.cyclic_factor_tuple_key(word)
        except Exception:
            continue

        if key in seen:
            continue

        seen.add(key)
        blocks.append(word)

    return blocks


def _bridge_resolved_length_one_product_blocks(self, factors, relations=None):
    blocks = []
    seen = set()

    for factor in tuple(factors or ()):
        try:
            word = self.canonical_mp_factors((factor,))
        except Exception:
            continue

        if len(word) != 1:
            continue

        factor = word[0]

        if getattr(factor, "source", None) != getattr(factor, "target", None):
            continue

        word = (factor,)

        try:
            key = self.cyclic_factor_tuple_key(word)
        except Exception:
            continue

        if key in seen:
            continue

        try:
            resolution = self.product_cyclic_class_is_bridge_resolved(
                word,
                relations=relations,
            )
        except Exception:
            resolution = None

        if not resolution or not resolution.get("resolved"):
            continue

        seen.add(key)
        blocks.append(word)

    return blocks


def _automaton_suffix_update(prefixes, forbidden_keys, suffix, next_key):
    candidate = tuple(suffix) + (next_key,)

    for block in forbidden_keys:
        if len(block) <= len(candidate) and candidate[-len(block):] == block:
            return None

    for length in range(len(candidate), -1, -1):
        possible_suffix = candidate[-length:] if length else ()

        if possible_suffix in prefixes:
            return possible_suffix

    return ()


def _sorted_linear_words(self, words):
    return tuple(
        sorted(
            (tuple(word) for word in words),
            key=lambda word: repr(self.cyclic_factor_tuple_key(word))
        )
    )


def _product_tail(factors, window):
    factors = tuple(factors)

    if window is None or len(factors) <= window:
        return factors

    return factors[-window:]


def _product_quotient_window(forbidden_blocks, relations):
    max_forbidden = 1
    max_relation = 1

    for block in forbidden_blocks:
        max_forbidden = max(max_forbidden, len(block))

    for relation in relations:
        max_relation = max(
            max_relation,
            len(relation.get("left", ())),
            len(relation.get("right", ())),
        )

    return max(1, max_forbidden + max_relation - 1)


def _product_suffix_component_key(self, component):
    return tuple(
        self.cyclic_factor_tuple_key(word)
        for word in _sorted_linear_words(self, component)
    )


def product_cyclic_automaton(
    self,
    factors=None,
    forbidden_blocks=None,
):
    if factors is None:
        factors = self.cyclic_factor_alphabet()
    else:
        factors = self.canonical_mp_factors(tuple(factors))

    factors = tuple(factors)

    if forbidden_blocks is None:
        forbidden_blocks = [
            item["factors"]
            for item in self.known_resolved_product_blocks()
        ]
    else:
        forbidden_blocks = [
            self.canonical_mp_factors(tuple(block))
            for block in forbidden_blocks
        ]

    forbidden_keys = [
        self.cyclic_factor_tuple_key(block)
        for block in forbidden_blocks
        if len(block) > 0
    ]
    prefixes = {()}

    for block in forbidden_keys:
        for length in range(1, len(block)):
            prefixes.add(block[:length])

    initial_states = tuple(
        (vertex, ())
        for vertex in sorted(getattr(self, "vertices", set()), key=repr)
    )
    transitions = {}
    queue = list(initial_states)
    seen = set(queue)

    while queue:
        state = queue.pop(0)
        vertex, suffix = state
        edges = []

        for factor in factors:
            if factor.source != vertex:
                continue

            next_suffix = _automaton_suffix_update(
                prefixes,
                forbidden_keys,
                suffix,
                self.cyclic_factor_key(factor)
            )

            if next_suffix is None:
                continue

            next_state = (factor.target, next_suffix)
            edge = {
                "factor": factor,
                "target": next_state,
            }
            edges.append(edge)

            if next_state not in seen:
                seen.add(next_state)
                queue.append(next_state)

        transitions[state] = edges

    return {
        "factors": factors,
        "forbidden_blocks": tuple(forbidden_blocks),
        "forbidden_keys": tuple(forbidden_keys),
        "prefixes": prefixes,
        "initial_states": initial_states,
        "states": tuple(seen),
        "transitions": transitions,
    }


def product_quotient_suffix_component(
    self,
    words,
    forbidden_blocks=None,
    forbidden_keys=None,
    relations=None,
    window=None,
):
    """
    Normalize suffix words modulo local product replacements.

    The input words may have length window + 1 just after appending one factor.
    We first close replacements before trimming, so a relation that starts at
    the oldest remembered factor can still expose a forbidden block.
    """

    needs_forbidden_blocks = forbidden_keys is None or window is None

    if forbidden_blocks is None:
        forbidden_blocks = (
            [
                item["factors"]
                for item in self.known_resolved_product_blocks()
            ]
            if needs_forbidden_blocks
            else []
        )
    elif needs_forbidden_blocks:
        forbidden_blocks = [
            self.canonical_mp_factors(tuple(block))
            for block in forbidden_blocks
        ]
    else:
        forbidden_blocks = tuple(forbidden_blocks)

    if forbidden_keys is None:
        forbidden_keys = tuple(
            self.cyclic_factor_tuple_key(block)
            for block in forbidden_blocks
            if len(block) > 0
        )

    if relations is None:
        relations = self.product_replacement_relations()

    if window is None:
        window = max(
            _product_quotient_window(forbidden_blocks, relations),
            _tower_replacement_detection_window(self, relations=relations),
        )

    queue = []
    seen = set()
    closure = []

    def remember_pretrim(word):
        try:
            word = self.canonical_mp_factors(tuple(word))
        except Exception:
            return

        if word and not self.mp_factors_composable(word, cyclic=False):
            return

        if len(word) > window + 1:
            word = word[-(window + 1):]

        key = self.cyclic_factor_tuple_key(word)

        if key in seen:
            return

        seen.add(key)
        queue.append(word)

    for word in words:
        remember_pretrim(word)

    while queue:
        word = queue.pop(0)

        if self.product_word_contains_forbidden_block(
            word,
            forbidden_keys=forbidden_keys,
            cyclic=False,
        ):
            return None

        if _product_word_tower_replacement_resolution(
            self,
            word,
            cyclic=False,
        ) is not None:
            return None

        closure.append(word)

        for neighbor in self.linear_replacement_neighbors(
            word,
            relations=relations,
        ):
            remember_pretrim(neighbor)

    tail_queue = []
    tail_seen = set()
    tail_component = []

    def remember_tail(word):
        word = _product_tail(word, window)

        if word and not self.mp_factors_composable(word, cyclic=False):
            return

        key = self.cyclic_factor_tuple_key(word)

        if key in tail_seen:
            return

        tail_seen.add(key)
        tail_queue.append(word)

    for word in closure:
        remember_tail(word)

    while tail_queue:
        word = tail_queue.pop(0)

        if self.product_word_contains_forbidden_block(
            word,
            forbidden_keys=forbidden_keys,
            cyclic=False,
        ):
            return None

        if _product_word_tower_replacement_resolution(
            self,
            word,
            cyclic=False,
        ) is not None:
            return None

        tail_component.append(word)

        for neighbor in self.linear_replacement_neighbors(
            word,
            relations=relations,
        ):
            remember_tail(neighbor)

    return _sorted_linear_words(self, tail_component)


def product_quotient_automaton(
    self,
    factors=None,
    forbidden_blocks=None,
    relations=None,
    include_bridge=True,
    include_ainf=True,
    window=None,
):
    """
    Product automaton whose suffix states are quotiented by replacements.

    A state remembers the replacement component of the recent suffix.  Thus if
    A ~ B is a bridge or A_inf replacement, any context fAg and fBg reaches the
    same suffix component before future transitions are explored.
    """

    if factors is None:
        factors = self.cyclic_factor_alphabet()
    else:
        factors = self.canonical_mp_factors(tuple(factors))

    factors = tuple(factors)

    if forbidden_blocks is None:
        forbidden_blocks = [
            item["factors"]
            for item in self.known_resolved_product_blocks()
        ]
    else:
        forbidden_blocks = [
            self.canonical_mp_factors(tuple(block))
            for block in forbidden_blocks
        ]

    forbidden_keys = tuple(
        self.cyclic_factor_tuple_key(block)
        for block in forbidden_blocks
        if len(block) > 0
    )

    if relations is None:
        relations = self.product_replacement_relations(
            include_bridge=include_bridge,
            include_ainf=include_ainf,
        )

    relations = tuple(relations)

    if window is None:
        window = max(
            _product_quotient_window(forbidden_blocks, relations),
            _tower_replacement_detection_window(self, relations=relations),
        )

    empty_component = self.product_quotient_suffix_component(
        ((),),
        forbidden_blocks=forbidden_blocks,
        forbidden_keys=forbidden_keys,
        relations=relations,
        window=window,
    )
    empty_key = _product_suffix_component_key(self, empty_component)
    state_components = {empty_key: empty_component}
    initial_states = tuple(
        (vertex, empty_key)
        for vertex in sorted(getattr(self, "vertices", set()), key=repr)
    )
    transitions = {}
    queue = list(initial_states)
    seen = set(queue)

    while queue:
        state = queue.pop(0)
        vertex, component_key = state
        component = state_components[component_key]
        edges = []

        for factor in factors:
            if factor.source != vertex:
                continue

            candidates = []

            for suffix in component:
                if suffix and suffix[-1].target != factor.source:
                    continue

                candidates.append(tuple(suffix) + (factor,))

            if not candidates:
                continue

            next_component = self.product_quotient_suffix_component(
                candidates,
                forbidden_blocks=forbidden_blocks,
                forbidden_keys=forbidden_keys,
                relations=relations,
                window=window,
            )

            if next_component is None:
                continue

            next_key = _product_suffix_component_key(self, next_component)

            if next_key not in state_components:
                state_components[next_key] = next_component

            next_state = (factor.target, next_key)
            edges.append({
                "factor": factor,
                "target": next_state,
                "source_component": component,
                "target_component": next_component,
            })

            if next_state not in seen:
                seen.add(next_state)
                queue.append(next_state)

        transitions[state] = edges

    return {
        "factors": factors,
        "forbidden_blocks": tuple(forbidden_blocks),
        "relations": relations,
        "window": window,
        "initial_states": initial_states,
        "states": tuple(seen),
        "transitions": transitions,
        "state_components": state_components,
        "quotient_replacements": True,
    }


def shortest_product_automaton_cycle(
    self,
    automaton=None,
    min_length=1,
):
    if automaton is None:
        automaton = self.product_cyclic_automaton()

    best = None
    states = automaton["states"]
    transitions = automaton["transitions"]

    for start in states:
        queue = [(start, ())]
        seen_depth = {start: 0}

        while queue:
            state, word = queue.pop(0)

            if best is not None and len(word) + 1 >= len(best):
                continue

            for edge in transitions.get(state, []):
                next_word = word + (edge["factor"],)
                next_state = edge["target"]

                if next_state == start:
                    candidate = next_word

                    while len(candidate) < min_length:
                        candidate = candidate + next_word

                    if best is None or len(candidate) < len(best):
                        best = candidate

                    continue

                if next_state in seen_depth:
                    continue

                seen_depth[next_state] = len(next_word)
                queue.append((next_state, next_word))

    return best


def product_automaton_max_word_length(self, automaton=None):
    if automaton is None:
        automaton = self.product_cyclic_automaton()

    if self.shortest_product_automaton_cycle(automaton) is not None:
        return None

    states = automaton["states"]
    transitions = automaton["transitions"]
    indegree = {state: 0 for state in states}

    for state in states:
        for edge in transitions.get(state, []):
            indegree[edge["target"]] += 1

    queue = [state for state in states if indegree[state] == 0]
    topo = []

    while queue:
        state = queue.pop(0)
        topo.append(state)

        for edge in transitions.get(state, []):
            target = edge["target"]
            indegree[target] -= 1

            if indegree[target] == 0:
                queue.append(target)

    distance = {
        state: 0
        for state in automaton["initial_states"]
    }

    for state in topo:
        if state not in distance:
            continue

        for edge in transitions.get(state, []):
            target = edge["target"]
            distance[target] = max(distance.get(target, 0), distance[state] + 1)

    return max(distance.values()) if distance else 0


def next_product_cyclic_class(
    self,
    factors=None,
    forbidden_blocks=None,
    min_length=2,
    terminating_min_length=1,
    use_replacement_relations=True,
    include_ainf_replacements=True,
    relations=None,
):
    if use_replacement_relations:
        automaton = self.product_quotient_automaton(
            factors=factors,
            forbidden_blocks=forbidden_blocks,
            relations=relations,
            include_ainf=include_ainf_replacements,
        )
    else:
        automaton = self.product_cyclic_automaton(
            factors=factors,
            forbidden_blocks=forbidden_blocks
        )

    cycle = self.shortest_product_automaton_cycle(
        automaton,
        min_length=max(min_length, terminating_min_length)
    )

    if cycle is None:
        return {
            "won": True,
            "terminating_min_length": terminating_min_length,
            "automaton": automaton,
            "max_word_length": self.product_automaton_max_word_length(automaton),
            "cycle": None,
            "report": None,
        }

    return {
        "won": False,
        "terminating_min_length": terminating_min_length,
        "automaton": automaton,
        "max_word_length": None,
        "cycle": cycle,
        "report": self.cyclic_product_class_report(cycle),
    }


def product_cyclic_frontier_report(
    self,
    factors=None,
    forbidden_blocks=None,
    min_length=1,
    terminating_min_length=1,
    max_length=None,
    use_bridge_relations=True,
    use_replacement_relations=None,
    include_ainf_replacements=True,
    stop_on_likely_over=False,
):
    """
    List the unresolved product cyclic frontier.

    If the first unresolved product length is l, this reports all unresolved
    product cyclic classes of lengths <= l.
    """

    if use_replacement_relations is None:
        use_replacement_relations = use_bridge_relations

    try:
        search_factors = (
            self.cyclic_factor_alphabet()
            if factors is None
            else self.canonical_mp_factors(tuple(factors))
        )
    except Exception:
        search_factors = factors

    if forbidden_blocks is None:
        forbidden_blocks = [
            item["factors"]
            for item in self.known_resolved_product_blocks()
        ]
    else:
        forbidden_blocks = [
            self.canonical_mp_factors(tuple(block))
            for block in forbidden_blocks
        ]

    seen_forbidden = set()

    for block in forbidden_blocks:
        try:
            seen_forbidden.add(self.cyclic_factor_tuple_key(block))
        except Exception:
            continue

    relations = (
        self.product_replacement_relations(
            include_ainf=include_ainf_replacements,
        )
        if use_bridge_relations
        else []
    )

    if use_bridge_relations:
        for block in _tower_replacement_resolved_periodic_class_blocks(
            self,
            search_factors,
            relations=relations,
        ):
            key = self.cyclic_factor_tuple_key(block)

            if key in seen_forbidden:
                continue

            seen_forbidden.add(key)
            forbidden_blocks.append(block)

        for block in _bridge_resolved_length_one_product_blocks(
            self,
            search_factors,
            relations=relations,
        ):
            key = self.cyclic_factor_tuple_key(block)

            if key in seen_forbidden:
                continue

            seen_forbidden.add(key)
            forbidden_blocks.append(block)

        for block in _pure_massey_orbit_resolved_product_blocks(
            self,
            factors=search_factors,
            relations=relations,
        ):
            key = self.cyclic_factor_tuple_key(block)

            if key in seen_forbidden:
                continue

            seen_forbidden.add(key)
            forbidden_blocks.append(block)

        if include_ainf_replacements:
            for block in _stasheff_zero_resolved_product_blocks(
                self,
                factors=search_factors,
            ):
                key = self.cyclic_factor_tuple_key(block)

                if key in seen_forbidden:
                    continue

                seen_forbidden.add(key)
                forbidden_blocks.append(block)

    if stop_on_likely_over:
        entry = _first_product_over_resolved_component_entry(
            self,
            search_factors,
            forbidden_blocks,
            relations,
            terminating_min_length,
        )

        if entry is not None:
            deferred = [entry] if entry["length"] < terminating_min_length else []
            terminating = [] if deferred else [entry]

            return {
                "won": False,
                "first_unresolved_length": entry["length"],
                "max_word_length": None,
                "terminating_min_length": terminating_min_length,
                "automaton": None,
                "next_result": {
                    "won": False,
                    "kind": "likely_over",
                    "cycle": tuple(entry.get("factors", ())),
                    "report": entry.get("report", {}),
                },
                "unresolved_by_length": [{
                    "length": entry["length"],
                    "classes": [entry],
                }],
                "unresolved_classes": [entry],
                "terminating_unresolved_classes": terminating,
                "deferred_unresolved_classes": deferred,
                "likely_over_classes": [entry],
                "search_incomplete": False,
                "searched_max_length": entry["length"],
                "early_likely_over": True,
            }

    raw_refinement_limit = getattr(
        self,
        "product_frontier_resolved_refinement_limit",
        0,
    )

    try:
        refinement_limit = int(raw_refinement_limit)
    except (TypeError, ValueError):
        refinement_limit = 0

    if raw_refinement_limit in (None, "infinity", "Infinity", "inf", "Inf"):
        refinement_limit = None
    elif refinement_limit < 0:
        refinement_limit = None

    refinement_count = 0
    refinement_blocks = []

    while True:
        next_result = self.next_product_cyclic_class(
            factors=search_factors,
            forbidden_blocks=forbidden_blocks,
            min_length=min_length,
            terminating_min_length=terminating_min_length,
            use_replacement_relations=use_replacement_relations,
            include_ainf_replacements=include_ainf_replacements,
            relations=relations if use_replacement_relations else None,
        )

        if next_result.get("won"):
            scan_limit = next_result.get("max_word_length")
        else:
            scan_limit = len(tuple(next_result["cycle"]))

        if max_length is not None:
            scan_limit = max(scan_limit or min_length, max_length)

        first_length = None
        unresolved_by_length = []
        unresolved_classes = []
        deferred_unresolved_classes = []
        terminating_unresolved_classes = []
        new_refinement_blocks = []

        if scan_limit is None:
            scan_limit = min_length - 1

        for length in range(min_length, scan_limit + 1):
            words = self.unresolved_product_cyclic_classes_at_length(
                length,
                factors=search_factors,
                forbidden_blocks=forbidden_blocks,
                use_bridge_relations=use_bridge_relations,
                include_ainf_replacements=include_ainf_replacements,
                relations=relations,
            )
            entries = []

            for word in words:
                report = self.cyclic_product_class_report(word)
                bridge_resolution = self.product_cyclic_class_is_bridge_resolved(
                    word,
                    forbidden_blocks=forbidden_blocks,
                ) if use_bridge_relations else {
                    "resolved": False,
                    "component": [tuple(word)],
                    "resolved_word": None,
                }
                entry = {
                    "kind": "product",
                    "length": length,
                    "factors": tuple(word),
                    "report": report,
                    "non_isolated": False,
                    "bridge_resolution": bridge_resolution,
                }

                if report.get("resolved") and not report.get("likely_over"):
                    try:
                        key = self.cyclic_factor_tuple_key(word)
                    except Exception:
                        key = None

                    if (
                        _product_report_has_stasheff_zero_resolution(report)
                        and key is not None
                        and key not in seen_forbidden
                    ):
                        seen_forbidden.add(key)
                        block = tuple(word)
                        forbidden_blocks.append(block)
                        new_refinement_blocks.append(block)

                    continue

                entries.append(entry)
                unresolved_classes.append(entry)

                if length < terminating_min_length:
                    deferred_unresolved_classes.append(entry)

            unresolved_by_length.append({
                "length": length,
                "classes": entries,
            })

            if entries and length >= terminating_min_length and first_length is None:
                first_length = length
                terminating_unresolved_classes.extend(entries)

            if first_length is not None:
                break

        if (
            first_length is None
            and not next_result.get("won")
            and new_refinement_blocks
            and (
                refinement_limit is None
                or refinement_count + len(new_refinement_blocks) <= refinement_limit
            )
        ):
            refinement_count += len(new_refinement_blocks)
            refinement_blocks.extend(new_refinement_blocks)
            continue

        break

    if first_length is None:
        return {
            "won": bool(next_result.get("won")),
            "first_unresolved_length": None,
            "max_word_length": next_result.get("max_word_length"),
            "terminating_min_length": terminating_min_length,
            "automaton": next_result.get("automaton"),
            "next_result": next_result,
            "unresolved_by_length": unresolved_by_length,
            "unresolved_classes": unresolved_classes,
            "terminating_unresolved_classes": terminating_unresolved_classes,
            "deferred_unresolved_classes": deferred_unresolved_classes,
            "likely_over_classes": [],
            "search_incomplete": not bool(next_result.get("won")),
            "searched_max_length": scan_limit,
            "resolved_refinement_blocks": refinement_blocks,
            "resolved_refinement_count": refinement_count,
        }

    return {
        "won": False,
        "first_unresolved_length": first_length,
        "max_word_length": None,
        "terminating_min_length": terminating_min_length,
        "automaton": next_result.get("automaton"),
        "next_result": next_result,
        "unresolved_by_length": unresolved_by_length,
        "unresolved_classes": unresolved_classes,
        "terminating_unresolved_classes": terminating_unresolved_classes,
        "deferred_unresolved_classes": deferred_unresolved_classes,
        "likely_over_classes": [],
        "search_incomplete": False,
        "searched_max_length": scan_limit,
        "resolved_refinement_blocks": refinement_blocks,
        "resolved_refinement_count": refinement_count,
    }


def unresolved_product_cyclic_classes_at_length(
    self,
    length,
    factors=None,
    forbidden_blocks=None,
    use_bridge_relations=True,
    include_ainf_replacements=True,
    relations=None,
):
    if factors is None:
        factors = self.cyclic_factor_alphabet()
    else:
        factors = self.canonical_mp_factors(tuple(factors))

    if forbidden_blocks is None:
        forbidden_blocks = [
            item["factors"]
            for item in self.known_resolved_product_blocks()
        ]

    forbidden_keys = tuple(
        self.cyclic_factor_tuple_key(block)
        for block in forbidden_blocks
        if len(block) > 0
    )

    results = []
    seen = set()
    if relations is None:
        relations = self.product_replacement_relations(
            include_ainf=include_ainf_replacements,
        ) if use_bridge_relations else []

    def extend(start_vertex, current_vertex, word):
        if len(word) == length:
            if current_vertex != start_vertex:
                return

            if use_bridge_relations:
                try:
                    bridge_neighbors = self.linear_replacement_neighbors(
                        tuple(word),
                        relations=relations,
                    )
                except Exception:
                    bridge_neighbors = ()

                for neighbor in bridge_neighbors:
                    if self.product_word_contains_forbidden_block(
                        neighbor,
                        forbidden_blocks=forbidden_blocks,
                        forbidden_keys=forbidden_keys,
                        cyclic=True,
                    ):
                        return

            bridge_resolution = self.product_cyclic_class_is_bridge_resolved(
                word,
                forbidden_blocks=forbidden_blocks,
                relations=relations,
            ) if use_bridge_relations else {
                "resolved": self.product_word_contains_forbidden_block(
                    word,
                    forbidden_blocks=forbidden_blocks,
                    forbidden_keys=forbidden_keys,
                    cyclic=True
                )
            }

            if bridge_resolution["resolved"]:
                return

            if (
                length == 1
                and use_bridge_relations
                and _periodic_product_class_tower_replacement_resolution(
                    self,
                    word,
                ) is not None
            ):
                return

            key = self.canonical_cyclic_factor_key(word)

            if key in seen:
                return

            seen.add(key)
            results.append(tuple(word))
            return

        for factor in factors:
            if factor.source != current_vertex:
                continue

            extend(start_vertex, factor.target, word + [factor])

    for vertex in sorted(getattr(self, "vertices", set()), key=repr):
        extend(vertex, vertex, [])

    return results


def pure_massey_input_alphabet(
    self,
    include_arrows=True,
    include_cells=False,
    include_higher_massey_products=True,
    resolved_higher_only=False,
):
    inputs = []

    if include_arrows:
        for name in sorted(getattr(self, "arrows", {}).keys()):
            arrow = self.arrows[name]

            if not include_cells and (
                hasattr(arrow, "cell_prefix") or hasattr(arrow, "index")
            ):
                continue

            inputs.append(arrow)

    if include_higher_massey_products:
        mp_items = sorted(
            getattr(self, "massey_products", {}).items(),
            key=lambda item: repr(item[0])
        )

        for key, M in mp_items:
            if not isinstance(M, MasseyProduct) or len(M.inputs) < 3:
                continue

            if resolved_higher_only and key not in getattr(self, "resolved_massey_products", {}):
                continue

            inputs.append(M)

    out = []
    seen = set()

    for item in inputs:
        key = self.mp_factor_key(item)

        if key in seen:
            continue

        seen.add(key)
        out.append(item)

    return tuple(out)


def canonical_pure_massey_input_tuple(self, inputs):
    inputs = self.normalize_mp_inputs(tuple(inputs))
    rotations = self.cyclic_rotations(inputs)

    if not rotations:
        return ()

    return min(
        rotations,
        key=lambda rotation: repr(tuple(self.mp_factor_key(x) for x in rotation))
    )


def canonical_pure_massey_input_key(self, inputs):
    canonical = self.canonical_pure_massey_input_tuple(inputs)
    return tuple(self.mp_factor_key(x) for x in canonical)


def _pure_search_bound_from_product_part(
    self,
    inputs,
    product_result=None,
    min_arity=3,
):
    if product_result is not None and product_result.get("won"):
        bound = product_result.get("max_word_length", None)

        if bound is not None:
            return max(min_arity, bound)

    product_factors = []

    for item in tuple(inputs):
        if isinstance(item, MasseyProduct):
            product_factors.append(item)
        else:
            mp_item = self.mp(item)

            if mp_item is not None:
                product_factors.append(mp_item)

    automaton = self.product_quotient_automaton(factors=tuple(product_factors))

    if self.shortest_product_automaton_cycle(automaton) is not None:
        return min_arity

    bound = self.product_automaton_max_word_length(automaton)

    if bound is None:
        return min_arity

    return max(min_arity, bound)


def generated_pure_massey_cyclic_class_reports(
    self,
    generated_items=None,
    unresolved_only=False,
    require_direct_primitives=False,
    record=True,
):
    """
    Report pure Massey cyclic classes from generated_massey_products.
    """

    if generated_items is None:
        generated_items = getattr(self, "generated_massey_products", [])

    items = _generated_items_from_result(generated_items)
    classes = []
    unresolved_classes = []
    likely_over_classes = []
    seen_orbits = set()

    for item in items:
        if not isinstance(item, MasseyProduct) or len(item.inputs) < 3:
            continue

        cyclically_zero = (
            getattr(item, "source", None) != getattr(item, "target", None)
        )

        if cyclically_zero:
            report = {
                "inputs": tuple(item.inputs),
                "massey_product": item,
                "resolved": True,
                "cyclically_zero": True,
                "cyclically_zero_reason": "non_loop_massey_product",
                "likely_over": False,
                "complete_compatible_orbit": False,
            }
            orbit_key = (
                "isolated",
                tuple(self.mp_factor_key(x) for x in tuple(item.inputs)),
            )
        else:
            report = self.pure_massey_cyclic_class_report(
                item.inputs,
                require_direct_primitives=require_direct_primitives,
                record=record,
            )

            if report.get("complete_compatible_orbit", False):
                orbit_key = (
                    "cyclic",
                    self.canonical_pure_massey_input_key(item.inputs),
                )
            else:
                orbit_key = (
                    "isolated",
                    tuple(self.mp_factor_key(x) for x in tuple(item.inputs)),
                )

        if orbit_key in seen_orbits:
            continue

        seen_orbits.add(orbit_key)

        entry = {
            "kind": "pure_massey",
            "arity": len(tuple(report.get("inputs", item.inputs))),
            "inputs": tuple(report.get("inputs", item.inputs)),
            "massey_product": report.get("massey_product"),
            "resolved": report.get("resolved", False),
            "likely_over": report.get("likely_over", False),
            "cyclically_zero": bool(report.get("cyclically_zero", False)),
            "non_isolated": report.get("complete_compatible_orbit", False),
            "isolated": not report.get("complete_compatible_orbit", False),
            "report": report,
        }

        if not entry["resolved"]:
            unresolved_classes.append(entry)

        if entry["likely_over"]:
            likely_over_classes.append(entry)

        if unresolved_only and entry["resolved"] and not entry["likely_over"]:
            continue

        classes.append(entry)

    return {
        "won": len(unresolved_classes) == 0 and len(likely_over_classes) == 0,
        "source_count": len(items),
        "classes": classes,
        "unresolved_classes": unresolved_classes,
        "likely_over_classes": likely_over_classes,
    }


def _with_generated_product_factors(self, product_factors, generated_items):
    out = list(product_factors or ())
    seen = set()

    for factor in tuple(out):
        try:
            seen.add(self.cyclic_factor_key(factor))
        except Exception:
            pass

    for item in _generated_items_from_result(generated_items):
        if not isinstance(item, MasseyProduct) or len(item.inputs) < 3:
            continue

        if _mp_input_contains_product_value(item):
            continue

        try:
            key = self.cyclic_factor_key(item)
        except Exception:
            continue

        if key in seen:
            continue

        seen.add(key)
        out.append(item)

    return tuple(out)


def _mp_input_contains_product_value(item, seen=None):
    if seen is None:
        seen = set()

    marker = id(item)

    if marker in seen:
        return False

    seen.add(marker)

    if isinstance(item, MPProduct):
        return True

    if isinstance(item, MasseyProduct):
        return any(
            _mp_input_contains_product_value(input_item, seen=seen)
            for input_item in tuple(getattr(item, "inputs", ()))
        )

    return False


def _with_generated_pure_inputs(self, pure_inputs, generated_items):
    out = list(pure_inputs or ())
    seen = set()

    for item in tuple(out):
        try:
            seen.add(self.mp_factor_key(item))
        except Exception:
            pass

    for item in _generated_items_from_result(generated_items):
        if not isinstance(item, MasseyProduct) or len(item.inputs) < 3:
            continue

        try:
            key = self.mp_factor_key(item)
        except Exception:
            continue

        if key in seen:
            continue

        seen.add(key)
        out.append(item)

    return tuple(out)


def _stage_relevant_generated_massey_products(
    self,
    generated_items,
    require_direct_primitives=False,
):
    relevant = []

    for item in _generated_items_from_result(generated_items):
        if not isinstance(item, MasseyProduct) or len(item.inputs) < 3:
            continue

        try:
            if self.generated_massey_inputs_have_zero_product_input(tuple(item.inputs)):
                continue

            if require_direct_primitives:
                defined = self.can_define_mp_direct(*tuple(item.inputs))
            else:
                defined = self.can_define_mp(*tuple(item.inputs))

            if not defined:
                continue

            if (
                not require_direct_primitives
                and not getattr(self, "skip_deep_tower_resolution", False)
                and self.is_tower_eliminated_mp(tuple(item.inputs))
            ):
                continue
        except Exception:
            continue

        relevant.append(item)

    return tuple(relevant)


def _pure_search_word_is_tower_eliminated(self, word):
    word = tuple(self.normalize_mp_inputs(tuple(word)))

    if not any(isinstance(item, MasseyProduct) for item in word):
        try:
            return self.tower_elimination_report(*word) is not None
        except Exception:
            return False

    try:
        return self.is_tower_eliminated_mp(word)
    except Exception:
        return False


def next_pure_massey_cyclic_class(
    self,
    inputs=None,
    min_arity=3,
    max_arity=None,
    product_result=None,
    include_arrows=True,
    include_cells=False,
    include_higher_massey_products=True,
    resolved_higher_only=False,
    require_direct_primitives=False,
    record=True,
):
    """
    Find the next unresolved pure Massey cyclic class in arity order.
    """

    if inputs is None:
        inputs = self.pure_massey_input_alphabet(
            include_arrows=include_arrows,
            include_cells=include_cells,
            include_higher_massey_products=include_higher_massey_products,
            resolved_higher_only=resolved_higher_only,
        )
    else:
        inputs = tuple(self.normalize_mp_input(item) for item in tuple(inputs))

    inputs = tuple(inputs)

    if max_arity is None:
        max_arity = _pure_search_bound_from_product_part(
            self,
            inputs,
            product_result=product_result,
            min_arity=min_arity,
        )

    seen_orbits = set()
    first_likely_over = None

    def extend(arity, word):
        if len(word) == arity:
            if not self.mp_factors_composable(word, cyclic=False):
                return None

            if require_direct_primitives:
                defined = self.can_define_mp_direct(*word)
            else:
                defined = self.can_define_mp(*word)

            if not defined:
                return None

            if not require_direct_primitives:
                if (
                    not getattr(self, "skip_deep_tower_resolution", False)
                    and _pure_search_word_is_tower_eliminated(self, word)
                ):
                    return None

            report_kwargs = {
                "require_direct_primitives": require_direct_primitives,
                "record": record,
            }

            if hasattr(self, "search_pure_bridge_resolvers"):
                report_kwargs["search_bridge_resolvers"] = bool(
                    getattr(self, "search_pure_bridge_resolvers", False)
                )

            report = self.pure_massey_cyclic_class_report(
                word,
                **report_kwargs,
            )

            if report.get("complete_compatible_orbit", False):
                orbit_key = (
                    "cyclic",
                    self.canonical_pure_massey_input_key(word),
                )
            else:
                orbit_key = (
                    "isolated",
                    tuple(self.mp_factor_key(x) for x in tuple(word)),
                )

            if orbit_key in seen_orbits:
                return None

            seen_orbits.add(orbit_key)
            report_inputs = tuple(report.get("inputs", word))

            if report.get("likely_over") and first_likely_over is None:
                return {
                    "kind": "likely_over",
                    "arity": arity,
                    "inputs": report_inputs,
                    "report": report,
                }

            if not report.get("resolved", False):
                return {
                    "kind": "unresolved",
                    "arity": arity,
                    "inputs": report_inputs,
                    "report": report,
                }

            return None

        for item in inputs:
            if word and word[-1].target != item.source:
                continue

            result = extend(arity, word + (item,))

            if result is not None:
                return result

        return None

    for arity in range(min_arity, max_arity + 1):
        result = extend(arity, ())

        if result is None:
            continue

        if result["kind"] == "likely_over":
            first_likely_over = result
            break

        return {
            "found": True,
            "status": "unresolved",
            "arity": result["arity"],
            "inputs": result["inputs"],
            "report": result["report"],
            "searched_min_arity": min_arity,
            "searched_max_arity": max_arity,
        }

    if first_likely_over is not None:
        return {
            "found": True,
            "status": "likely_over",
            "arity": first_likely_over["arity"],
            "inputs": first_likely_over["inputs"],
            "report": first_likely_over["report"],
            "searched_min_arity": min_arity,
            "searched_max_arity": max_arity,
        }

    return {
        "found": False,
        "status": "won",
        "report": None,
        "searched_min_arity": min_arity,
        "searched_max_arity": max_arity,
    }


def cyclic_search_stage_report(
    self,
    product_factors=None,
    pure_inputs=None,
    min_product_length=1,
    max_product_length=None,
    terminating_min_product_length=1,
    min_pure_arity=3,
    max_pure_arity=None,
    include_cells=False,
    include_higher_massey_products=True,
    resolved_higher_only=True,
    generated_massey_products=None,
    fallback_to_pure_search=True,
    require_direct_primitives=False,
    record=True,
):
    """
    Combined stopping report: product automaton first, then pure MPs.
    """

    explicit_product_factors = product_factors is not None
    explicit_empty_product_factors = False

    if explicit_product_factors:
        try:
            explicit_empty_product_factors = len(tuple(product_factors)) == 0
        except Exception:
            explicit_empty_product_factors = False

    if product_factors is None:
        stage_generated_massey_products = _stage_relevant_generated_massey_products(
            self,
            (
                generated_massey_products
                if generated_massey_products is not None
                else getattr(self, "generated_massey_products", [])
            ),
            require_direct_primitives=require_direct_primitives,
        )
        product_generated_massey_products = _stage_relevant_generated_massey_products(
            self,
            (
                generated_massey_products
                if generated_massey_products is not None
                else getattr(self, "generated_massey_products", [])
            ),
            require_direct_primitives=True,
        )
        product_factors = self.cyclic_factor_alphabet(
            include_cells=include_cells,
            include_higher_massey_products=include_higher_massey_products,
            resolved_higher_only=resolved_higher_only,
        )

        if include_higher_massey_products:
            product_factors = _with_generated_product_factors(
                self,
                product_factors,
                product_generated_massey_products,
            )
    else:
        stage_generated_massey_products = _stage_relevant_generated_massey_products(
            self,
            (
                generated_massey_products
                if generated_massey_products is not None
                else getattr(self, "generated_massey_products", [])
            ),
            require_direct_primitives=require_direct_primitives,
        )

    product_result = self.product_cyclic_frontier_report(
        factors=product_factors,
        min_length=min_product_length,
        terminating_min_length=terminating_min_product_length,
        max_length=max_product_length,
        stop_on_likely_over=max_product_length is None,
    )

    pure_generated_result = self.generated_pure_massey_cyclic_class_reports(
        generated_items=stage_generated_massey_products,
        unresolved_only=False,
        require_direct_primitives=require_direct_primitives,
        record=record,
    )
    product_cycle_result = self.generated_product_cycle_class_reports(
        unresolved_only=False,
        record=record,
    )
    if getattr(self, "detect_redundant_generators", False):
        generator_redundancy_result = self.redundant_generator_report()
    else:
        generator_redundancy_result = {
            "won": True,
            "redundant_generators": [],
            "skipped": True,
        }
    pure_search_result = None
    redundant_has_problem = (
        len(generator_redundancy_result.get("redundant_generators", [])) > 0
    )
    product_cycle_has_problem = (
        len(product_cycle_result.get("unresolved_classes", [])) > 0
        or len(product_cycle_result.get("likely_over_classes", [])) > 0
    )
    generated_has_problem = (
        len(pure_generated_result.get("unresolved_classes", [])) > 0
        or len(pure_generated_result.get("likely_over_classes", [])) > 0
        or product_cycle_has_problem
    )
    product_has_problem = not bool(product_result.get("won"))

    if (
        fallback_to_pure_search
        and not product_has_problem
        and not generated_has_problem
    ):
        if pure_inputs is None:
            # Default pure search is generators plus active generated MPs; resolved
            # tower MPs remain available to callers via explicit pure_inputs.
            pure_inputs = self.pure_massey_input_alphabet(
                include_cells=include_cells,
                include_higher_massey_products=False,
                resolved_higher_only=resolved_higher_only,
            )

            if include_higher_massey_products and explicit_empty_product_factors:
                pure_inputs = _with_generated_pure_inputs(
                    self,
                    pure_inputs,
                    stage_generated_massey_products,
                )

        pure_search_result = self.next_pure_massey_cyclic_class(
            inputs=pure_inputs,
            min_arity=min_pure_arity,
            max_arity=max_pure_arity,
            product_result=product_result,
            include_cells=include_cells,
            include_higher_massey_products=include_higher_massey_products,
            resolved_higher_only=resolved_higher_only,
            require_direct_primitives=require_direct_primitives,
            record=record,
        )

    pure_result = pure_generated_result

    if pure_search_result is not None:
        pure_result = pure_search_result

    if not product_result.get("won"):
        return {
            "won": False,
            "next_kind": "product",
            "product_part_won": False,
            "product_result": product_result,
            "pure_result": pure_result,
            "pure_generated_result": pure_generated_result,
            "generated_product_cycle_result": product_cycle_result,
            "generator_redundancy_result": generator_redundancy_result,
            "pure_search_result": pure_search_result,
        }

    search_has_problem = (
        pure_search_result is not None
        and pure_search_result.get("found")
    )

    if redundant_has_problem:
        return {
            "won": False,
            "next_kind": "redundant_generator",
            "product_part_won": True,
            "product_result": product_result,
            "pure_result": pure_result,
            "pure_generated_result": pure_generated_result,
            "generated_product_cycle_result": product_cycle_result,
            "generator_redundancy_result": generator_redundancy_result,
            "pure_search_result": pure_search_result,
        }

    if generated_has_problem or search_has_problem:
        next_kind = "product_cycle" if product_cycle_has_problem else "pure_massey"

        return {
            "won": False,
            "next_kind": next_kind,
            "product_part_won": True,
            "product_result": product_result,
            "pure_result": pure_result,
            "pure_generated_result": pure_generated_result,
            "generated_product_cycle_result": product_cycle_result,
            "generator_redundancy_result": generator_redundancy_result,
            "pure_search_result": pure_search_result,
        }

    return {
        "won": True,
        "next_kind": None,
        "product_part_won": True,
        "product_result": product_result,
        "pure_result": pure_result,
        "pure_generated_result": pure_generated_result,
        "generated_product_cycle_result": product_cycle_result,
        "generator_redundancy_result": generator_redundancy_result,
        "pure_search_result": pure_search_result,
    }


def _cyclic_autocomplete_default_inputs(self):
    inputs = []

    for name in getattr(self, "arrows", {}):
        arrow = self.arrows[name]

        if hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"):
            continue

        inputs.append(arrow)

    return tuple(inputs)


def _cyclic_autocomplete_attachment_entry(self, rotation, reason):
    M = rotation.get("massey_product")
    inputs = tuple(rotation.get("inputs", ()))

    return {
        "kind": "pure_massey",
        "reason": reason,
        "arity": len(inputs),
        "inputs": inputs,
        "massey_product": M,
        "resolved": rotation.get("resolved", False),
    }


def _cyclic_autocomplete_choose_leave_rotation(
    self,
    report,
    leave_inputs=None,
    leave_strategy="current",
):
    rotations = list(report.get("rotations", []))
    defined = [
        rotation
        for rotation in rotations
        if rotation.get("defined")
    ]

    if not defined:
        return None

    if leave_inputs is not None:
        leave_inputs = tuple(self.normalize_mp_inputs(tuple(leave_inputs)))
        leave_key = tuple(self.mp_factor_key(x) for x in leave_inputs)

        for rotation in defined:
            rotation_key = tuple(
                self.mp_factor_key(x)
                for x in tuple(rotation.get("inputs", ()))
            )

            if rotation_key == leave_key:
                return rotation

    if leave_strategy == "canonical":
        return min(
            defined,
            key=lambda rotation: repr(
                tuple(
                    self.mp_factor_key(x)
                    for x in tuple(rotation.get("inputs", ()))
                )
            )
        )

    return defined[0]


def cyclic_autocomplete_plan(
    self,
    pure_inputs=None,
    product_factors=None,
    min_product_length=1,
    max_product_length=None,
    terminating_min_product_length=1,
    min_pure_arity=3,
    max_pure_arity=8,
    include_cells=False,
    include_higher_massey_products=False,
    resolved_higher_only=True,
    require_direct_primitives=True,
    resolve_non_isolated="stop",
    leave_inputs=None,
    leave_strategy="current",
):
    """
    Plan the next cyclic autocomplete move without attaching cells.

    By default, non-isolated pure Massey classes are reported as choice points.
    Passing resolve_non_isolated="attach_all_but_leave" proposes resolving all
    currently unresolved rotations except one chosen representative.
    """

    if product_factors is None:
        product_factors = self.cyclic_factor_alphabet(
            include_cells=include_cells,
            include_higher_massey_products=True,
            resolved_higher_only=resolved_higher_only,
        )

    product_result = self.product_cyclic_frontier_report(
        factors=product_factors,
        min_length=min_product_length,
        max_length=max_product_length,
        terminating_min_length=terminating_min_product_length,
    )

    if not product_result.get("won"):
        return {
            "status": "blocked_product",
            "reason": "product frontier has unresolved terminating classes",
            "product_result": product_result,
            "attachments": [],
        }

    if pure_inputs is None:
        if include_higher_massey_products:
            pure_inputs = self.pure_massey_input_alphabet(
                include_cells=include_cells,
                include_higher_massey_products=include_higher_massey_products,
                resolved_higher_only=resolved_higher_only,
            )
        else:
            pure_inputs = _cyclic_autocomplete_default_inputs(self)
    else:
        pure_inputs = tuple(
            self.normalize_mp_input(item)
            for item in tuple(pure_inputs)
        )

    pure_result = self.next_pure_massey_cyclic_class(
        inputs=pure_inputs,
        min_arity=min_pure_arity,
        max_arity=max_pure_arity,
        product_result=product_result,
        include_cells=include_cells,
        include_higher_massey_products=include_higher_massey_products,
        resolved_higher_only=resolved_higher_only,
        require_direct_primitives=require_direct_primitives,
        record=True,
    )

    if not pure_result.get("found"):
        return {
            "status": "won",
            "reason": "no unresolved pure Massey class found within bounds",
            "product_result": product_result,
            "pure_result": pure_result,
            "attachments": [],
        }

    if pure_result.get("status") == "likely_over":
        return {
            "status": "likely_over",
            "reason": "a pure Massey orbit is likely over-resolved",
            "product_result": product_result,
            "pure_result": pure_result,
            "attachments": [],
        }

    report = pure_result.get("report", {})

    if report.get("complete_compatible_orbit", False):
        leave_rotation = _cyclic_autocomplete_choose_leave_rotation(
            self,
            report,
            leave_inputs=leave_inputs,
            leave_strategy=leave_strategy,
        )
        leave_inputs_tuple = (
            tuple(leave_rotation.get("inputs", ()))
            if leave_rotation is not None
            else None
        )
        attachments = []

        for rotation in report.get("rotations", []):
            if not rotation.get("defined") or rotation.get("resolved"):
                continue

            if leave_rotation is not None and rotation is leave_rotation:
                continue

            attachments.append(
                _cyclic_autocomplete_attachment_entry(
                    self,
                    rotation,
                    "non_isolated_orbit"
                )
            )

        if resolve_non_isolated != "attach_all_but_leave":
            return {
                "status": "needs_choice",
                "reason": "non-isolated pure Massey orbit needs a representative to leave unresolved",
                "product_result": product_result,
                "pure_result": pure_result,
                "report": report,
                "leave_inputs": leave_inputs_tuple,
                "proposed_attachments": attachments,
                "attachments": [],
            }

        if not attachments:
            return {
                "status": "blocked",
                "reason": "non-isolated orbit had no attachable unresolved rotations",
                "product_result": product_result,
                "pure_result": pure_result,
                "report": report,
                "leave_inputs": leave_inputs_tuple,
                "attachments": [],
            }

        return {
            "status": "attach",
            "action": "attach_non_isolated_orbit",
            "reason": "attach all unresolved rotations except the chosen representative",
            "product_result": product_result,
            "pure_result": pure_result,
            "report": report,
            "leave_inputs": leave_inputs_tuple,
            "attachments": attachments,
        }

    rotation = report.get("rotations", [{}])[0]
    attachment = _cyclic_autocomplete_attachment_entry(
        self,
        rotation,
        "isolated_unresolved"
    )

    if attachment.get("massey_product") is None:
        return {
            "status": "blocked",
            "reason": "isolated unresolved class has no Massey product object",
            "product_result": product_result,
            "pure_result": pure_result,
            "report": report,
            "attachments": [],
        }

    return {
        "status": "attach",
        "action": "attach_isolated",
        "reason": "isolated unresolved pure Massey class",
        "product_result": product_result,
        "pure_result": pure_result,
        "report": report,
        "attachments": [attachment],
    }


def _cyclic_autocomplete_fingerprint(self):
    resolved = tuple(
        sorted(
            repr(tuple(self.mp_factor_key(x) for x in tuple(key)))
            for key in getattr(self, "resolved_massey_products", {}).keys()
        )
    )
    expressions = tuple(
        sorted(
            repr(key)
            for key in getattr(self, "resolved_mp_expressions", {}).keys()
        )
    )

    return (resolved, expressions)


def _cyclic_autocomplete_remember_generated(self, M):
    if M is None:
        return None

    key = self.mp_factor_key(M)

    items = getattr(self, "generated_massey_products", None)

    if items is None:
        self.generated_massey_products = [M]
        return key

    if isinstance(items, list):
        for item in items:
            if isinstance(item, MasseyProduct) and self.mp_factor_key(item) == key:
                return None

        items.append(M)
        return key

    return None


def _cyclic_autocomplete_forget_generated_keys(self, keys):
    key_set = set(keys or [])

    if not key_set or not hasattr(self, "generated_massey_products"):
        return []

    removed = []
    kept = []

    for item in self.generated_massey_products:
        if isinstance(item, MasseyProduct) and self.mp_factor_key(item) in key_set:
            removed.append(item)
        else:
            kept.append(item)

    self.generated_massey_products = kept
    return removed


def apply_cyclic_autocomplete(
    self,
    pure_inputs=None,
    product_factors=None,
    min_product_length=1,
    max_product_length=None,
    terminating_min_product_length=1,
    min_pure_arity=3,
    max_pure_arity=8,
    include_cells=False,
    include_higher_massey_products=False,
    resolved_higher_only=True,
    require_direct_primitives=True,
    resolve_non_isolated="stop",
    leave_inputs=None,
    leave_strategy="current",
    max_steps=20,
    max_cells=50,
    dry_run=False,
):
    """
    Apply cyclic autocomplete with explicit breakers and an undo token.
    """

    self.ensure_attachment_history()
    start_history_length = len(getattr(self, "attachment_history", []))
    steps = []
    attached = []
    generated_keys_added = []
    seen = set()
    status = None
    reason = None

    for step_index in range(max_steps):
        fingerprint = _cyclic_autocomplete_fingerprint(self)

        if fingerprint in seen:
            status = "repeat_detected"
            reason = "autocomplete state repeated"
            break

        seen.add(fingerprint)
        plan = self.cyclic_autocomplete_plan(
            pure_inputs=pure_inputs,
            product_factors=product_factors,
            min_product_length=min_product_length,
            max_product_length=max_product_length,
            terminating_min_product_length=terminating_min_product_length,
            min_pure_arity=min_pure_arity,
            max_pure_arity=max_pure_arity,
            include_cells=include_cells,
            include_higher_massey_products=include_higher_massey_products,
            resolved_higher_only=resolved_higher_only,
            require_direct_primitives=require_direct_primitives,
            resolve_non_isolated=resolve_non_isolated,
            leave_inputs=leave_inputs,
            leave_strategy=leave_strategy,
        )
        steps.append(plan)

        if plan.get("status") != "attach":
            status = plan.get("status")
            reason = plan.get("reason")
            break

        attachments = list(plan.get("attachments", []))

        if len(attached) + len(attachments) > max_cells:
            status = "budget_exceeded"
            reason = "max_cells would be exceeded"
            break

        if dry_run:
            status = "dry_run"
            reason = "dry run stopped before applying attachments"
            break

        for attachment in attachments:
            M = attachment.get("massey_product")

            if M is None:
                status = "blocked"
                reason = "planned attachment had no Massey product object"
                break

            before = len(getattr(self, "attachment_history", []))
            cell = self.attach_mp_cell(M)
            after = len(getattr(self, "attachment_history", []))

            if cell is None or after == before:
                status = "blocked"
                reason = "attachment failed or did not add a new cell"
                break

            generated_key = _cyclic_autocomplete_remember_generated(self, M)

            if generated_key is not None:
                generated_keys_added.append(generated_key)

            record = dict(attachment)
            record["cell"] = cell
            record["history_index"] = after - 1
            attached.append(record)

        if status is not None:
            break

    else:
        status = "budget_exceeded"
        reason = "max_steps reached"

    final_history_length = len(getattr(self, "attachment_history", []))
    token = {
        "kind": "cyclic_autocomplete_undo",
        "start_attachment_history_length": start_history_length,
        "final_attachment_history_length": final_history_length,
        "attached_count": len(attached),
        "attached_cells": [
            item.get("cell")
            for item in attached
        ],
        "generated_keys_added": list(generated_keys_added),
    }

    if attached:
        stack = getattr(self, "_cyclic_autocomplete_undo_stack", None)

        if stack is None:
            stack = []
            self._cyclic_autocomplete_undo_stack = stack

        stack.append(token)

    return {
        "status": status,
        "reason": reason,
        "steps": steps,
        "attached": attached,
        "attached_count": len(attached),
        "undo_token": token if attached else None,
        "start_attachment_history_length": start_history_length,
        "final_attachment_history_length": final_history_length,
    }


def undo_cyclic_autocomplete(
    self,
    token=None,
    force=False,
    verbose=True,
):
    """
    Undo one autocomplete run, refusing by default if later cells were added.
    """

    stack = getattr(self, "_cyclic_autocomplete_undo_stack", [])

    if token is None:
        if not stack:
            return {
                "undone": False,
                "reason": "no autocomplete undo token available",
            }

        token = stack[-1]

    start = token.get("start_attachment_history_length")
    final = token.get("final_attachment_history_length")
    current = len(getattr(self, "attachment_history", []))

    if current != final and not force:
        return {
            "undone": False,
            "reason": "attachment history changed after autocomplete; pass force=True to undo anyway",
            "current_attachment_history_length": current,
            "expected_attachment_history_length": final,
        }

    undone = []

    while len(getattr(self, "attachment_history", [])) > start:
        result = self.undo_latest_attachment(verbose=verbose)

        if result is None:
            break

        undone.append(result)

    removed_generated = _cyclic_autocomplete_forget_generated_keys(
        self,
        token.get("generated_keys_added", [])
    )

    if stack and token in stack:
        stack.remove(token)

    return {
        "undone": True,
        "undone_count": len(undone),
        "undo_results": undone,
        "removed_generated": removed_generated,
        "remaining_attachment_history_length": len(getattr(self, "attachment_history", [])),
    }


def _massey_tower_factor_keys(self, inputs):
    return tuple(self.mp_factor_key(x) for x in tuple(inputs))


def _tower_coerce_inputs(args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return tuple(args[0])

    return tuple(args)


def _tower_factor_key(self, factor):
    try:
        factor = self.normalize_mp_input(factor)
    except Exception:
        pass

    return self.mp_factor_key(factor)


def _tower_word_is_periodic_subword(self, word, seed_inputs):
    word = tuple(word)
    seed_inputs = tuple(seed_inputs)

    if not word or not seed_inputs:
        return False

    word_keys = tuple(_tower_factor_key(self, factor) for factor in word)
    seed_keys = tuple(_tower_factor_key(self, factor) for factor in seed_inputs)
    n = len(seed_keys)

    for offset in range(n):
        if all(
            word_keys[index] == seed_keys[(offset + index) % n]
            for index in range(len(word_keys))
        ):
            return True

    return False


def _tower_single_mp_factor(self, product):
    try:
        factors = self.canonical_mp_factors(product)
    except Exception:
        return None

    if len(factors) != 1:
        return None

    return factors[0]


def _tower_alias_input(self, factor):
    factor = self.normalize_mp_input(factor)

    if isinstance(factor, MasseyProduct) and len(factor.inputs) == 1:
        return self.normalize_mp_input(factor.inputs[0])

    return factor


def _tower_seed_candidates(self):
    candidates = {}

    def remember(seed_inputs, aliases=()):
        seed_inputs = tuple(self.normalize_mp_inputs(tuple(seed_inputs)))

        if len(seed_inputs) < 3:
            return

        seed_key = self.mp_key(*seed_inputs)
        record = candidates.setdefault(seed_key, {
            "seed_inputs": seed_inputs,
            "aliases": [],
        })
        seen_aliases = {
            _tower_factor_key(self, alias)
            for alias in record["aliases"]
        }

        for alias in aliases:
            alias = _tower_alias_input(self, alias)
            alias_key = _tower_factor_key(self, alias)

            if alias_key in seen_aliases:
                continue

            seen_aliases.add(alias_key)
            record["aliases"].append(alias)

    for key, M in getattr(self, "massey_products", {}).items():
        if isinstance(M, MasseyProduct):
            remember(M.inputs)
        elif isinstance(key, tuple):
            remember(key)

    for expression in getattr(self, "bridge_expressions", {}).values():
        if not isinstance(expression, MPElement):
            continue

        singleton_factors = []

        for product in expression.terms.keys():
            factor = _tower_single_mp_factor(self, product)

            if factor is not None:
                singleton_factors.append(factor)

        for factor in singleton_factors:
            if not isinstance(factor, MasseyProduct) or len(factor.inputs) < 3:
                continue

            aliases = [
                other
                for other in singleton_factors
                if _tower_factor_key(self, other) != _tower_factor_key(self, factor)
            ]
            remember(factor.inputs, aliases=aliases)

    return list(candidates.values())


def _tower_has_concrete_primitive(self, inputs):
    """
    Primitive-existence check for tower completion.

    This deliberately avoids the full bridge-replacement primitive search: that
    search can become too expensive inside tower inference.  Instead we accept
    directly recorded primitives plus one-step bridge aliases to directly
    recorded primitives.
    """

    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    cache_key = (
        tuple(repr(self.mp_factor_key(x)) for x in inputs),
        _tower_cache_state_signature(self),
    )
    cache = getattr(self, "_tower_concrete_primitive_cache", {})

    if cache_key in cache:
        return cache[cache_key]

    primitive_keys_for_tower = None

    def has_recorded_primitive(block_inputs):
        nonlocal primitive_keys_for_tower

        block_inputs = tuple(self.normalize_mp_inputs(tuple(block_inputs)))

        if len(block_inputs) == 1:
            item = block_inputs[0]

            if not isinstance(item, MasseyProduct) or len(item.inputs) <= 1:
                return False

            block_inputs = tuple(self.normalize_mp_inputs(item.inputs))

        try:
            key = _fast_mp_key(self, block_inputs)

            if primitive_keys_for_tower is None:
                primitive_keys_for_tower, _records, _source_by_key = (
                    _fast_known_mp_primitive_records(self)
                )

            return key in primitive_keys_for_tower
        except Exception:
            return False

    def product_block_has_recorded_primitive(factors):
        factors = tuple(factors)

        if not factors:
            return False

        if len(factors) == 1 and isinstance(factors[0], MasseyProduct):
            if len(factors[0].inputs) <= 1:
                return False

            return has_recorded_primitive(factors[0].inputs)

        try:
            block_key = self.mp_product_block_key(factors)
        except Exception:
            return False

        return has_recorded_primitive(block_key)

    has_primitive = has_recorded_primitive(inputs)

    if not has_primitive:
        target_keys = set()

        try:
            if len(inputs) >= 3:
                key = self.mp_key(*inputs)
                M = getattr(self, "massey_products", {}).get(key, None)

                if M is None:
                    M = MasseyProduct(self, key)

                target_keys.add(self.mp_product_key(M.as_product()))
        except Exception:
            pass

        try:
            factors = self.canonical_mp_factors(inputs)
            target_keys.add(self.mp_product_key(MPProduct(self, factors)))
        except Exception:
            pass

        for expression in getattr(self, "bridge_expressions", {}).values():
            if not isinstance(expression, MPElement):
                continue

            terms = list(expression.terms.keys())
            matching_products = [
                product
                for product in terms
                if self.mp_product_key(product) in target_keys
            ]

            if not matching_products:
                continue

            for product in terms:
                if product in matching_products:
                    continue

                try:
                    replacement_factors = self.canonical_mp_factors(product)
                except Exception:
                    continue

                if product_block_has_recorded_primitive(replacement_factors):
                    has_primitive = True
                    break

            if has_primitive:
                break

    cache[cache_key] = has_primitive
    self._tower_concrete_primitive_cache = cache

    return has_primitive


def _tower_cache_state_signature(self):
    return (
        len(getattr(self, "resolved_massey_products", {})),
        len(getattr(self, "resolved_mp_expressions", {})),
        len(getattr(self, "bridge_expressions", {})),
        tuple(sorted(id(value) for value in getattr(self, "bridge_expressions", {}).values())),
        len(getattr(self, "cells", {})),
        len(getattr(self, "attachment_history", [])),
    )


def _tower_can_define_mp_from_concrete_primitives(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    n = len(inputs)

    if n == 0:
        return False

    if self.has_zero_mp_input(inputs):
        return True

    if n == 1:
        return True

    if n == 2:
        return self.are_composable(inputs[0], inputs[1])

    for subkey in self.required_lower_mps(*inputs):
        if not _tower_has_concrete_primitive(self, subkey):
            return False

    return True


def _completed_tower_record_for_seed(self, seed_inputs, aliases=()):
    seed_inputs = tuple(self.normalize_mp_inputs(tuple(seed_inputs)))

    if len(seed_inputs) < 3:
        return None

    rotations = self.cyclic_rotations(seed_inputs)

    if not rotations:
        return None

    base_records = []

    for offset, rotation in enumerate(rotations):
        try:
            defined = _tower_can_define_mp_from_concrete_primitives(
                self,
                rotation,
            )
        except Exception:
            defined = False

        has_primitive = _tower_has_concrete_primitive(self, rotation)
        base_records.append({
            "offset": offset,
            "inputs": rotation,
            "defined": defined,
            "has_primitive": has_primitive,
            "directly_resolved": self.mp_key(*rotation) in getattr(self, "resolved_massey_products", {}),
            "is_leave": offset == 0,
            "is_center": offset == 0,
            "in_tower": offset != 0,
        })

    if any(not record["has_primitive"] for record in base_records[1:]):
        return None

    run_length = len(seed_inputs) - 1

    tower_levels = [{
        "level": 1,
        "arity": len(seed_inputs),
        "candidates": [
            {
                "level": 1,
                "arity": len(seed_inputs),
                "offset": record["offset"],
                "inputs": record["inputs"],
                "key": self.mp_key(*record["inputs"]),
                "has_primitive": record["has_primitive"],
                "directly_resolved": record["directly_resolved"],
                "defined": record["defined"],
            }
            for record in base_records[1:]
        ],
    }]
    levels = []

    for definition_level in range(2, len(seed_inputs)):
        arity = len(seed_inputs) + definition_level - 1
        count = len(seed_inputs) - definition_level
        level_items = []

        for offset in range(1, count + 1):
            inputs = _massey_tower_cyclic_word(seed_inputs, offset, arity)
            has_primitive = _tower_has_concrete_primitive(self, inputs)
            level_items.append({
                "level": definition_level,
                "arity": arity,
                "offset": offset,
                "inputs": inputs,
                "key": self.mp_key(*inputs),
                "has_primitive": has_primitive,
                "directly_resolved": self.mp_key(*inputs) in getattr(self, "resolved_massey_products", {}),
            })

        tower_levels.append({
            "level": definition_level,
            "arity": arity,
            "candidates": level_items,
        })
        levels.append({
            "level": definition_level - 1,
            "definition_level": definition_level,
            "arity": arity,
            "candidates": level_items,
        })

    if any(
        not item["has_primitive"]
        for level in tower_levels
        for item in level["candidates"]
    ):
        return None

    aliases = tuple(aliases)

    return {
        "seed_inputs": seed_inputs,
        "seed_key": self.mp_key(*seed_inputs),
        "aliases": aliases,
        "alias_keys": tuple(_tower_factor_key(self, alias) for alias in aliases),
        "run_length": run_length,
        "base_rotations": base_records,
        "tower_levels": tower_levels,
        "levels": levels,
    }


def _completed_tower_record_key(self, record):
    seed_inputs = tuple(record.get("seed_inputs", ()))
    return (
        "completed_massey_tower",
        tuple(repr(_tower_factor_key(self, factor)) for factor in seed_inputs),
    )


def _completed_tower_record_summary(self, record):
    seed_inputs = tuple(record.get("seed_inputs", ()))
    tower_levels = tuple(record.get("tower_levels", ()))
    levels = tuple(record.get("levels", ()))
    highest_level = max(
        (
            int(level.get("level", 0) or 0)
            for level in (tower_levels or levels)
        ),
        default=0,
    )
    higher_count = sum(
        len(tuple(level.get("candidates", ())))
        for level in levels
    )
    base_count = len([
        item
        for item in record.get("base_rotations", ())
        if item.get("in_tower", not item.get("is_leave"))
    ])

    return {
        "key": _completed_tower_record_key(self, record),
        "seed_inputs": seed_inputs,
        "seed_key": record.get("seed_key"),
        "aliases": tuple(record.get("aliases", ())),
        "alias_keys": tuple(record.get("alias_keys", ())),
        "run_length": record.get("run_length", 0),
        "base_resolution_count": base_count,
        "higher_resolution_count": higher_count,
        "total_resolution_count": base_count + higher_count,
        "top_arity": (
            len(seed_inputs) + highest_level - 1
            if tower_levels
            else len(seed_inputs) + highest_level
        ),
    }


def record_completed_massey_towers(self, records=None):
    """
    Refresh the durable list of completed pointed-tower detections.

    Detection itself is inferred from the current state and remains virtual:
    this records that the tower has been seen, without adding primitives or
    cells.  Previously seen towers stay in history and are marked inactive if
    undo removes the data that completed them.
    """

    if records is None:
        records = self.completed_massey_tower_elimination_records(record=False)

    records = list(records or [])
    current_keys = {
        _completed_tower_record_key(self, record)
        for record in records
    }
    history = getattr(self, "completed_massey_tower_history", None)

    if history is None:
        history = []
        self.completed_massey_tower_history = history

    by_key = {
        entry.get("key"): entry
        for entry in history
    }
    new_records = []
    current_entries = []

    for record in records:
        key = _completed_tower_record_key(self, record)
        summary = _completed_tower_record_summary(self, record)
        entry = by_key.get(key)

        if entry is None:
            entry = {
                **summary,
                "record": record,
                "first_seen_attachment_history_length": len(getattr(self, "attachment_history", [])),
                "active": True,
            }
            history.append(entry)
            by_key[key] = entry
            new_records.append(record)
        else:
            entry.update(summary)
            entry["record"] = record
            entry["active"] = True

        current_entries.append(entry)

    for entry in history:
        entry["active"] = entry.get("key") in current_keys

    return {
        "records": records,
        "new_records": new_records,
        "current_entries": current_entries,
        "history": history,
    }


def completed_massey_tower_elimination_records(self, record=True):
    """
    Infer completed isolated-tower records from the current resolved state.

    A record is purely virtual: it says that nested products supported on the
    seed's periodic word are already killed by the completed pointed tower.  It
    does not add anything to resolved_massey_products.
    """

    cache_key = (
        _tower_cache_state_signature(self),
        len(getattr(self, "massey_products", {})),
    )
    cache = getattr(self, "_completed_massey_tower_elimination_cache", None)

    if cache is not None and cache.get("key") == cache_key:
        records = cache.get("records", [])

        if record:
            record_completed_massey_towers(self, records=records)

        return records

    records = []

    for candidate in _tower_seed_candidates(self):
        record = _completed_tower_record_for_seed(
            self,
            candidate["seed_inputs"],
            aliases=candidate.get("aliases", ()),
        )

        if record is None:
            continue

        records.append(record)

    self._completed_massey_tower_elimination_cache = {
        "key": cache_key,
        "records": records,
    }

    if record:
        record_completed_massey_towers(self, records=records)

    return records


def _tower_flatten_factor_options(self, factor, record, max_options):
    seed_inputs = tuple(record["seed_inputs"])
    seed_key = record["seed_key"]
    alias_keys = set(record.get("alias_keys", ()))
    factor = self.normalize_mp_input(factor)
    factor_key = _tower_factor_key(self, factor)

    if isinstance(factor, MasseyProduct):
        inner_inputs = tuple(self.normalize_mp_inputs(factor.inputs))

        if self.mp_key(*inner_inputs) == seed_key:
            return [(seed_inputs, True)]

        options = []
        if factor_key in alias_keys:
            options.append((seed_inputs, True))

        options.append(((factor,), False))

        seed_input_keys = {
            _tower_factor_key(self, seed_factor)
            for seed_factor in seed_inputs
        }

        if factor_key in seed_input_keys:
            return options

        options.extend([
            (word, True)
            for word, _used in _tower_flatten_input_options(
                self,
                inner_inputs,
                record,
                max_options=max_options,
            )
        ])
        return options

    options = []

    if factor_key in alias_keys:
        options.append((seed_inputs, True))

    options.append(((factor,), False))

    return options


def _tower_flatten_input_options(self, inputs, record, max_options=256):
    options = [((), False)]

    for factor in tuple(inputs):
        factor_options = _tower_flatten_factor_options(
            self,
            factor,
            record,
            max_options=max_options,
        )
        next_options = []

        for prefix, prefix_used in options:
            for word, used in factor_options:
                next_options.append((prefix + tuple(word), prefix_used or used))

                if len(next_options) >= max_options:
                    break

            if len(next_options) >= max_options:
                break

        options = next_options

        if not options:
            break

    return options


def _tower_alias_presentation_options(self, inputs, record, max_options=64):
    seed_massey = _tower_record_seed_massey_factor(self, record)

    if seed_massey is None:
        return ()

    seed_key = record.get("seed_key")
    alias_keys = set(record.get("alias_keys", ()))
    options = [((), False, 0, ())]

    for factor_index, factor in enumerate(tuple(inputs)):
        factor = self.normalize_mp_input(factor)
        factor_key = _tower_factor_key(self, factor)
        factor_options = [((factor,), False, 0, ())]

        if factor_key in alias_keys:
            factor_options.append(((seed_massey,), True, 1, (factor_index,)))

        if isinstance(factor, MasseyProduct):
            try:
                factor_inputs = tuple(self.normalize_mp_inputs(tuple(factor.inputs)))
                is_seed = self.mp_key(*factor_inputs) == seed_key
            except Exception:
                is_seed = False

            if is_seed:
                factor_options = [((factor,), True, 0, ())]

        next_options = []

        for prefix, prefix_used, prefix_count, prefix_positions in options:
            for word, used, count, positions in factor_options:
                next_options.append((
                    prefix + tuple(word),
                    prefix_used or used,
                    prefix_count + count,
                    prefix_positions + positions,
                ))

                if len(next_options) >= max_options:
                    break

            if len(next_options) >= max_options:
                break

        options = next_options

        if not options:
            break

    options = sorted(
        options,
        key=lambda option: (
            not option[1],
            option[2],
            option[3],
        ),
    )

    return tuple((word, used) for word, used, _count, _positions in options)


def _tower_alias_stasheff_zero_report(self, inputs, record):
    if getattr(self, "_suppress_tower_alias_stasheff_zero", False):
        allowed_below_arity = getattr(
            self,
            "_tower_alias_stasheff_zero_allowed_below_arity",
            None,
        )

        try:
            allowed_below_arity = int(allowed_below_arity)
        except (TypeError, ValueError):
            allowed_below_arity = None

        if allowed_below_arity is None or len(tuple(inputs)) >= allowed_below_arity:
            return None

        if not any(isinstance(factor, MasseyProduct) for factor in tuple(inputs)):
            return None

    try:
        seed_inputs = tuple(record.get("seed_inputs", ()) or ())

        if (
            len(tuple(inputs)) == len(seed_inputs)
            and _tower_word_keys(self, inputs) == _tower_word_keys(self, seed_inputs)
        ):
            return None

        cache_key = (
            tuple(repr(self.mp_factor_key(item)) for item in tuple(inputs)),
            _completed_tower_record_key(self, record),
            _tower_cache_state_signature(self),
            _ainf_outer_arity_limit(self) == 0,
        )
    except Exception:
        cache_key = None

    cache = getattr(self, "_tower_alias_stasheff_zero_cache", None)

    if cache is None:
        cache = {}
        self._tower_alias_stasheff_zero_cache = cache

    if cache_key is not None and cache_key in cache:
        return cache[cache_key]

    def remember(report):
        if cache_key is not None:
            cache[cache_key] = report

        return report

    for presentation_inputs, used_alias in _tower_alias_presentation_options(
        self,
        inputs,
        record,
    ):
        if not used_alias:
            continue

        had_limit = hasattr(self, "ainf_replacement_max_outer_arity")
        old_limit = getattr(self, "ainf_replacement_max_outer_arity", None)
        limit = _ainf_outer_arity_limit(self)

        if limit == 0:
            continue

        if limit is not None and limit < len(tuple(presentation_inputs)):
            self.ainf_replacement_max_outer_arity = len(tuple(presentation_inputs))

        try:
            zero_report = _stasheff_zero_massey_presentation_report(
                self,
                presentation_inputs,
            )
        finally:
            if had_limit:
                self.ainf_replacement_max_outer_arity = old_limit
            elif hasattr(self, "ainf_replacement_max_outer_arity"):
                delattr(self, "ainf_replacement_max_outer_arity")

        if zero_report is None:
            continue

        return remember({
            "eliminated": True,
            "inputs": inputs,
            "flat_word": tuple(zero_report.get("flattened_inputs", ())),
            "seed_inputs": tuple(record.get("seed_inputs", ())),
            "aliases": tuple(record.get("aliases", ())),
            "record": record,
            "source": "tower_alias_stasheff_zero",
            "equivalent_inputs": presentation_inputs,
            "stasheff_zero": zero_report,
        })

    return remember(None)


def tower_elimination_report(self, *inputs, records=None):
    """
    Return the completed-tower record eliminating inputs, or None.

    The test is word-level.  It expands nested Massey inputs and any bridge
    alias for the isolated seed, then checks whether the resulting generator
    word is a periodic subword of the isolated class.  A pure periodic word is
    recognized once it is longer than the seed; shorter consequences still need
    a nested/alias occurrence so the unresolved seed itself is not killed.
    """

    inputs = tuple(self.normalize_mp_inputs(_tower_coerce_inputs(inputs)))

    if records is None:
        records = self.completed_massey_tower_elimination_records()

    for record in records:
        seed_inputs = tuple(record["seed_inputs"])

        for flat_word, used_inner in _tower_flatten_input_options(
            self,
            inputs,
            record,
        ):
            if not used_inner and len(flat_word) <= len(seed_inputs):
                continue

            if not _tower_word_is_periodic_subword(self, flat_word, seed_inputs):
                continue

            return {
                "eliminated": True,
                "inputs": inputs,
                "flat_word": flat_word,
                "seed_inputs": seed_inputs,
                "aliases": tuple(record.get("aliases", ())),
                "record": record,
            }

        alias_zero_report = _tower_alias_stasheff_zero_report(
            self,
            inputs,
            record,
        )

        if alias_zero_report is not None:
            return alias_zero_report

    return None


def _tower_word_keys(self, word):
    return tuple(_tower_factor_key(self, factor) for factor in tuple(word))


def _tower_word_contains_subword(self, word, subword):
    word_keys = _tower_word_keys(self, word)
    subword_keys = _tower_word_keys(self, subword)
    subword_len = len(subword_keys)

    if subword_len == 0 or len(word_keys) < subword_len:
        return False

    return any(
        word_keys[start:start + subword_len] == subword_keys
        for start in range(0, len(word_keys) - subword_len + 1)
    )


def _paired_tower_boundary_split(self, word, left_seed, right_seed):
    word_keys = _tower_word_keys(self, word)
    left_keys = _tower_word_keys(self, left_seed)
    right_keys = _tower_word_keys(self, right_seed)

    if len(word_keys) < 2 or not left_keys or not right_keys:
        return None

    left_len = len(left_keys)
    right_len = len(right_keys)

    for split in range(1, len(word_keys)):
        left_part = word_keys[:split]
        right_part = word_keys[split:]

        left_matches = all(
            key == left_keys[(left_len - len(left_part) + index) % left_len]
            for index, key in enumerate(left_part)
        )
        if not left_matches:
            continue

        right_matches = all(
            key == right_keys[index % right_len]
            for index, key in enumerate(right_part)
        )
        if right_matches:
            return split

    return None


def _pair_tower_block_has_hypothesis_certificate(
    self,
    block,
    tower_records,
):
    block = tuple(self.normalize_mp_inputs(tuple(block)))

    if len(block) < 2:
        return True

    if self.has_zero_mp_input(block):
        return True

    if not _fast_key_is_composable(self, block):
        return False

    try:
        if _tower_has_concrete_primitive(self, block):
            return True
    except Exception:
        pass

    had_guard = hasattr(self, "_suppress_tower_alias_stasheff_zero")
    old_guard = getattr(self, "_suppress_tower_alias_stasheff_zero", False)
    self._suppress_tower_alias_stasheff_zero = True

    try:
        try:
            if self.tower_elimination_report(
                *block,
                records=tower_records,
            ) is not None:
                return True
        except Exception:
            pass
    finally:
        if had_guard:
            self._suppress_tower_alias_stasheff_zero = old_guard
        elif hasattr(self, "_suppress_tower_alias_stasheff_zero"):
            delattr(self, "_suppress_tower_alias_stasheff_zero")

    try:
        if _fast_block_has_bridge_replacement_certificate(self, block):
            return True
    except Exception:
        pass

    return False


def _pair_tower_hypothesis_checks(self, left_seed, right_seed, tower_records):
    left_seed = tuple(self.normalize_mp_inputs(tuple(left_seed)))
    right_seed = tuple(self.normalize_mp_inputs(tuple(right_seed)))
    concatenated = left_seed + right_seed
    checks = []

    if len(left_seed) < 2 or len(right_seed) < 2:
        return None

    if not _fast_key_is_composable(self, concatenated):
        return None

    for start in range(0, len(concatenated)):
        for stop in range(start + 2, len(concatenated) + 1):
            window = concatenated[start:stop]

            if (
                _tower_word_contains_subword(self, window, left_seed)
                or _tower_word_contains_subword(self, window, right_seed)
            ):
                continue

            has_certificate = _pair_tower_block_has_hypothesis_certificate(
                self,
                window,
                tower_records,
            )
            checks.append({
                "start": start,
                "stop": stop,
                "inputs": window,
                "has_primitive": has_certificate,
            })

            if not has_certificate:
                return None

    return tuple(checks)


def _completed_pair_tower_record_key(self, record):
    return (
        "completed_massey_pair_tower",
        _completed_tower_record_key(self, record.get("left_record", {})),
        _completed_tower_record_key(self, record.get("right_record", {})),
    )


def completed_massey_pair_tower_elimination_records(
    self,
    tower_records=None,
):
    """
    Infer ordered pairs of completed towers whose mixed boundary is killed.

    The hypotheses are checked only against already available primitive/tower/
    bridge certificates, never against pair-tower certificates themselves.
    """

    if tower_records is None:
        try:
            tower_records = self.completed_massey_tower_elimination_records(
                record=False,
            )
        except Exception:
            tower_records = ()

    tower_records = tuple(tower_records or ())
    cache_key = (
        _tower_cache_state_signature(self),
        len(getattr(self, "massey_products", {})),
        tuple(_completed_tower_record_key(self, record) for record in tower_records),
    )
    cache = getattr(self, "_completed_massey_pair_tower_elimination_cache", None)

    if cache is not None and cache.get("key") == cache_key:
        return list(cache.get("records", ()))

    records = []
    seen = set()

    for left_record in tower_records:
        left_seed = tuple(left_record.get("seed_inputs", ()))

        if len(left_seed) < 3:
            continue

        for right_record in tower_records:
            right_seed = tuple(right_record.get("seed_inputs", ()))

            if len(right_seed) < 3:
                continue

            pair_key = (
                _completed_tower_record_key(self, left_record),
                _completed_tower_record_key(self, right_record),
            )

            if pair_key in seen:
                continue

            seen.add(pair_key)
            checks = _pair_tower_hypothesis_checks(
                self,
                left_seed,
                right_seed,
                tower_records,
            )

            if checks is None:
                continue

            records.append({
                "left_record": left_record,
                "right_record": right_record,
                "left_seed_inputs": left_seed,
                "right_seed_inputs": right_seed,
                "ordered_seed_inputs": left_seed + right_seed,
                "hypothesis_checks": checks,
            })

    self._completed_massey_pair_tower_elimination_cache = {
        "key": cache_key,
        "records": records,
    }
    return list(records)


def _pair_tower_flatten_factor_options(
    self,
    factor,
    pair_record,
    max_options,
    include_aliases=False,
    seen_inputs=None,
):
    factor = self.normalize_mp_input(factor)
    left_record = pair_record.get("left_record", {})
    right_record = pair_record.get("right_record", {})
    options = []
    seen_options = set()

    def remember(word, used_left, used_right):
        word = tuple(self.normalize_mp_inputs(tuple(word)))

        if not word:
            return

        key = (
            tuple(repr(self.mp_factor_key(item)) for item in word),
            bool(used_left),
            bool(used_right),
        )

        if key in seen_options:
            return

        seen_options.add(key)
        options.append((word, bool(used_left), bool(used_right)))

    remember((factor,), False, False)

    for side, record in (("left", left_record), ("right", right_record)):
        if include_aliases:
            try:
                factor_options = _tower_flatten_factor_options(
                    self,
                    factor,
                    record,
                    max_options=max_options,
                )
            except Exception:
                factor_options = ()
        else:
            factor_options = ()

            if isinstance(factor, MasseyProduct):
                try:
                    inner_inputs = tuple(self.normalize_mp_inputs(factor.inputs))
                    if self.mp_key(*inner_inputs) == record.get("seed_key"):
                        factor_options = ((tuple(record.get("seed_inputs", ())), True),)
                except Exception:
                    factor_options = ()

        for word, used_inner in factor_options:
            if not used_inner:
                continue

            remember(word, side == "left", side == "right")

            if len(options) >= max_options:
                return options

    if isinstance(factor, MasseyProduct):
        if seen_inputs is None:
            seen_inputs = set()

        try:
            input_key = repr(self.mp_key(*factor.inputs))
        except Exception:
            input_key = repr(tuple(factor.inputs))

        if input_key not in seen_inputs:
            nested_seen = set(seen_inputs)
            nested_seen.add(input_key)

            for word, used_left, used_right in _pair_tower_flatten_input_options(
                self,
                factor.inputs,
                pair_record,
                max_options=max_options,
                include_aliases=include_aliases,
                seen_inputs=nested_seen,
            ):
                if not (used_left or used_right):
                    continue

                remember(word, used_left, used_right)

                if len(options) >= max_options:
                    return options

    return options


def _pair_tower_flatten_input_options(
    self,
    inputs,
    pair_record,
    max_options=256,
    include_aliases=False,
    seen_inputs=None,
):
    options = [((), False, False)]

    for factor in tuple(inputs):
        factor_options = _pair_tower_flatten_factor_options(
            self,
            factor,
            pair_record,
            max_options=max_options,
            include_aliases=include_aliases,
            seen_inputs=seen_inputs,
        )
        next_options = []

        for prefix, prefix_left, prefix_right in options:
            for word, used_left, used_right in factor_options:
                next_options.append((
                    prefix + tuple(word),
                    prefix_left or used_left,
                    prefix_right or used_right,
                ))

                if len(next_options) >= max_options:
                    break

            if len(next_options) >= max_options:
                break

        options = next_options

        if not options:
            break

    return options


def pair_tower_elimination_report(
    self,
    *inputs,
    pair_records=None,
    tower_records=None,
    include_aliases=False,
):
    inputs = tuple(self.normalize_mp_inputs(_tower_coerce_inputs(inputs)))
    cache_key = None

    if pair_records is None and tower_records is None:
        try:
            cache_key = (
                tuple(repr(self.mp_factor_key(item)) for item in inputs),
                bool(include_aliases),
                _tower_cache_state_signature(self),
                len(getattr(self, "massey_products", {})),
            )
        except Exception:
            cache_key = None

    cache = getattr(self, "_pair_tower_elimination_report_cache", None)

    if cache_key is not None:
        if cache is None:
            cache = {}
            self._pair_tower_elimination_report_cache = cache
        elif cache_key in cache:
            return cache[cache_key]

    def remember(result):
        if cache_key is not None:
            cache[cache_key] = result
        return result

    if len(inputs) < 2:
        return remember(None)

    if tower_records is None:
        try:
            tower_records = self.completed_massey_tower_elimination_records(
                record=False,
            )
        except Exception:
            tower_records = ()

    if pair_records is None:
        pair_records = self.completed_massey_pair_tower_elimination_records(
            tower_records=tower_records,
        )

    for record in tuple(pair_records or ()):
        left_seed = tuple(record.get("left_seed_inputs", ()))
        right_seed = tuple(record.get("right_seed_inputs", ()))

        for flat_word, used_left, used_right in _pair_tower_flatten_input_options(
            self,
            inputs,
            record,
            include_aliases=include_aliases,
        ):
            boundary_split = _paired_tower_boundary_split(
                self,
                flat_word,
                left_seed,
                right_seed,
            )

            if boundary_split is None:
                continue

            contains_center = (
                _tower_word_contains_subword(self, flat_word, left_seed)
                or _tower_word_contains_subword(self, flat_word, right_seed)
            )

            if not (used_left or used_right or contains_center):
                continue

            return remember({
                "eliminated": True,
                "source": "completed_massey_pair_tower",
                "inputs": inputs,
                "flat_word": flat_word,
                "boundary_split": boundary_split,
                "left_seed_inputs": left_seed,
                "right_seed_inputs": right_seed,
                "used_left_tower_center": bool(used_left),
                "used_right_tower_center": bool(used_right),
                "record": record,
            })

    return remember(None)


def is_pair_tower_eliminated_mp(self, *inputs, pair_records=None):
    return pair_tower_elimination_report(
        self,
        *inputs,
        pair_records=pair_records,
    ) is not None


def _tower_elimination_report_with_replacements(self, inputs, records=None):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    direct_report = self.tower_elimination_report(*inputs, records=records)

    if direct_report is not None:
        return direct_report

    try:
        factors = self.canonical_mp_factors(tuple(inputs))
    except Exception:
        return None

    if len(factors) < 2:
        return None

    resolution = _tower_replacement_resolution_for_product_block(self, factors)

    if resolution is None:
        return None

    tower_report = resolution.get("tower_report")

    if not isinstance(tower_report, dict):
        return None

    seed_inputs = tuple(tower_report.get("seed_inputs", ()) or ())

    if (
        seed_inputs
        and len(inputs) == len(seed_inputs)
        and _tower_word_is_periodic_subword(self, inputs, seed_inputs)
    ):
        return None

    report = dict(tower_report)
    report.update({
        "inputs": inputs,
        "original_factors": tuple(resolution.get("original_factors", factors)),
        "presentation_factors": tuple(resolution.get("presentation_factors", ())),
        "bridge_path": tuple(resolution.get("bridge_path", ())),
        "replacement_used": bool(resolution.get("bridge_path", ())),
    })
    return report


def _tower_resolution_cache_key(self, inputs):
    return (
        tuple(repr(self.mp_factor_key(item)) for item in tuple(inputs)),
        _tower_cache_state_signature(self),
        getattr(self, "ainf_replacement_max_outer_arity", 3),
    )


def _cached_tower_elimination_report_with_replacements(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    key = _tower_resolution_cache_key(self, inputs)
    cache = getattr(self, "_tower_resolution_with_replacements_cache", None)

    if cache is None:
        cache = {}
        self._tower_resolution_with_replacements_cache = cache

    if key not in cache:
        cache[key] = _tower_elimination_report_with_replacements(self, inputs)

    return cache[key]


def is_tower_eliminated_mp(self, *inputs, records=None):
    inputs = tuple(self.normalize_mp_inputs(_tower_coerce_inputs(inputs)))

    if records is None:
        return _cached_tower_elimination_report_with_replacements(
            self,
            inputs,
        ) is not None

    return _tower_elimination_report_with_replacements(
        self,
        inputs,
        records=records,
    ) is not None


def _virtual_tower_primitive_candidate(self, factors, start, stop, block_key, report):
    return {
        "kind": "completed_massey_tower",
        "virtual_primitive": True,
        "source": "completed_massey_tower",
        "left": tuple(factors[:start]),
        "primitive": None,
        "right": tuple(factors[stop:]),
        "block": tuple(factors[start:stop]),
        "block_key": tuple(block_key),
        "sign_source": tuple(factors[:start]),
        "tower_report": report,
        "tower_record": report.get("record"),
        "flat_word": tuple(report.get("flat_word", ())),
        "seed_inputs": tuple(report.get("seed_inputs", ())),
        "aliases": tuple(report.get("aliases", ())),
    }


def _virtual_pair_tower_primitive_candidate(
    self,
    factors,
    start,
    stop,
    block_key,
    report,
):
    return {
        "kind": "completed_massey_pair_tower",
        "virtual_primitive": True,
        "source": "completed_massey_pair_tower",
        "left": tuple(factors[:start]),
        "primitive": None,
        "right": tuple(factors[stop:]),
        "block": tuple(factors[start:stop]),
        "block_key": tuple(block_key),
        "sign_source": tuple(factors[:start]),
        "pair_tower_report": report,
        "pair_tower_record": report.get("record"),
        "flat_word": tuple(report.get("flat_word", ())),
        "left_seed_inputs": tuple(report.get("left_seed_inputs", ())),
        "right_seed_inputs": tuple(report.get("right_seed_inputs", ())),
        "boundary_split": report.get("boundary_split"),
    }


def _virtual_tower_or_pair_report(self, block_key, tower_records, pair_records):
    tower_report = self.tower_elimination_report(
        *block_key,
        records=tower_records,
    )

    if tower_report is not None:
        return ("tower", tower_report)

    pair_report = self.pair_tower_elimination_report(
        *block_key,
        tower_records=tower_records,
        pair_records=pair_records,
    )

    if pair_report is not None:
        return ("pair_tower", pair_report)

    return (None, None)


def _virtual_tower_primitive_candidates_for_product(self, P, minimal_only=True):
    if getattr(self, "skip_deep_tower_resolution", False):
        return []

    if isinstance(P, MasseyProduct):
        P = P.as_product()

    if not isinstance(P, MPProduct):
        return []

    factors = tuple(P.factors)
    n = len(factors)
    candidates = []

    try:
        tower_records = self.completed_massey_tower_elimination_records(
            record=False,
        )
    except Exception:
        tower_records = ()

    try:
        pair_records = self.completed_massey_pair_tower_elimination_records(
            tower_records=tower_records,
        )
    except Exception:
        pair_records = ()

    for start in range(n):
        for stop in range(start + 1, n + 1):
            block = factors[start:stop]

            if len(block) == 1:
                factor = block[0]

                if not isinstance(factor, MasseyProduct):
                    continue

                if len(factor.inputs) == 1:
                    continue

                block_key = self.mp_key(*factor.inputs)
            else:
                block_key = self.mp_product_block_key(block)

            report_kind, report = _virtual_tower_or_pair_report(
                self,
                block_key,
                tower_records,
                pair_records,
            )

            if report is None:
                continue

            if minimal_only and len(block) > 1:
                has_smaller_virtual = False

                for sub_start in range(start, stop):
                    for sub_stop in range(sub_start + 1, stop + 1):
                        if sub_start == start and sub_stop == stop:
                            continue

                        subblock = factors[sub_start:sub_stop]

                        if len(subblock) == 1:
                            subfactor = subblock[0]

                            if not isinstance(subfactor, MasseyProduct):
                                continue

                            if len(subfactor.inputs) == 1:
                                continue

                            subkey = self.mp_key(*subfactor.inputs)
                        else:
                            subkey = self.mp_product_block_key(subblock)

                        sub_report_kind, _sub_report = (
                            _virtual_tower_or_pair_report(
                                self,
                                subkey,
                                tower_records,
                                pair_records,
                            )
                        )

                        if sub_report_kind is not None:
                            has_smaller_virtual = True
                            break

                    if has_smaller_virtual:
                        break

                if has_smaller_virtual:
                    continue

            if report_kind == "pair_tower":
                candidates.append(
                    _virtual_pair_tower_primitive_candidate(
                        self,
                        factors,
                        start,
                        stop,
                        block_key,
                        report,
                    )
                )
            else:
                candidates.append(
                    _virtual_tower_primitive_candidate(
                        self,
                        factors,
                        start,
                        stop,
                        block_key,
                        report,
                    )
                )

    return candidates


def _record_virtual_tower_primitive_use(self, candidate):
    history = getattr(self, "completed_massey_tower_primitive_uses", None)

    if history is None:
        history = []
        self.completed_massey_tower_primitive_uses = history

    key = (
        tuple(repr(self.mp_factor_key(factor)) for factor in tuple(candidate.get("block", ()))),
        tuple(repr(self.mp_factor_key(factor)) for factor in tuple(candidate.get("flat_word", ()))),
        _completed_tower_record_key(self, candidate.get("tower_record", {})),
    )

    for entry in history:
        if entry.get("key") == key:
            entry["last_seen_attachment_history_length"] = len(getattr(self, "attachment_history", []))
            return entry

    entry = {
        "key": key,
        "block": tuple(candidate.get("block", ())),
        "block_key": tuple(candidate.get("block_key", ())),
        "flat_word": tuple(candidate.get("flat_word", ())),
        "seed_inputs": tuple(candidate.get("seed_inputs", ())),
        "tower_record_key": _completed_tower_record_key(self, candidate.get("tower_record", {})),
        "first_seen_attachment_history_length": len(getattr(self, "attachment_history", [])),
        "last_seen_attachment_history_length": len(getattr(self, "attachment_history", [])),
    }
    history.append(entry)
    return entry


def find_primitives_mp_product(
    self,
    P,
    record=True,
    minimal_only=True,
    use_bridge_replacements=True,
    include_virtual_tower_primitives=None,
):
    """
    Find primitive candidates, adding virtual completed-tower certificates.

    Virtual candidates are existence records only.  They tell generation and
    definability that the block has a primitive by the completed tower lemma,
    without storing or expanding an actual primitive formula.
    """

    if getattr(self, "_suppress_primitive_expansion", False):
        primitive_keys, _primitive_records, source_by_key = _fast_known_mp_primitive_records(self)
        tower_records = _fast_tower_records(self)
        candidates = list(_fast_primitive_candidates_for_product(
            self,
            P,
            primitive_keys=primitive_keys,
            source_by_key=source_by_key,
            tower_records=tower_records,
            minimal_only=minimal_only,
        ))

        if use_bridge_replacements:
            candidates.extend(self.bridge_replacement_primitive_candidates(
                P,
                record=False,
                minimal_only=minimal_only,
            ))

        if record:
            try:
                factors = tuple(P.as_product().factors) if isinstance(P, MasseyProduct) else tuple(P.factors)
                self.mp_primitive_candidates[factors] = candidates
            except Exception:
                pass

        return candidates

    base = getattr(
        type(self),
        "_cyclic_base_find_primitives_mp_product",
        None,
    )

    if base is None:
        candidates = []
    else:
        candidates = list(base(
            self,
            P,
            record=False,
            minimal_only=minimal_only,
            use_bridge_replacements=use_bridge_replacements,
        ))

    if include_virtual_tower_primitives is None:
        include_virtual_tower_primitives = use_bridge_replacements

    if include_virtual_tower_primitives:
        try:
            virtual_candidates = _virtual_tower_primitive_candidates_for_product(
                self,
                P,
                minimal_only=minimal_only,
            )
        except Exception:
            virtual_candidates = []

        seen_spans = {
            (
                len(tuple(candidate.get("left", ()))),
                len(tuple(candidate.get("left", ()))) + len(tuple(candidate.get("block", ()))),
                tuple(self.mp_factor_key(factor) for factor in tuple(candidate.get("block", ()))),
            )
            for candidate in candidates
        }

        for candidate in virtual_candidates:
            span_key = (
                len(tuple(candidate.get("left", ()))),
                len(tuple(candidate.get("left", ()))) + len(tuple(candidate.get("block", ()))),
                tuple(self.mp_factor_key(factor) for factor in tuple(candidate.get("block", ()))),
            )

            if span_key in seen_spans:
                continue

            seen_spans.add(span_key)
            _record_virtual_tower_primitive_use(self, candidate)
            candidates.append(candidate)

    if record:
        try:
            factors = tuple(P.as_product().factors) if isinstance(P, MasseyProduct) else tuple(P.factors)
            self.mp_primitive_candidates[factors] = candidates
        except Exception:
            pass

    return candidates


def primitive_candidate_to_element(self, candidate):
    if isinstance(candidate, dict) and candidate.get("virtual_primitive"):
        return None

    if isinstance(candidate, dict) and candidate.get("deferred_primitive"):
        return None

    base = getattr(
        type(self),
        "_cyclic_base_primitive_candidate_to_element",
        None,
    )

    if base is None:
        return None

    return base(self, candidate)


def _mp_block_has_bridge_replacement_certificate(self, inputs):
    try:
        factors = self.canonical_mp_factors(tuple(inputs))
    except Exception:
        return False

    if len(factors) < 2:
        return False

    candidates = _bridge_replacement_product_resolution_candidates(
        self,
        factors,
        minimal_only=True,
    )

    for candidate in candidates:
        if not (
            candidate.get("minimal")
            and _bridge_candidate_spans_whole_original(candidate, factors)
        ):
            continue

        if len(factors) < 3:
            if _bridge_candidate_uses_pair_tower_source(candidate):
                continue

            return True

        if _bridge_replacement_candidate_is_whole_primitive_certificate(
            self,
            candidate,
            factors,
        ):
            return True

    return False


def _bridge_candidate_uses_pair_tower_source(candidate):
    candidate = candidate if isinstance(candidate, dict) else {}

    if candidate.get("source") == "completed_massey_pair_tower":
        return True

    source_primitive = candidate.get("source_primitive", None)

    if isinstance(source_primitive, dict):
        return source_primitive.get("source") == "completed_massey_pair_tower"

    return False


def _bridge_replacement_candidate_is_whole_primitive_certificate(
    self,
    candidate,
    factors,
):
    if not (
        candidate.get("minimal")
        and _bridge_candidate_spans_whole_original(candidate, factors)
    ):
        return False

    if candidate.get("source") == "completed_massey_tower":
        return False

    if (
        candidate.get("primitive_element") is not None
        and candidate.get("verified", False)
    ):
        return True

    source_primitive = candidate.get("source_primitive", None)

    if not isinstance(source_primitive, dict):
        return False

    source_factors = tuple(candidate.get("source_product_factors", ()))
    primitive_span = candidate.get("primitive_block_span", None)

    if source_factors:
        try:
            primitive_start, primitive_stop = (
                int(primitive_span[0]),
                int(primitive_span[1]),
            )
        except Exception:
            primitive_start = len(tuple(source_primitive.get("left", ())))
            primitive_stop = (
                primitive_start
                + len(tuple(source_primitive.get("block", ())))
            )

        if (primitive_start, primitive_stop) != (0, len(source_factors)):
            return False

    if source_primitive.get("source") in (
        "completed_massey_tower",
    ):
        return True

    return bool(source_primitive.get("termination_count", 0))


def _higher_mp_block_has_obvious_primitive(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return False

    try:
        if not self.can_define_mp(*inputs):
            return False
    except Exception:
        return False

    try:
        key = self.mp_key(*inputs)
        recorded_primitive = getattr(self, "resolved_massey_products", {}).get(
            key,
            None,
        )

        if _is_bridge_promoted_massey_primitive_for_inputs(
            self,
            recorded_primitive,
            inputs,
        ):
            return False

        M = getattr(self, "massey_products", {}).get(key, None)

        if M is None:
            M = MasseyProduct(self, key)

        report = self.classify_massey_product_primitives(
            M,
            record=False,
            minimal_only=True,
            include_primitive_details=False,
        )
    except Exception:
        return False

    return bool(report.get("has_obvious_primitive", False))


def _mp_factor_contains_resolved_higher_massey(self, factor, seen=None):
    if seen is None:
        seen = set()

    factor = self.normalize_mp_input(factor)

    if isinstance(factor, MasseyProduct):
        inputs = tuple(self.normalize_mp_inputs(tuple(factor.inputs)))

        try:
            key = self.mp_key(*inputs)
        except Exception:
            key = tuple(inputs)

        key_token = repr(key)

        if key_token in seen:
            return False

        seen.add(key_token)

        if (
            len(inputs) >= 3
            and key in getattr(self, "resolved_massey_products", {})
        ):
            return True

        return any(
            _mp_factor_contains_resolved_higher_massey(self, item, seen)
            for item in inputs
        )

    if isinstance(factor, MPProduct):
        try:
            factors = tuple(self.canonical_mp_factors(factor))
        except Exception:
            factors = tuple(getattr(factor, "factors", ()))

        return any(
            _mp_factor_contains_resolved_higher_massey(self, item, seen)
            for item in factors
        )

    if isinstance(factor, MPElement):
        for product, coeff in tuple(getattr(factor, "terms", {}).items()):
            if is_zero_coeff(coeff):
                continue

            if _mp_factor_contains_resolved_higher_massey(self, product, seen):
                return True

    return False


def _mp_inputs_contain_resolved_higher_massey(self, inputs):
    return any(
        _mp_factor_contains_resolved_higher_massey(self, item)
        for item in tuple(inputs)
    )


def _fast_block_has_bridge_replacement_certificate(self, inputs):
    try:
        factors = self.canonical_mp_factors(tuple(inputs))
    except Exception:
        return False

    if len(factors) < 2:
        return False

    max_length = getattr(self, "fast_bridge_certificate_max_length", 3)

    try:
        max_length = max(2, int(max_length))
    except (TypeError, ValueError):
        max_length = 3

    if len(factors) > max_length:
        return False

    candidates = _bridge_replacement_product_resolution_candidates(
        self,
        factors,
        minimal_only=True,
    )
    has_bridge_certificate = False

    for candidate in candidates:
        if not (
            candidate.get("minimal")
            and _bridge_candidate_spans_whole_original(candidate, factors)
        ):
            continue

        if len(factors) < 3:
            if candidate.get("source") == "completed_massey_tower":
                continue

            if _bridge_candidate_uses_pair_tower_source(candidate):
                continue

            has_bridge_certificate = True
            continue

        if _bridge_replacement_candidate_is_whole_primitive_certificate(
            self,
            candidate,
            factors,
        ):
            has_bridge_certificate = True

    return has_bridge_certificate


def _mp_block_has_fast_primitive_certificate(
    self,
    inputs,
    allow_bridge_replacements=True,
):
    try:
        skip_deep_tower = getattr(self, "skip_deep_tower_resolution", False)
        primitive_keys, _primitive_records, _source_by_key = (
            _fast_known_mp_primitive_records(self)
        )
        tower_records = () if skip_deep_tower else _fast_tower_records(self)
        return _fast_block_has_primitive_certificate(
            self,
            inputs,
            primitive_keys,
            tower_records=tower_records,
            allow_tower_records=not skip_deep_tower,
            allow_bridge_replacements=allow_bridge_replacements,
        )
    except Exception:
        return False


def mp_block_has_primitive(self, inputs, allow_bridge_replacements=True):
    """
    Return True if a lower block has a concrete or virtual tower primitive.
    """

    _ensure_absorbing_higher_products(self)

    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    bridge_promoted_self_primitive = False

    try:
        key = self.mp_key(*inputs)
        recorded_primitive = getattr(self, "resolved_massey_products", {}).get(
            key,
            None,
        )
        bridge_promoted_self_primitive = (
            _is_bridge_promoted_massey_primitive_for_inputs(
                self,
                recorded_primitive,
                inputs,
            )
        )
    except Exception:
        bridge_promoted_self_primitive = False

    skip_deep_tower = getattr(self, "skip_deep_tower_resolution", False)

    if not skip_deep_tower and not bridge_promoted_self_primitive:
        if self.is_tower_eliminated_mp(inputs):
            return True

        if self.is_pair_tower_eliminated_mp(inputs):
            return True

    primitive = self.mp_block_primitive(
        *inputs,
        allow_bridge_replacements=(
            False
            if skip_deep_tower or len(inputs) >= 3
            else allow_bridge_replacements
        ),
    )

    if primitive is not None:
        if _is_bridge_promoted_massey_primitive_for_inputs(self, primitive, inputs):
            return False

        return True

    if len(inputs) >= 3:
        if getattr(self, "_suppress_primitive_expansion", False):
            if _mp_block_has_fast_primitive_certificate(
                self,
                inputs,
                allow_bridge_replacements=not skip_deep_tower,
            ):
                return True

            if not allow_bridge_replacements or skip_deep_tower:
                return False

            return _mp_block_has_bridge_replacement_certificate(self, inputs)

        if _mp_block_has_fast_primitive_certificate(
            self,
            inputs,
            allow_bridge_replacements=not skip_deep_tower,
        ):
            return True

        if _higher_mp_block_has_obvious_primitive(self, inputs):
            return True

        if not allow_bridge_replacements:
            return False

        return _mp_block_has_bridge_replacement_certificate(self, inputs)

    if getattr(self, "_suppress_primitive_expansion", False):
        if _mp_block_has_fast_primitive_certificate(
            self,
            inputs,
            allow_bridge_replacements=allow_bridge_replacements,
        ):
            return True

        if not allow_bridge_replacements:
            return False

        return _mp_block_has_bridge_replacement_certificate(self, inputs)

    if _mp_block_has_fast_primitive_certificate(
        self,
        inputs,
        allow_bridge_replacements=allow_bridge_replacements,
    ):
        return True

    if not allow_bridge_replacements:
        return False

    return _mp_block_has_bridge_replacement_certificate(self, inputs)


def _base_can_define_mp(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    base = getattr(type(self), "_cyclic_base_can_define_mp", None)

    if base is not None:
        try:
            return bool(base(self, *inputs))
        except Exception:
            return False

    n = len(inputs)

    if n == 0:
        return False

    if self.has_zero_mp_input(inputs):
        return True

    if n == 1:
        return True

    if n == 2:
        return self.are_composable(inputs[0], inputs[1])

    try:
        required = self.required_lower_mps(*inputs)
    except Exception:
        return False

    for subkey in required:
        if not self.mp_block_has_primitive(subkey):
            return False

    return True


def _base_mp(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    base = getattr(type(self), "_cyclic_base_mp", None)

    if base is not None:
        return base(self, *inputs)

    key = tuple(inputs)
    existing = getattr(self, "massey_products", {}).get(key, None)

    if existing is not None:
        return existing

    if not _base_can_define_mp(self, inputs):
        return None

    M = MasseyProduct(self, key)
    self.massey_products[key] = M
    return M


def _generalized_definition_key(self, inputs):
    try:
        return tuple(self.mp_factor_key(item) for item in tuple(inputs))
    except Exception:
        return tuple(repr(item) for item in tuple(inputs))


def _generalized_factor_for_inputs(self, inputs, report=None, record=False):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) == 0:
        return None

    if len(inputs) == 1:
        try:
            factors = self.canonical_mp_factors(inputs)
            return factors[0] if factors else None
        except Exception:
            try:
                return self.mp(inputs[0])
            except Exception:
                return None

    if report is not None and not report.get("classical", True):
        return absorbing_higher_product(
            self,
            *inputs,
            record=record,
            resolution_data=report,
        )

    existing = getattr(self, "massey_products", {}).get(tuple(inputs), None)

    if isinstance(existing, MasseyProduct):
        return existing

    try:
        return MasseyProduct(self, inputs)
    except Exception:
        return None


def _generalized_factor_lists_for_interval(self, interval_inputs, interval_report):
    lists = []
    seen = set()

    def remember(factors):
        try:
            factors = self.canonical_mp_factors(tuple(factors))
        except Exception:
            return

        if not factors:
            return

        try:
            key = tuple(self.mp_factor_key(factor) for factor in factors)
        except Exception:
            key = tuple(repr(factor) for factor in factors)

        if key in seen:
            return

        seen.add(key)
        lists.append(factors)

    interval_factor = _generalized_factor_for_inputs(
        self,
        interval_inputs,
        report=interval_report,
        record=False,
    )

    if interval_factor is not None:
        remember((interval_factor,))

    remember(tuple(interval_inputs))
    return tuple(lists)


def _generalized_collapsed_product_factors(
    self,
    inputs,
    start,
    stop,
    replacement_factor,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    try:
        prefix = self.canonical_mp_factors(inputs[:start])
        suffix = self.canonical_mp_factors(inputs[stop:])
        middle = self.canonical_mp_factors((replacement_factor,))
    except Exception:
        return ()

    return tuple(prefix) + tuple(middle) + tuple(suffix)


def _generalized_collapsed_inputs(inputs, start, stop, replacement_input):
    inputs = tuple(inputs)
    return inputs[:start] + (replacement_input,) + inputs[stop:]


def _generalized_product_factors_have_direct_primitive(self, factors):
    try:
        factors = self.canonical_mp_factors(tuple(factors))
    except Exception:
        return False

    if len(factors) < 1:
        return False

    try:
        if not self.mp_factors_composable(factors, cyclic=False):
            return False
    except Exception:
        return False

    try:
        block_key = self.mp_product_block_key(factors)
        primitive = self.direct_mp_block_primitive(*block_key)
    except Exception:
        primitive = None

    return primitive is not None


def _generalized_inputs_have_resolution(self, inputs):
    try:
        return bool(self.mp_block_has_primitive(tuple(inputs)))
    except Exception:
        return False


def _generalized_bridge_collapse_options(
    self,
    interval_inputs,
    interval_report,
):
    source_lists = _generalized_factor_lists_for_interval(
        self,
        interval_inputs,
        interval_report,
    )

    if not source_lists:
        return ()

    try:
        relations = tuple(
            self.mp_presentation_replacement_relations(
                include_bridge=True,
                include_ainf=False,
                include_self_expanding=True,
            )
            or ()
        )
    except Exception:
        relations = ()

    options = []
    seen = set()

    for relation in relations:
        raw_sides = (
            (relation.get("left", ()), relation.get("right", ())),
            (relation.get("right", ()), relation.get("left", ())),
        )

        for source, target in raw_sides:
            try:
                source = self.canonical_mp_factors(tuple(source))
                target = self.canonical_mp_factors(tuple(target))
            except Exception:
                continue

            if len(target) != 1:
                continue

            if not any(self.mp_factors_equal(source, item) for item in source_lists):
                continue

            try:
                source_complexity = _replacement_factors_complexity(self, source)
                target_complexity = _replacement_factors_complexity(self, target)
            except Exception:
                continue

            if target_complexity >= source_complexity:
                continue

            target_factor = target[0]
            target_input = _absorbing_input_from_factor(self, target_factor)

            try:
                key = (
                    tuple(self.mp_factor_key(item) for item in source),
                    tuple(self.mp_factor_key(item) for item in target),
                )
            except Exception:
                key = (repr(source), repr(target))

            if key in seen:
                continue

            seen.add(key)
            options.append({
                "source_factors": source,
                "target_factors": target,
                "target_factor": target_factor,
                "target_input": target_input,
                "source_complexity": source_complexity,
                "target_complexity": target_complexity,
                "relation": relation,
            })

    return tuple(options)


def _classical_higher_product_definition_report(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if not _base_can_define_mp(self, inputs):
        return None

    return {
        "defined": True,
        "classical": True,
        "source": "classical_pure_massey_product",
        "inputs": inputs,
        "intervals": (),
        "nonclassical_reasons": (),
    }


def _generalized_definition_memo_key(self, inputs, require_nonclassical):
    return (
        "nonclassical" if require_nonclassical else "any",
        _generalized_definition_key(self, inputs),
    )


def _generalized_definition_report_candidates(
    self,
    inputs,
    memo,
    visiting,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    candidates = []

    classical = _classical_higher_product_definition_report(self, inputs)

    if classical is not None:
        candidates.append(classical)

    nonclassical = _generalized_higher_product_definition_report(
        self,
        inputs,
        memo=memo,
        visiting=visiting,
        require_nonclassical=True,
    )

    if nonclassical is not None:
        candidates.append(nonclassical)

    return tuple(candidates)


def _generalized_interval_resolution_candidate(
    self,
    inputs,
    start,
    stop,
    interval_report,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    interval_inputs = inputs[start:stop]
    interval_record = {
        "span": (start, stop),
        "inputs": interval_inputs,
        "definition": interval_report,
    }
    reasons = []

    if not interval_report.get("classical", True):
        reasons.append({
            "kind": "nonclassical_subinterval",
            "span": (start, stop),
            "inputs": interval_inputs,
        })

    if _generalized_inputs_have_resolution(self, interval_inputs):
        interval_record["resolution"] = "resolved_subinterval"
        return interval_record, tuple(reasons)

    interval_factor = _generalized_factor_for_inputs(
        self,
        interval_inputs,
        report=interval_report,
        record=False,
    )

    if interval_factor is not None:
        collapsed_factors = _generalized_collapsed_product_factors(
            self,
            inputs,
            start,
            stop,
            interval_factor,
        )

        if _generalized_product_factors_have_direct_primitive(
            self,
            collapsed_factors,
        ):
            interval_record.update({
                "resolution": "contextual_product",
                "collapsed_product_factors": collapsed_factors,
            })
            reasons.append({
                "kind": "contextual_product",
                "span": (start, stop),
                "inputs": interval_inputs,
                "collapsed_product_factors": collapsed_factors,
            })
            return interval_record, tuple(reasons)

    for option in _generalized_bridge_collapse_options(
        self,
        interval_inputs,
        interval_report,
    ):
        collapsed_inputs = _generalized_collapsed_inputs(
            inputs,
            start,
            stop,
            option["target_input"],
        )

        if not _generalized_inputs_have_resolution(
            self,
            collapsed_inputs,
        ):
            continue

        chosen_bridge = dict(option)
        chosen_bridge["collapsed_inputs"] = collapsed_inputs
        interval_record.update({
            "resolution": "bridge_collapse",
            "bridge_collapse": chosen_bridge,
            "collapsed_inputs": collapsed_inputs,
        })
        reasons.append({
            "kind": "bridge_collapse",
            "span": (start, stop),
            "inputs": interval_inputs,
            "collapsed_inputs": collapsed_inputs,
            "target_factor": chosen_bridge.get("target_factor"),
            "relation": chosen_bridge.get("relation"),
        })
        return interval_record, tuple(reasons)

    return None, ()


def _generalized_higher_product_definition_report(
    self,
    inputs,
    memo=None,
    visiting=None,
    require_nonclassical=False,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    key = _generalized_definition_memo_key(
        self,
        inputs,
        require_nonclassical,
    )

    if memo is None:
        memo = {}

    if visiting is None:
        visiting = set()

    if key in memo:
        return memo[key]

    classical_report = _classical_higher_product_definition_report(self, inputs)

    if classical_report is not None and not require_nonclassical:
        memo[key] = classical_report
        return classical_report

    n = len(inputs)

    if n < 3:
        memo[key] = None
        return None

    if self.has_zero_mp_input(inputs):
        memo[key] = None
        return None

    if not _fast_key_is_composable(self, inputs):
        memo[key] = None
        return None

    if key in visiting:
        return None

    visiting.add(key)
    intervals = []
    nonclassical_reasons = []

    try:
        for length in range(2, n):
            for start in range(0, n - length + 1):
                stop = start + length
                interval_inputs = inputs[start:stop]
                interval_reports = _generalized_definition_report_candidates(
                    self,
                    interval_inputs,
                    memo=memo,
                    visiting=visiting,
                )

                if not interval_reports:
                    memo[key] = None
                    return None

                interval_record = None
                interval_reasons = ()

                for interval_report in interval_reports:
                    interval_record, interval_reasons = (
                        _generalized_interval_resolution_candidate(
                            self,
                            inputs,
                            start,
                            stop,
                            interval_report,
                        )
                    )

                    if interval_record is not None:
                        break

                if interval_record is None:
                    memo[key] = None
                    return None

                intervals.append(interval_record)
                nonclassical_reasons.extend(interval_reasons)
    finally:
        visiting.discard(key)

    if not nonclassical_reasons:
        memo[key] = None
        return None

    report = {
        "defined": True,
        "classical": False,
        "source": "generalized_higher_product",
        "inputs": inputs,
        "intervals": tuple(intervals),
        "nonclassical_reasons": tuple(nonclassical_reasons),
    }
    memo[key] = report
    return report


def generalized_higher_product_definition_report(self, *inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    report = _generalized_higher_product_definition_report(self, inputs)

    if report is None:
        return {
            "defined": False,
            "classical": False,
            "source": "not_defined",
            "inputs": inputs,
            "intervals": (),
            "nonclassical_reasons": (),
        }

    return dict(report)


def can_define_mp(self, *inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if _base_can_define_mp(self, inputs):
        return True

    report = _generalized_higher_product_definition_report(self, inputs)
    return bool(report and report.get("defined", False))


def mp(self, *inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    key = tuple(inputs)

    existing = getattr(self, "massey_products", {}).get(key, None)

    if existing is not None:
        return existing

    if _base_can_define_mp(self, inputs):
        return _base_mp(self, inputs)

    report = _generalized_higher_product_definition_report(self, inputs)

    if report and report.get("defined", False):
        return absorbing_higher_product(
            self,
            *inputs,
            record=True,
            resolution_data=report,
        )

    try:
        missing = self.missing_requirements_for_mp(*inputs)
    except Exception:
        missing = []

    print(
        f"Warning: mp{key} is not defined yet. "
        f"Missing resolved lower products: {missing}"
    )
    return None


def missing_requirements_for_mp(self, *inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if _base_can_define_mp(self, inputs):
        return []

    report = _generalized_higher_product_definition_report(self, inputs)

    if report and report.get("defined", False):
        return []

    base = getattr(type(self), "_cyclic_base_missing_requirements_for_mp", None)

    if base is not None:
        try:
            return base(self, *inputs)
        except Exception:
            return []

    missing = []

    try:
        required = self.required_lower_mps(*inputs)
    except Exception:
        return missing

    for subkey in required:
        if not self.mp_block_has_primitive(subkey):
            missing.append(subkey)

    return missing


def generation_item_key(self, item):
    if _is_absorbing_higher_product(item):
        try:
            return item.key()
        except Exception:
            return (
                "AbsorbingHigherProduct",
                tuple(repr(part) for part in tuple(getattr(item, "inputs", ()))),
            )

    base = getattr(type(self), "_cyclic_base_generation_item_key", None)

    if base is not None:
        return base(self, item)

    if hasattr(item, "key"):
        return item.key()

    return repr(item)


def virtual_mp(self, *inputs, record=True):
    """
    Create a formal MasseyProduct when its lower products are certified only
    virtually, for example by tower elimination or bridge replacement.
    """

    inputs = tuple(self.normalize_mp_inputs(inputs))
    key = tuple(inputs)

    existing = getattr(self, "massey_products", {}).get(key, None)

    if existing is not None:
        return existing

    if _base_can_define_mp(self, inputs):
        M = MasseyProduct(self, key)

        if record:
            self.massey_products[key] = M

        return M

    report = _generalized_higher_product_definition_report(self, inputs)

    if report and report.get("defined", False):
        return absorbing_higher_product(
            self,
            *inputs,
            record=record,
            resolution_data=report,
        )

    try:
        defined = self.can_define_mp(*inputs)
    except Exception:
        defined = False

    if not defined:
        try:
            missing = self.missing_requirements_for_mp(*inputs)
        except Exception:
            missing = []

        print(
            f"Warning: mp{key} is not defined yet. "
            f"Missing resolved lower products: {missing}"
        )
        return None

    M = MasseyProduct(self, key)

    if record:
        self.massey_products[key] = M

    return M


def try_generate_mp(self, *inputs, record=True, verbose=False):
    """
    Generate/register mp(inputs), except for virtual tower-eliminated products.
    """

    inputs = tuple(self.normalize_mp_inputs(inputs))

    if _mp_inputs_contain_resolved_higher_massey(self, inputs):
        if verbose:
            print("Skipping MP with resolved higher Massey input:")
            print("inputs =", inputs)

        return None

    if self.has_zero_mp_input(inputs):
        if verbose:
            print("Skipping zero-input MP:")
            print("inputs =", inputs)

        return None

    if self.is_tower_eliminated_mp(inputs):
        if verbose:
            print("Skipping tower-eliminated MP:")
            print("inputs =", inputs)

        return None

    if not self.can_define_mp(*inputs):
        if verbose:
            print("Cannot define MP:")
            print("inputs =", inputs)

        return None

    try:
        M = self.mp(*inputs)
    except Exception as e:
        if verbose:
            print("Could not generate MP:")
            print("inputs =", inputs)
            print("Python error:", e)

        return None

    if record:
        if not hasattr(self, "generated_massey_products"):
            self.generated_massey_products = []

        key = self.mp_key(*inputs)
        old_keys = {
            self.mp_key(*self.normalize_mp_inputs(x.inputs))
            for x in self.generated_massey_products
            if isinstance(x, MasseyProduct)
        }

        if key not in old_keys:
            self.generated_massey_products.append(M)

    return M


def _fast_mp_key(self, inputs):
    try:
        return self.mp_key(*tuple(inputs))
    except Exception:
        return None


def _fast_key_is_composable(self, key):
    key = tuple(key)

    if len(key) < 2:
        return True

    try:
        if self.has_zero_mp_input(key):
            return True

        return all(
            self.are_composable(left, right)
            for left, right in zip(key, key[1:])
        )
    except Exception:
        return False


def _fast_candidate_key(self, candidate):
    try:
        return repr(self.mp_factor_key(candidate))
    except Exception:
        return repr(candidate)


def _fast_candidate_is_cell_like(candidate):
    return hasattr(candidate, "cell_prefix") or hasattr(candidate, "index")


def _fast_add_extension_candidate(self, candidates, seen, candidate):
    try:
        candidate = self.normalize_mp_input(candidate)
    except Exception:
        pass

    if _mp_factor_contains_resolved_higher_massey(self, candidate):
        return

    if isinstance(candidate, tuple):
        return

    if _fast_candidate_is_cell_like(candidate):
        return

    if isinstance(candidate, MPProduct):
        try:
            factors = tuple(self.canonical_mp_factors(candidate))
        except Exception:
            return

        if len(factors) < 2:
            return

        try:
            if not self.mp_factors_composable(factors, cyclic=False):
                return
        except Exception:
            return

        candidate = MPProduct(self, factors)

    elif isinstance(candidate, MasseyProduct):
        if len(tuple(candidate.inputs)) < 3:
            return

    elif getattr(candidate, "source", None) is None or getattr(candidate, "target", None) is None:
        return

    key = _fast_candidate_key(self, candidate)

    if key in seen:
        return

    seen.add(key)
    candidates.append(candidate)


def _fast_composite_product_extension_candidates(self, primitive_records):
    raw_bound = getattr(self, "fast_product_factor_candidate_max_length", 3)

    try:
        max_length = max(2, int(raw_bound))
    except (TypeError, ValueError):
        max_length = 3

    out = []
    seen = set()

    for record_data in tuple(primitive_records or ()):
        source_key = tuple(record_data.get("key", ()))

        if len(source_key) < 2:
            continue

        for start in range(len(source_key)):
            for stop in range(start + 2, min(len(source_key), start + max_length) + 1):
                block = source_key[start:stop]

                try:
                    factors = tuple(self.canonical_mp_factors(block))
                except Exception:
                    continue

                if len(factors) < 2:
                    continue

                try:
                    if not self.mp_factors_composable(factors, cyclic=False):
                        continue
                except Exception:
                    continue

                key = tuple(repr(self.mp_factor_key(factor)) for factor in factors)

                if key in seen:
                    continue

                seen.add(key)
                out.append(MPProduct(self, factors))

    return tuple(out)


def _fast_product_factors_as_mp_input(self, factors):
    factors = tuple(self.normalize_mp_inputs(tuple(factors)))

    if not factors:
        return None

    if len(factors) == 1:
        return self.normalize_mp_input(factors[0])

    product = None

    for factor in factors:
        mp_factor = factor if isinstance(factor, MasseyProduct) else self.mp(factor)
        product = mp_factor if product is None else product * mp_factor

    return product


def _fast_grouped_input_partitions(self, flat_word, arity, max_partitions=128):
    flat_word = tuple(self.normalize_mp_inputs(tuple(flat_word)))

    if arity < 1 or len(flat_word) < arity:
        return ()

    out = []

    def grouped_factor(group):
        return _fast_product_factors_as_mp_input(self, group)

    def visit(start, groups_left, current):
        if len(out) >= max_partitions:
            return

        if groups_left == 1:
            group = flat_word[start:]

            if not group:
                return

            factor = grouped_factor(group)

            if factor is not None:
                out.append(tuple(current) + (factor,))

            return

        max_stop = len(flat_word) - groups_left + 1

        for stop in range(start + 1, max_stop + 1):
            factor = grouped_factor(flat_word[start:stop])

            if factor is None:
                continue

            visit(stop, groups_left - 1, tuple(current) + (factor,))

    visit(0, arity, ())
    return tuple(out)


def _fast_equivalent_grouped_input_variants(self, inputs, max_partitions=None):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return ()

    original_key = _fast_mp_key(self, inputs)
    variants = []
    seen = {original_key}

    for boundary in range(0, len(inputs) - 1):
        right_input = self.normalize_mp_input(inputs[boundary + 1])

        if not isinstance(right_input, MPProduct):
            continue

        try:
            right_factors = tuple(self.canonical_mp_factors(right_input))
        except Exception:
            right_factors = tuple(getattr(right_input, "factors", ()))

        right_factors = tuple(self.normalize_mp_inputs(tuple(right_factors)))

        if len(right_factors) < 2:
            continue

        try:
            left_factors = tuple(self.canonical_mp_factors((inputs[boundary],)))
        except Exception:
            left_factors = (inputs[boundary],)

        left_factors = tuple(self.normalize_mp_inputs(tuple(left_factors)))

        if not left_factors:
            continue

        try:
            boundary_factors = tuple(
                self.canonical_mp_factors((inputs[boundary], right_input))
            )
        except Exception:
            boundary_factors = left_factors + right_factors

        boundary_factors = tuple(self.normalize_mp_inputs(tuple(boundary_factors)))
        left_stop = len(left_factors)

        if len(boundary_factors) <= left_stop + 1:
            continue

        for split in range(left_stop + 1, len(boundary_factors)):
            left = _fast_product_factors_as_mp_input(
                self,
                boundary_factors[:split],
            )
            right = _fast_product_factors_as_mp_input(
                self,
                boundary_factors[split:],
            )

            if left is None or right is None:
                continue

            grouped_inputs = (
                inputs[:boundary]
                + (left, right)
                + inputs[boundary + 2:]
            )
            key = _fast_mp_key(self, grouped_inputs)

            if key is None or key in seen:
                continue

            seen.add(key)
            variants.append(grouped_inputs)

    return tuple(variants)


def _fast_path_specific_extension_inputs(
    self,
    source_key,
    q,
    direction,
    primitive_keys,
    tower_records,
    _depth=0,
):
    source_key = tuple(source_key)
    q = self.normalize_mp_input(q)
    default_inputs = (
        (q,) + source_key
        if direction == "left"
        else source_key + (q,)
    )

    if not isinstance(q, MPProduct) or not source_key:
        return (default_inputs,)

    try:
        q_factors = tuple(self.canonical_mp_factors(q))
    except Exception:
        return (default_inputs,)

    if len(q_factors) < 2:
        return (default_inputs,)

    if _depth > len(q_factors) + 1:
        return (default_inputs,)

    if direction == "right":
        boundary_seed = (source_key[-1], q)
        q_start = len(tuple(self.canonical_mp_factors((source_key[-1],))))
        build_inputs = lambda reduced: source_key + (reduced,)
    else:
        boundary_seed = (q, source_key[0])
        q_start = 0
        build_inputs = lambda reduced: (reduced,) + source_key

    try:
        boundary_factors = tuple(self.canonical_mp_factors(boundary_seed))
    except Exception:
        return (default_inputs,)

    if direction == "left":
        q_stop = len(q_factors)
    else:
        q_stop = len(boundary_factors)

    candidates = _fast_primitive_candidates_for_product(
        self,
        MPProduct(self, boundary_factors),
        primitive_keys=primitive_keys,
        tower_records=tower_records,
        minimal_only=True,
    )

    if not candidates:
        return (default_inputs,)

    variants = []
    seen = set()

    def remember(inputs):
        key = _fast_mp_key(self, inputs)

        if key is None or key in seen:
            return

        seen.add(key)
        variants.append(tuple(inputs))

    def remember_reduced(reduced):
        if reduced is None:
            return

        if isinstance(reduced, MPProduct):
            try:
                reduced_factors = tuple(self.canonical_mp_factors(reduced))
            except Exception:
                reduced_factors = ()

            if 1 < len(reduced_factors) < len(q_factors):
                for nested_inputs in _fast_path_specific_extension_inputs(
                    self,
                    source_key,
                    reduced,
                    direction,
                    primitive_keys,
                    tower_records,
                    _depth=_depth + 1,
                ):
                    remember(nested_inputs)
                return

        remember(build_inputs(reduced))

    for candidate in candidates:
        left = tuple(candidate.get("left", ()))
        block = tuple(candidate.get("block", ()))
        start = len(left)
        stop = start + len(block)

        if direction == "right":
            if stop <= q_start:
                continue

            if start < q_start:
                if stop == q_stop or (
                    stop > q_start and len(q_factors) >= 3
                ):
                    remember(default_inputs)
                continue

            rel_start = start - q_start
            reduced = _fast_product_factors_as_mp_input(
                self,
                q_factors[:rel_start + 1],
            )

            remember_reduced(reduced)
        else:
            if start >= q_stop:
                continue

            if stop > q_stop:
                if (
                    start == 0
                    and stop == len(boundary_factors)
                ) or (
                    start < q_stop
                    and len(q_factors) >= 3
                ):
                    remember(default_inputs)
                continue

            reduced = _fast_product_factors_as_mp_input(
                self,
                q_factors[stop - 1:],
            )

            remember_reduced(reduced)

    return tuple(variants)


def _fast_higher_massey_extension_candidates(self, generated_items=()):
    out = []
    seen = set()

    def remember(item):
        if not isinstance(item, MasseyProduct):
            return

        if len(tuple(item.inputs)) < 3:
            return

        key = _fast_candidate_key(self, item)

        if key in seen:
            return

        seen.add(key)
        out.append(item)

    for item in getattr(self, "generated_massey_products", []):
        remember(item)

    for item in tuple(generated_items or ()):
        remember(item)

    for item in getattr(self, "massey_products", {}).values():
        remember(item)

    for key in getattr(self, "resolved_massey_products", {}).keys():
        if len(tuple(key)) < 3:
            continue

        try:
            item = getattr(self, "massey_products", {}).get(tuple(key), None)

            if item is None:
                item = MasseyProduct(self, tuple(key))
        except Exception:
            continue

        remember(item)

    return tuple(out)


def _fast_add_primitive_record(
    self,
    records,
    keys,
    source_by_key,
    inputs,
    source,
    allow_length_one=False,
):
    key = _fast_mp_key(self, inputs)

    if key is None or len(key) < 1:
        return

    if len(key) < 2 and not allow_length_one:
        return

    if not _fast_key_is_composable(self, key):
        return

    if key in keys:
        return

    keys.add(key)
    source_by_key[key] = source
    records.append({
        "key": key,
        "source": source,
    })


def _fast_expression_primitive_key(self, expression):
    if isinstance(expression, MasseyProduct):
        return _fast_mp_key(self, expression.inputs)

    if isinstance(expression, MPProduct):
        try:
            return self.mp_product_block_key(tuple(expression.factors))
        except Exception:
            return None

    if isinstance(expression, MPElement) and len(expression.terms) == 1:
        product, coeff = next(iter(expression.terms.items()))

        if is_zero_coeff(coeff) or not isinstance(product, MPProduct):
            return None

        try:
            return self.mp_product_block_key(tuple(product.factors))
        except Exception:
            return None

    if isinstance(expression, (Arrow, Path, Element)) and hasattr(self, "path_to_mp_product"):
        try:
            product = self.path_to_mp_product(expression)
        except Exception:
            product = None

        if isinstance(product, MPProduct):
            try:
                return self.mp_product_block_key(tuple(product.factors))
            except Exception:
                return None

    return None


def _fast_remember_termination_record(
    self,
    records_by_key,
    key,
    source,
    cell=None,
    expression=None,
    path_key=None,
):
    if key is None or len(tuple(key)) < 1:
        return

    if not _fast_key_is_composable(self, key):
        return

    records = records_by_key.setdefault(tuple(key), [])
    record_key = (
        source,
        id(cell) if cell is not None else None,
        repr(expression),
        tuple(path_key or ()),
    )

    for record in records:
        if cell is not None and record.get("cell") is cell:
            return

        if record.get("record_key") == record_key:
            return

    records.append({
        "record_key": record_key,
        "source": source,
        "cell": cell,
        "expression": expression,
        "path_key": tuple(path_key or ()),
    })


def _fast_known_mp_termination_records(self):
    _ensure_absorbing_higher_products(self)

    records_by_key = {}

    for key, primitive in getattr(self, "resolved_massey_products", {}).items():
        expression = None

        try:
            expression = self.mp(*tuple(key))
        except Exception:
            expression = None

        _fast_remember_termination_record(
            self,
            records_by_key,
            tuple(key),
            (
                "absorbing_higher_product"
                if _is_absorbing_higher_product(primitive)
                else "resolved_massey_product"
            ),
            cell=primitive,
            expression=expression,
        )

    for entry in getattr(self, "attachment_history", []):
        expression = entry.get("expression", None)
        key = _fast_expression_primitive_key(self, expression)

        if key is None:
            continue

        _fast_remember_termination_record(
            self,
            records_by_key,
            key,
            entry.get("kind", "attachment"),
            cell=entry.get("cell", None),
            expression=expression,
        )

    for path_key, cell in getattr(self, "cells", {}).items():
        try:
            inputs = tuple(
                self.arrows[name] if isinstance(name, str) else name
                for name in tuple(path_key)
            )
        except Exception:
            continue

        key = _fast_mp_key(self, inputs)
        _fast_remember_termination_record(
            self,
            records_by_key,
            key,
            "ordinary_cell",
            cell=cell,
            expression=getattr(cell, "index", None),
            path_key=path_key,
        )

    return records_by_key


def _fast_primitive_records_cache_signature(self):
    _ensure_absorbing_higher_products(self)

    return (
        len(tuple(getattr(self, "attachment_history", ()) or ())),
        len(getattr(self, "resolved_massey_products", {}) or {}),
        len(getattr(self, "resolved_mp_expressions", {}) or {}),
        len(getattr(self, "cells", {}) or {}),
        tuple(sorted(
            repr(key)
            for key in getattr(self, "_absorbing_higher_product_resolved_keys", set())
        )),
    )


def _fast_add_regrouped_resolved_massey_records(
    self,
    records,
    keys,
    source_by_key,
    inputs,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return

    try:
        flat_word = tuple(self.canonical_mp_factors(inputs))
    except Exception:
        return

    flat_word = tuple(self.normalize_mp_inputs(tuple(flat_word)))

    if len(flat_word) <= len(inputs):
        return

    if any(isinstance(item, MasseyProduct) for item in flat_word):
        return

    raw_max_length = getattr(
        self,
        "fast_regrouped_massey_certificate_max_flat_length",
        7,
    )

    try:
        max_length = max(3, int(raw_max_length))
    except (TypeError, ValueError):
        max_length = 7

    if len(flat_word) > max_length:
        return

    raw_max_partitions = getattr(
        self,
        "fast_regrouped_massey_certificate_max_partitions",
        128,
    )

    try:
        max_partitions = max(1, int(raw_max_partitions))
    except (TypeError, ValueError):
        max_partitions = 128

    base_primitive_keys = frozenset(
        key
        for key in keys
        if not str(source_by_key.get(key, "")).startswith("regrouped_")
    )
    tower_records = _fast_tower_records(self)

    for grouped_inputs in _fast_grouped_input_partitions(
        self,
        flat_word,
        len(inputs),
        max_partitions=max_partitions,
    ):
        if _mp_inputs_contain_resolved_higher_massey(self, grouped_inputs):
            continue

        if _fast_inputs_have_zero_product_input(
            self,
            grouped_inputs,
            base_primitive_keys,
            tower_records=tower_records,
        ):
            continue

        if not _fast_can_define_mp_from_certificates(
            self,
            grouped_inputs,
            base_primitive_keys,
            tower_records=tower_records,
            allow_bridge_replacements=True,
            allow_product_multiples=False,
        ):
            continue

        _fast_add_primitive_record(
            self,
            records,
            keys,
            source_by_key,
            grouped_inputs,
            "regrouped_resolved_massey_product",
        )


def _fast_known_mp_primitive_records(self):
    _ensure_absorbing_higher_products(self)

    cache_key = _fast_primitive_records_cache_signature(self)
    cache = getattr(self, "_fast_known_mp_primitive_records_cache", None)

    if isinstance(cache, dict) and cache.get("key") == cache_key:
        return cache["value"]

    records = []
    keys = set()
    source_by_key = {}

    for key, primitive in getattr(self, "resolved_massey_products", {}).items():
        if _is_bridge_promoted_massey_primitive_for_inputs(self, primitive, key):
            continue

        source = (
            "absorbing_higher_product"
            if _is_absorbing_higher_product(primitive)
            else "resolved_massey_product"
        )
        _fast_add_primitive_record(
            self,
            records,
            keys,
            source_by_key,
            tuple(key),
            source,
        )

        if not _is_absorbing_higher_product(primitive):
            _fast_add_regrouped_resolved_massey_records(
                self,
                records,
                keys,
                source_by_key,
                tuple(key),
            )

    for entry in getattr(self, "attachment_history", []):
        key = _fast_expression_primitive_key(self, entry.get("expression", None))

        if key is None:
            continue

        _fast_add_primitive_record(
            self,
            records,
            keys,
            source_by_key,
            key,
            entry.get("kind", "attachment"),
            allow_length_one=True,
        )

    for path_key in getattr(self, "cells", {}).keys():
        try:
            inputs = tuple(
                self.arrows[name] if isinstance(name, str) else name
                for name in tuple(path_key)
            )
        except Exception:
            continue

        _fast_add_primitive_record(
            self,
            records,
            keys,
            source_by_key,
            inputs,
            "ordinary_cell",
            allow_length_one=True,
        )

    value = (frozenset(keys), tuple(records), dict(source_by_key))
    self._fast_known_mp_primitive_records_cache = {
        "key": cache_key,
        "value": value,
    }
    return value


def _fast_tower_records(self):
    try:
        return tuple(self.completed_massey_tower_elimination_records(record=False))
    except Exception:
        return ()


def _fast_tower_generation_seed_max_length(self, tower_records):
    configured = getattr(self, "tower_massey_generation_seed_max_length", None)

    if configured is not None:
        try:
            return max(2, int(configured))
        except (TypeError, ValueError):
            pass

    seed_bound = max(
        (
            len(tuple(record.get("seed_inputs", ())))
            for record in tuple(tower_records or ())
        ),
        default=2,
    )
    return max(2, min(4, seed_bound))


def _fast_tower_primitive_seed_records(
    self,
    candidates,
    primitive_keys,
    tower_records,
):
    if not tower_records:
        return []

    candidates = tuple(self.normalize_mp_input(item) for item in tuple(candidates))
    max_length = _fast_tower_generation_seed_max_length(self, tower_records)
    records = []
    seen = set(primitive_keys or ())
    tower_cache = {}

    def is_tower_seed(source_key):
        cache_key = tuple(repr(self.mp_factor_key(item)) for item in source_key)

        if cache_key not in tower_cache:
            try:
                tower_cache[cache_key] = self.tower_elimination_report(
                    *source_key,
                    records=tower_records,
                ) is not None
            except Exception:
                tower_cache[cache_key] = False

        return tower_cache[cache_key]

    def remember(word):
        source_key = _fast_mp_key(self, word)

        if source_key is None or len(source_key) < 2:
            return

        if source_key in seen:
            return

        if not _fast_key_is_composable(self, source_key):
            return

        if not is_tower_seed(source_key):
            return

        seen.add(source_key)
        records.append({
            "key": source_key,
            "source": "completed_massey_tower",
            "virtual": True,
        })

    def extend(word):
        if len(word) >= 2:
            remember(word)

        if len(word) >= max_length:
            return

        for item in candidates:
            if word and word[-1].target != item.source:
                continue

            extend(word + (item,))

    for item in candidates:
        extend((item,))

    return records


def _fast_tower_word_has_primitive(self, flat_word, used_inner, tower_records):
    flat_word = tuple(self.normalize_mp_inputs(tuple(flat_word)))

    if len(flat_word) < 2:
        return False

    if not _fast_key_is_composable(self, flat_word):
        return False

    for record in tuple(tower_records or ()):
        seed_inputs = tuple(record.get("seed_inputs", ()))

        if len(seed_inputs) < 2:
            continue

        if not used_inner and len(flat_word) <= len(seed_inputs):
            continue

        if _tower_word_is_periodic_subword(self, flat_word, seed_inputs):
            return True

    return False


def _fast_pair_tower_word_has_primitive(
    self,
    flat_word,
    tower_records=(),
    pair_tower_records=None,
):
    if getattr(self, "skip_deep_tower_resolution", False):
        return False

    flat_word = tuple(self.normalize_mp_inputs(tuple(flat_word)))

    if len(flat_word) < 2:
        return False

    if not _fast_key_is_composable(self, flat_word):
        return False

    if pair_tower_records is None:
        try:
            pair_tower_records = (
                self.completed_massey_pair_tower_elimination_records(
                    tower_records=tower_records,
                )
            )
        except Exception:
            pair_tower_records = ()

    try:
        return self.pair_tower_elimination_report(
            *flat_word,
            tower_records=tower_records,
            pair_records=pair_tower_records,
        ) is not None
    except Exception:
        return False


def _fast_factor_signature(self, factor):
    try:
        return repr(self.mp_factor_key(factor))
    except Exception:
        return repr(factor)


def _fast_flat_factor_signature(self, factors):
    return tuple(_fast_factor_signature(self, factor) for factor in tuple(factors))


def _fast_input_flat_word_and_boundaries(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    flat = []
    boundaries = []

    for index, factor in enumerate(inputs):
        try:
            word = tuple(self.canonical_mp_factors((factor,)))
        except Exception:
            word = (factor,)

        word = tuple(self.normalize_mp_inputs(tuple(word)))

        if not word:
            continue

        flat.extend(word)

        if index < len(inputs) - 1:
            boundaries.append(len(flat))

    return tuple(flat), tuple(boundaries)


def _fast_primitive_flat_signature_entries(self, primitive_keys):
    entries = []
    seen = set()

    for primitive_key in tuple(primitive_keys or ()):
        primitive_key = tuple(self.normalize_mp_inputs(tuple(primitive_key)))

        if len(primitive_key) < 2:
            continue

        try:
            flat = tuple(self.canonical_mp_factors(primitive_key))
        except Exception:
            flat = primitive_key

        flat = tuple(self.normalize_mp_inputs(tuple(flat)))

        if len(flat) < 2:
            continue

        signature = _fast_flat_factor_signature(self, flat)
        entry_key = (signature, _fast_mp_key(self, primitive_key))

        if entry_key in seen:
            continue

        seen.add(entry_key)
        entries.append({
            "signature": signature,
            "key": primitive_key,
            "flat": flat,
        })

    return tuple(entries)


def _fast_span_crosses_input_boundary(start, stop, boundaries):
    return any(start < boundary < stop for boundary in tuple(boundaries))


def _fast_block_has_product_multiple_certificate(
    self,
    block,
    primitive_keys,
):
    block = tuple(self.normalize_mp_inputs(tuple(block)))

    if len(block) < 2:
        return False

    has_product_input = False

    for item in block:
        item = self.normalize_mp_input(item)

        if not isinstance(item, MPProduct):
            continue

        try:
            item_factors = tuple(self.canonical_mp_factors(item))
        except Exception:
            item_factors = tuple(getattr(item, "factors", ()))

        if len(item_factors) > 1:
            has_product_input = True
            break

    if not has_product_input:
        return False

    try:
        flat_block, boundaries = _fast_input_flat_word_and_boundaries(self, block)
    except Exception:
        return False

    if len(flat_block) < 2 or not boundaries:
        return False

    raw_max_length = getattr(
        self,
        "fast_product_multiple_certificate_max_flat_length",
        8,
    )

    try:
        max_length = max(3, int(raw_max_length))
    except (TypeError, ValueError):
        max_length = 8

    if len(flat_block) > max_length:
        return False

    block_signature = _fast_flat_factor_signature(self, flat_block)
    block_key = _fast_mp_key(self, block)

    for entry in _fast_primitive_flat_signature_entries(self, primitive_keys):
        primitive_signature = tuple(entry["signature"])

        if len(primitive_signature) > len(block_signature):
            continue

        if primitive_signature == block_signature:
            if _fast_mp_key(self, entry["key"]) != block_key:
                return True

            continue

        if len(primitive_signature) == len(block_signature):
            continue

        max_start = len(block_signature) - len(primitive_signature)

        for start in range(max_start + 1):
            stop = start + len(primitive_signature)

            if block_signature[start:stop] != primitive_signature:
                continue

            if not _fast_span_crosses_input_boundary(start, stop, boundaries):
                continue

            return True

    return False


def _fast_block_has_primitive_certificate(
    self,
    block,
    primitive_keys,
    tower_records=(),
    pair_tower_records=None,
    used_inner=False,
    allow_tower_records=True,
    allow_bridge_replacements=True,
    allow_product_multiples=True,
):
    block = tuple(self.normalize_mp_inputs(tuple(block)))

    if len(block) < 2:
        return True

    if self.has_zero_mp_input(block):
        return True

    if not _fast_key_is_composable(self, block):
        return False

    key = _fast_mp_key(self, block)

    if key in primitive_keys:
        return True

    try:
        flat_block = tuple(self.canonical_mp_factors(block))
    except Exception:
        flat_block = ()

    if flat_block and flat_block != block:
        flat_key = _fast_mp_key(self, flat_block)

        if flat_key in primitive_keys:
            return True

    if (
        allow_product_multiples
        and _fast_block_has_product_multiple_certificate(
            self,
            block,
            primitive_keys,
        )
    ):
        return True

    if (
        allow_tower_records
        and _fast_tower_word_has_primitive(
            self,
            block,
            used_inner=used_inner,
            tower_records=tower_records,
        )
    ):
        return True

    if (
        allow_tower_records
        and _fast_pair_tower_word_has_primitive(
            self,
            block,
            tower_records=tower_records,
            pair_tower_records=pair_tower_records,
        )
    ):
        return True

    if not allow_bridge_replacements:
        return False

    return _fast_block_has_bridge_replacement_certificate(self, block)


def _fast_factor_presentation_options(self, factor, tower_records):
    factor = self.normalize_mp_input(factor)
    raw = (factor,)
    options = [{
        "word": raw,
        "used_inner": False,
    }]
    seen = {
        (
            tuple(repr(self.mp_factor_key(item)) for item in raw),
            False,
        )
    }

    if isinstance(factor, MPProduct):
        try:
            product_word = tuple(self.canonical_mp_factors(factor))
        except Exception:
            product_word = ()

        if len(product_word) >= 2:
            key = (
                tuple(repr(self.mp_factor_key(item)) for item in product_word),
                True,
            )

            if key not in seen:
                seen.add(key)
                options.append({
                    "word": product_word,
                    "used_inner": True,
                })

    for record in tuple(tower_records or ()):
        try:
            factor_options = _tower_flatten_factor_options(
                self,
                factor,
                record,
                max_options=16,
            )
        except Exception:
            factor_options = []

        for word, used_inner in factor_options:
            if not used_inner:
                continue

            word = tuple(self.normalize_mp_inputs(tuple(word)))

            if not word:
                continue

            key = (
                tuple(repr(self.mp_factor_key(item)) for item in word),
                True,
            )

            if key in seen:
                continue

            seen.add(key)
            options.append({
                "word": word,
                "used_inner": True,
            })

    return options


def _fast_input_presentations(self, inputs, tower_records, max_options=256):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    presentations = [{
        "words": (),
        "used_flags": (),
    }]

    for factor in inputs:
        factor_options = _fast_factor_presentation_options(
            self,
            factor,
            tower_records,
        )
        next_presentations = []
        seen = set()

        for presentation in presentations:
            for option in factor_options:
                words = presentation["words"] + (tuple(option["word"]),)
                used_flags = presentation["used_flags"] + (bool(option["used_inner"]),)
                key = tuple(
                    tuple(repr(self.mp_factor_key(item)) for item in word)
                    for word in words
                )

                if key in seen:
                    continue

                seen.add(key)
                next_presentations.append({
                    "words": words,
                    "used_flags": used_flags,
                })

                if len(next_presentations) >= max_options:
                    break

            if len(next_presentations) >= max_options:
                break

        presentations = next_presentations

        if not presentations:
            break

    return presentations


def _fast_presentation_flat_word(presentation, start=None, stop=None):
    words = tuple(presentation.get("words", ()))

    if start is None:
        start = 0

    if stop is None:
        stop = len(words)

    flat = []

    for word in words[start:stop]:
        flat.extend(tuple(word))

    return tuple(flat)


def _fast_presentation_uses_inner(presentation, start, stop):
    return any(tuple(presentation.get("used_flags", ()))[start:stop])


def _fast_can_define_mp_from_certificates(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
    allow_bridge_replacements=False,
    allow_product_multiples=True,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    n = len(inputs)

    if n < 3:
        return False

    if _mp_inputs_contain_resolved_higher_massey(self, inputs):
        return False

    if self.has_zero_mp_input(inputs):
        return False

    if _fast_inputs_have_zero_product_input(
        self,
        inputs,
        primitive_keys,
        tower_records=tower_records,
    ):
        return False

    if not _fast_key_is_composable(self, inputs):
        return False

    for presentation in _fast_input_presentations(
        self,
        inputs,
        tower_records,
    ):
        flat_word = _fast_presentation_flat_word(presentation)

        if not _fast_key_is_composable(self, flat_word):
            continue

        all_blocks_have_primitives = True

        for length in range(2, n):
            for start in range(0, n - length + 1):
                stop = start + length
                block = _fast_presentation_flat_word(
                    presentation,
                    start,
                    stop,
                )
                used_inner = _fast_presentation_uses_inner(
                    presentation,
                    start,
                    stop,
                )

                if not _fast_block_has_primitive_certificate(
                    self,
                    block,
                    primitive_keys,
                    tower_records=tower_records,
                    used_inner=used_inner,
                    allow_tower_records=False,
                    allow_bridge_replacements=allow_bridge_replacements,
                    allow_product_multiples=allow_product_multiples,
                ):
                    all_blocks_have_primitives = False
                    break

            if not all_blocks_have_primitives:
                break

        if all_blocks_have_primitives:
            return True

    return False


def _fast_product_input_is_zero(
    self,
    factor,
    primitive_keys,
    tower_records=(),
):
    factor = self.normalize_mp_input(factor)

    if not isinstance(factor, MPProduct):
        return False

    try:
        factors = tuple(self.canonical_mp_factors(factor))
    except Exception:
        return False

    factors = tuple(self.normalize_mp_inputs(factors))

    if len(factors) < 2:
        return False

    for length in range(2, len(factors) + 1):
        for start in range(0, len(factors) - length + 1):
            block = factors[start:start + length]

            if _fast_block_has_primitive_certificate(
                self,
                block,
                primitive_keys,
                tower_records=tower_records,
                allow_bridge_replacements=True,
            ):
                return True

    return False


def _fast_inputs_have_zero_product_input(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
):
    return any(
        _fast_product_input_is_zero(
            self,
            item,
            primitive_keys,
            tower_records=tower_records,
        )
        for item in tuple(inputs)
    )


def generated_massey_inputs_have_zero_product_input(self, inputs):
    try:
        primitive_keys, _primitive_records, _source_by_key = (
            _fast_known_mp_primitive_records(self)
        )
        tower_records = _fast_tower_records(self)
    except Exception:
        return False

    return _fast_inputs_have_zero_product_input(
        self,
        tuple(inputs),
        primitive_keys,
        tower_records=tower_records,
    )


def _fast_block_has_recorded_certificate(self, block, primitive_keys):
    block = tuple(self.normalize_mp_inputs(tuple(block)))

    if len(block) < 2:
        return True

    if self.has_zero_mp_input(block):
        return True

    if not _fast_key_is_composable(self, block):
        return False

    key = _fast_mp_key(self, block)
    return key in primitive_keys


def _fast_inputs_need_bridge_certificate(self, inputs, primitive_keys):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    try:
        required = tuple(self.required_lower_mps(*inputs))
    except Exception:
        return False

    for subkey in required:
        if _fast_block_has_recorded_certificate(self, subkey, primitive_keys):
            continue

        if _mp_block_has_bridge_replacement_certificate(self, subkey):
            return True

    return False


def _fast_inputs_have_whole_bridge_certificate(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    try:
        factors = self.canonical_mp_factors(tuple(inputs))
    except Exception:
        return False

    candidates = _bridge_replacement_product_resolution_candidates(
        self,
        factors,
        minimal_only=True,
    )

    return any(
        candidate.get("minimal")
        and _bridge_candidate_spans_whole_original(candidate, factors)
        for candidate in candidates
    )


def _fast_inputs_are_tower_eliminated(self, inputs, tower_records=()):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 2:
        return False

    try:
        if _tower_elimination_report_with_replacements(
            self,
            inputs,
            records=tower_records,
        ) is not None:
            return True
    except Exception:
        try:
            if self.tower_elimination_report(
                *inputs,
                records=tower_records,
            ) is not None:
                return True
        except Exception:
            pass

    try:
        return self.pair_tower_elimination_report(
            *inputs,
            tower_records=tower_records,
        ) is not None
    except Exception:
        return False


def _fast_inputs_have_nontrivial_product_input(self, inputs):
    for item in tuple(inputs):
        item = self.normalize_mp_input(item)

        if not isinstance(item, MPProduct):
            continue

        try:
            factors = tuple(self.canonical_mp_factors(item))
        except Exception:
            factors = tuple(getattr(item, "factors", ()))

        if len(factors) > 1:
            return True

    return False


def _fast_generated_keys(self):
    out = set()

    for item in getattr(self, "generated_massey_products", ()) or ():
        if not isinstance(item, MasseyProduct):
            continue

        try:
            out.add(self.mp_key(*self.normalize_mp_inputs(tuple(item.inputs))))
        except Exception:
            continue

    return out


def _fast_inputs_are_left_product_multiple_of_known_massey(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return False

    first = self.normalize_mp_input(inputs[0])

    if not isinstance(first, MPProduct):
        return False

    try:
        first_factors = tuple(self.canonical_mp_factors(first))
    except Exception:
        first_factors = tuple(getattr(first, "factors", ()))

    first_factors = tuple(self.normalize_mp_inputs(tuple(first_factors)))

    if len(first_factors) < 2:
        return False

    current_key = _fast_mp_key(self, inputs)
    known_generated_keys = _fast_generated_keys(self)

    for split in range(1, len(first_factors)):
        base_first = _fast_product_factors_as_mp_input(
            self,
            first_factors[split:],
        )

        if base_first is None:
            continue

        base_inputs = (base_first,) + inputs[1:]
        base_key = _fast_mp_key(self, base_inputs)

        if base_key is None or base_key == current_key:
            continue

        if not _fast_key_is_composable(self, base_inputs):
            continue

        if base_key in primitive_keys or base_key in known_generated_keys:
            return True

        if _fast_can_define_mp_from_certificates(
            self,
            base_inputs,
            primitive_keys,
            tower_records=tower_records,
            allow_bridge_replacements=True,
            allow_product_multiples=True,
        ):
            return True

    return False


def _fast_inputs_are_right_product_multiple_of_known_massey(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if len(inputs) < 3:
        return False

    last = self.normalize_mp_input(inputs[-1])

    if not isinstance(last, MPProduct):
        return False

    try:
        last_factors = tuple(self.canonical_mp_factors(last))
    except Exception:
        last_factors = tuple(getattr(last, "factors", ()))

    last_factors = tuple(self.normalize_mp_inputs(tuple(last_factors)))

    if len(last_factors) < 2:
        return False

    current_key = _fast_mp_key(self, inputs)
    known_generated_keys = _fast_generated_keys(self)

    for split in range(1, len(last_factors)):
        base_last = _fast_product_factors_as_mp_input(
            self,
            last_factors[:split],
        )

        if base_last is None:
            continue

        base_inputs = inputs[:-1] + (base_last,)
        base_key = _fast_mp_key(self, base_inputs)

        if base_key is None or base_key == current_key:
            continue

        if not _fast_key_is_composable(self, base_inputs):
            continue

        if base_key in primitive_keys or base_key in known_generated_keys:
            return True

        if _fast_can_define_mp_from_certificates(
            self,
            base_inputs,
            primitive_keys,
            tower_records=tower_records,
            allow_bridge_replacements=True,
            allow_product_multiples=True,
        ):
            return True

    return False


def _fast_inputs_are_endpoint_product_multiple_of_known_massey(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
):
    return (
        _fast_inputs_are_left_product_multiple_of_known_massey(
            self,
            inputs,
            primitive_keys,
            tower_records=tower_records,
        )
        or _fast_inputs_are_right_product_multiple_of_known_massey(
            self,
            inputs,
            primitive_keys,
            tower_records=tower_records,
        )
    )


def generated_massey_inputs_are_product_multiple(self, inputs):
    try:
        primitive_keys, _primitive_records, _source_by_key = (
            _fast_known_mp_primitive_records(self)
        )
        tower_records = _fast_tower_records(self)
    except Exception:
        return False

    return _fast_inputs_are_endpoint_product_multiple_of_known_massey(
        self,
        tuple(inputs),
        primitive_keys,
        tower_records=tower_records,
    )


def _fast_register_generated_mp_if_defined(
    self,
    inputs,
    primitive_keys,
    tower_records=(),
    record=True,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))

    if _mp_inputs_contain_resolved_higher_massey(self, inputs):
        return None

    if not _fast_can_define_mp_from_certificates(
        self,
        inputs,
        primitive_keys,
        tower_records=tower_records,
        allow_bridge_replacements=True,
    ):
        return None

    key = self.mp_key(*inputs)

    if (
        key not in primitive_keys
        and _fast_inputs_are_endpoint_product_multiple_of_known_massey(
            self,
            inputs,
            primitive_keys,
            tower_records=tower_records,
        )
    ):
        return None

    if (
        len(inputs) == 3
        and key not in primitive_keys
        and _fast_inputs_have_nontrivial_product_input(self, inputs)
        and not _fast_can_define_mp_from_certificates(
            self,
            inputs,
            primitive_keys,
            tower_records=tower_records,
            allow_bridge_replacements=True,
            allow_product_multiples=False,
        )
    ):
        return None

    bridge_guard_max_arity = getattr(self, "fast_whole_bridge_guard_max_arity", 3)

    try:
        bridge_guard_max_arity = max(3, int(bridge_guard_max_arity))
    except (TypeError, ValueError):
        bridge_guard_max_arity = 3

    if (
        len(inputs) <= bridge_guard_max_arity
        and
        _fast_inputs_need_bridge_certificate(self, inputs, primitive_keys)
        and not _fast_inputs_have_whole_bridge_certificate(self, inputs)
    ):
        return None

    if _fast_inputs_are_tower_eliminated(
        self,
        inputs,
        tower_records=tower_records,
    ):
        return None

    M = getattr(self, "massey_products", {}).get(key, None)

    if M is None:
        M = MasseyProduct(self, key)
        self.massey_products[key] = M

    if record:
        if not hasattr(self, "generated_massey_products"):
            self.generated_massey_products = []

        old_keys = {
            self.mp_key(*self.normalize_mp_inputs(item.inputs))
            for item in self.generated_massey_products
            if isinstance(item, MasseyProduct)
        }

        if key not in old_keys:
            self.generated_massey_products.append(M)

    return M


def _fast_virtual_tower_seed_extension_is_compatible(
    self,
    inputs,
    source_key,
    primitive_keys,
    tower_records,
):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    source_key = tuple(self.normalize_mp_inputs(tuple(source_key)))
    source_arity = len(source_key)

    try:
        required = tuple(self.required_lower_mps(*inputs))
    except Exception:
        return False

    for subkey in required:
        subkey = tuple(self.normalize_mp_inputs(tuple(subkey)))

        if subkey == source_key:
            continue

        if len(subkey) < 2:
            continue

        if source_arity >= 3 and subkey in primitive_keys:
            continue

        if (
            source_arity >= 3
            and _fast_block_has_bridge_replacement_certificate(self, subkey)
        ):
            continue

        try:
            if self.tower_elimination_report(
                *subkey,
                records=tower_records,
            ) is not None:
                continue
        except Exception:
            pass

        return False

    return True


def _fast_extension_candidates(
    self,
    primitive_records=None,
    generated_items=(),
    include_composite_products=True,
    include_higher_massey=True,
):
    candidates = []
    seen = set()

    try:
        raw_candidates = self.mp_extension_candidates()
    except Exception:
        raw_candidates = []

    for candidate in raw_candidates:
        _fast_add_extension_candidate(self, candidates, seen, candidate)

    if include_composite_products:
        for candidate in _fast_composite_product_extension_candidates(
            self,
            primitive_records,
        ):
            _fast_add_extension_candidate(self, candidates, seen, candidate)

    if include_higher_massey:
        for candidate in _fast_higher_massey_extension_candidates(
            self,
            generated_items=generated_items,
        ):
            _fast_add_extension_candidate(self, candidates, seen, candidate)

    return tuple(candidates)


def _is_bridge_cell(self, cell):
    if cell is None:
        return False

    if getattr(cell, "cell_kind", None) == "bridge":
        return True

    return any(
        bridge_cell is cell
        for bridge_cell in getattr(self, "bridge_cells", {}).values()
    )


def _fast_primitive_records_for_cells(self, cells):
    records = []
    keys = set()
    source_by_key = {}

    for cell in tuple(cells or ()):
        if cell is None or _is_bridge_cell(self, cell):
            continue

        expression = (
            getattr(cell, "deferred_differential_expression", None)
            or getattr(cell, "index", None)
        )
        key = _fast_expression_primitive_key(self, expression)

        if key is None:
            continue

        _fast_add_primitive_record(
            self,
            records,
            keys,
            source_by_key,
            key,
            getattr(cell, "cell_kind", None) or "cell",
            allow_length_one=True,
        )

    return tuple(records)


def _fast_generate_from_primitive_records(
    self,
    source_records,
    primitive_keys,
    primitive_records,
    tower_records,
    record=True,
    verbose=False,
    include_tower_seed_sources=False,
):
    candidates = _fast_extension_candidates(
        self,
        primitive_records=primitive_records,
    )
    tower_seed_candidates = _fast_extension_candidates(
        self,
        include_composite_products=False,
        include_higher_massey=False,
    )
    tower_seed_records = _fast_tower_primitive_seed_records(
        self,
        tower_seed_candidates,
        primitive_keys,
        tower_records,
    )

    primitive_records_for_candidates = tuple(primitive_records)

    if tower_seed_records:
        primitive_records_for_candidates = (
            tuple(primitive_records_for_candidates)
            + tuple(tower_seed_records)
        )

    if include_tower_seed_sources and tower_seed_records:
        source_records = tuple(source_records) + tuple(tower_seed_records)

    tower_seed_keys = {
        tuple(record_data["key"])
        for record_data in tower_seed_records
        if record_data.get("virtual")
    }
    generated = []
    seen = set()
    raw_candidate_rounds = getattr(self, "fast_generation_candidate_rounds", 2)

    try:
        candidate_rounds = max(1, int(raw_candidate_rounds))
    except (TypeError, ValueError):
        candidate_rounds = 2

    seen_candidate_sets = set()

    for _round_index in range(candidate_rounds):
        candidate_set_key = tuple(
            _fast_candidate_key(self, candidate)
            for candidate in tuple(candidates)
        )

        if candidate_set_key in seen_candidate_sets:
            break

        seen_candidate_sets.add(candidate_set_key)
        round_generated_count = len(generated)

        for record_data in tuple(source_records):
            source_key = tuple(record_data["key"])
            record_primitive_keys = primitive_keys

            if record_data.get("virtual"):
                record_primitive_keys = set(primitive_keys)
                record_primitive_keys.add(source_key)

                if len(source_key) >= 3:
                    record_primitive_keys.update(tower_seed_keys)

            if len(source_key) < 2:
                continue

            for q in candidates:
                q = self.normalize_mp_input(q)

                if record_data.get("virtual") and (
                    isinstance(q, MPProduct)
                    or (
                        isinstance(q, MasseyProduct)
                        and len(tuple(q.inputs)) >= 3
                    )
                ):
                    continue

                input_choices = []

                for direction in ("left", "right"):
                    input_choices.extend(
                        _fast_path_specific_extension_inputs(
                            self,
                            source_key,
                            q,
                            direction,
                            record_primitive_keys,
                            tower_records,
                        )
                    )

                for inputs in input_choices:
                    generated_key = _fast_mp_key(self, inputs)

                    if generated_key is None or generated_key in seen:
                        continue

                    if record_data.get("virtual") and not (
                        _fast_virtual_tower_seed_extension_is_compatible(
                            self,
                            generated_key,
                            source_key,
                            record_primitive_keys,
                            tower_records,
                        )
                    ):
                        continue

                    M = _fast_register_generated_mp_if_defined(
                        self,
                        generated_key,
                        record_primitive_keys,
                        tower_records=tower_records,
                        record=record,
                    )

                    if M is None:
                        continue

                    seen.add(generated_key)
                    generated.append(M)

                    if verbose:
                        print("Fast-generated Massey product:", M)

                    for variant_inputs in _fast_equivalent_grouped_input_variants(
                        self,
                        generated_key,
                    ):
                        variant_key = _fast_mp_key(self, variant_inputs)

                        if variant_key is None or variant_key in seen:
                            continue

                        variant = _fast_register_generated_mp_if_defined(
                            self,
                            variant_key,
                            record_primitive_keys,
                            tower_records=tower_records,
                            record=record,
                        )

                        if variant is None:
                            continue

                        seen.add(variant_key)
                        generated.append(variant)

                        if verbose:
                            print("Fast-generated equivalent Massey product:", variant)

        if len(generated) == round_generated_count:
            break

        candidates = _fast_extension_candidates(
            self,
            primitive_records=primitive_records_for_candidates,
            generated_items=generated,
        )

    return self.dedupe_massey_products(generated)


def fast_generate_massey_products(
    self,
    cells=None,
    record=True,
    verbose=False,
):
    """
    Generate MP names by finite block-overlap certificates.

    This intentionally avoids primitive formulas, bridge-replacement graph
    search, and symbolic differential simplification.  A candidate is accepted
    only when one consistent presentation of the whole input sequence makes all
    required lower contiguous blocks primitive, and the whole sequence is not
    already eliminated by a completed tower.
    """

    had_guard = hasattr(self, "_suppress_tower_alias_stasheff_zero")
    old_guard = getattr(self, "_suppress_tower_alias_stasheff_zero", False)
    self._suppress_tower_alias_stasheff_zero = True

    try:
        if cells is not None:
            generated = []
            local_records = _fast_primitive_records_for_cells(self, cells)

            for cell in tuple(cells):
                if not _is_bridge_cell(self, cell):
                    continue

                generated.extend(
                    self.generate_massey_products_from_bridge_cell(
                        cell,
                        record=record,
                        verbose=verbose,
                    )
                )

            if local_records:
                primitive_keys, primitive_records, _source_by_key = (
                    _fast_known_mp_primitive_records(self)
                )
                tower_records = _fast_tower_records(self)
                generated.extend(
                    _fast_generate_from_primitive_records(
                        self,
                        local_records,
                        primitive_keys,
                        primitive_records,
                        tower_records,
                        record=record,
                        verbose=verbose,
                        include_tower_seed_sources=False,
                    )
                )

            return self.dedupe_massey_products(generated)

        primitive_keys, primitive_records, _source_by_key = _fast_known_mp_primitive_records(self)
        tower_records = _fast_tower_records(self)
        return _fast_generate_from_primitive_records(
            self,
            primitive_records,
            primitive_keys,
            primitive_records,
            tower_records,
            record=record,
            verbose=verbose,
            include_tower_seed_sources=True,
        )
    finally:
        if had_guard:
            self._suppress_tower_alias_stasheff_zero = old_guard
        elif hasattr(self, "_suppress_tower_alias_stasheff_zero"):
            delattr(self, "_suppress_tower_alias_stasheff_zero")


def _fast_primitive_candidates_for_product(
    self,
    product,
    primitive_keys=None,
    source_by_key=None,
    termination_by_key=None,
    tower_records=None,
    minimal_only=True,
):
    if isinstance(product, MasseyProduct):
        product = product.as_product()

    if not isinstance(product, MPProduct):
        return []

    try:
        ambient_factors = tuple(self.canonical_mp_factors(product))
    except Exception:
        ambient_factors = tuple(product.factors)

    if primitive_keys is None or source_by_key is None:
        primitive_keys, _records, source_by_key = _fast_known_mp_primitive_records(self)

    if termination_by_key is None:
        termination_by_key = _fast_known_mp_termination_records(self)

    skip_deep_tower = getattr(self, "skip_deep_tower_resolution", False)

    if tower_records is None:
        tower_records = () if skip_deep_tower else _fast_tower_records(self)

    if skip_deep_tower:
        pair_tower_records = ()
    else:
        try:
            pair_tower_records = self.completed_massey_pair_tower_elimination_records(
                tower_records=tower_records,
            )
        except Exception:
            pair_tower_records = ()

    candidates = []
    seen = set()

    for start in range(len(ambient_factors)):
        for stop in range(start + 1, len(ambient_factors) + 1):
            block = ambient_factors[start:stop]

            if len(block) == 1:
                factor = block[0]

                if isinstance(factor, MasseyProduct):
                    block_inputs = tuple(factor.inputs)
                else:
                    block_inputs = (factor,)

                block_key = _fast_mp_key(self, block_inputs)
                block_has_primitive = block_key in primitive_keys
                source = source_by_key.get(block_key, "resolved_massey_product")
                tower_source = False
                pair_tower_source = False
                pair_tower_report = None
            else:
                try:
                    block_key = _fast_mp_key(
                        self,
                        self.mp_product_block_key(block),
                    )
                except Exception:
                    block_key = None

                block_has_primitive = block_key in primitive_keys
                source = source_by_key.get(block_key, "resolved_block")
                tower_source = False
                pair_tower_source = False
                pair_tower_report = None

                if not block_has_primitive and not skip_deep_tower:
                    block_has_primitive = _fast_tower_word_has_primitive(
                        self,
                        block_key or (),
                        used_inner=False,
                        tower_records=tower_records,
                    )
                    tower_source = block_has_primitive

                if not block_has_primitive and not skip_deep_tower:
                    try:
                        pair_tower_report = self.pair_tower_elimination_report(
                            *(block_key or ()),
                            tower_records=tower_records,
                            pair_records=pair_tower_records,
                        )
                    except Exception:
                        pair_tower_report = None

                    block_has_primitive = pair_tower_report is not None
                    pair_tower_source = block_has_primitive

            if not block_has_primitive:
                continue

            termination_records = tuple(termination_by_key.get(block_key, ()))

            if tower_source and not termination_records:
                termination_records = ({
                    "source": "completed_massey_tower",
                    "cell": None,
                    "expression": None,
                    "path_key": (),
                },)

            if pair_tower_source and not termination_records:
                termination_records = ({
                    "source": "completed_massey_pair_tower",
                    "cell": None,
                    "expression": None,
                    "path_key": (),
                },)

            span = (start, stop)
            source_label = (
                "completed_massey_pair_tower"
                if pair_tower_source
                else "completed_massey_tower" if tower_source else source
            )
            candidate_key = (
                span,
                tuple(repr(self.mp_factor_key(item)) for item in block),
                source_label,
            )

            if candidate_key in seen:
                continue

            seen.add(candidate_key)
            candidates.append({
                "kind": source_label if (
                    tower_source or pair_tower_source
                ) else "fast_certificate",
                "source": source_label,
                "left": tuple(ambient_factors[:start]),
                "block": block,
                "right": tuple(ambient_factors[stop:]),
                "block_key": block_key,
                "primitive": None,
                "deferred_primitive": True,
                "pair_tower_report": pair_tower_report,
                "pair_tower_record": (
                    pair_tower_report.get("record")
                    if isinstance(pair_tower_report, dict)
                    else None
                ),
                "termination_records": termination_records,
                "termination_count": len(termination_records),
            })

    if not minimal_only:
        return candidates

    minimal = []

    for candidate in candidates:
        start = len(tuple(candidate.get("left", ())))
        stop = start + len(tuple(candidate.get("block", ())))
        has_smaller = False

        for other in candidates:
            if other is candidate:
                continue

            other_start = len(tuple(other.get("left", ())))
            other_stop = other_start + len(tuple(other.get("block", ())))

            if (
                start <= other_start
                and other_stop <= stop
                and (start, stop) != (other_start, other_stop)
            ):
                has_smaller = True
                break

        if not has_smaller:
            minimal.append(candidate)

    return minimal


def _empty_primitive_classification(
    has_obvious_primitive=False,
    ambient_product=None,
    detail_mode="summary",
):
    return {
        "has_obvious_primitive": has_obvious_primitive,
        "candidates": [],
        "candidate_summaries": [],
        "profiles": [],
        "profile_summaries": [],
        "obvious_pair": None,
        "obvious_profiles": (),
        "ordered_obvious_profiles": (),
        "obvious_split": None,
        "obvious_factorization": None,
        "ambient_product": ambient_product,
        "obvious_massey_product": None,
        "obvious_massey_products": [],
        "induced_massey_products": [],
        "unsettled_termination_pairs": [],
        "detail_mode": detail_mode,
    }


def _termination_record_summary(record):
    cell = record.get("cell", None)
    expression = record.get("expression", None)

    return {
        "source": record.get("source"),
        "cell": "" if cell is None else str(cell),
        "expression": "" if expression is None else str(expression),
        "path_key": tuple(record.get("path_key", ())),
    }


def _termination_record_identity(record):
    record_key = record.get("record_key", None)

    if record_key is not None:
        return repr(record_key)

    cell = record.get("cell", None)

    if cell is not None:
        return ("cell", id(cell))

    return (
        record.get("source"),
        repr(record.get("expression", None)),
        tuple(record.get("path_key", ())),
    )


def _primitive_candidate_summary(self, candidate):
    block = tuple(candidate.get("block", ()))
    left = tuple(candidate.get("left", ()))
    right = tuple(candidate.get("right", ()))
    terminations = tuple(candidate.get("termination_records", ()))
    summary = {
        "kind": candidate.get("kind", "mp_cell"),
        "source": candidate.get("source", "resolved_block"),
        "left": left,
        "block": block,
        "right": right,
        "block_span": (
            len(left),
            len(left) + len(block),
        ),
        "termination_count": len(terminations),
        "terminations": tuple(
            _termination_record_summary(record)
            for record in terminations
        ),
    }

    if candidate.get("kind") == "bridge_replacement":
        summary.update({
            "source": "bridge_replacement",
            "side": candidate.get("side"),
            "original_product_factors": tuple(candidate.get("original_product_factors", ())),
            "original_replaced_block": tuple(candidate.get("original_replaced_block", ())),
            "original_replaced_span": candidate.get("original_replaced_span"),
            "source_product_factors": tuple(candidate.get("source_product_factors", ())),
            "replacement_block": tuple(candidate.get("replacement_block", ())),
            "replacement_span": candidate.get("replacement_span"),
            "primitive_block": tuple(candidate.get("primitive_block", block)),
            "primitive_block_span": candidate.get("primitive_block_span"),
            "bridge_replacements": [
                {
                    "from": tuple(record.get("from", record.get("target_factors", ()))),
                    "to": tuple(record.get("to", record.get("replacement_factors", ()))),
                    "occurrence_span": record.get(
                        "occurrence_span",
                        record.get("occurrence_span_before"),
                    ),
                }
                for record in candidate.get("bridge_replacements", [])
            ],
        })

    return summary


def _profile_summary(profile):
    return {
        "context": profile.get("context"),
        "span": profile.get("span"),
        "block": tuple(profile.get("block", ())),
        "prefix_length": profile.get("prefix_length", 0),
    }


def _unsettled_termination_pair_summary(
    first_index,
    second_index,
    first_profile,
    second_profile,
    first_termination,
    second_termination,
):
    return {
        "first_candidate": first_index,
        "second_candidate": second_index,
        "context": first_profile.get("context"),
        "first_span": first_profile.get("span"),
        "second_span": second_profile.get("span"),
        "first_termination": _termination_record_summary(first_termination),
        "second_termination": _termination_record_summary(second_termination),
    }


def _generated_items_from_result(items):
    if items is None:
        return []

    if isinstance(items, dict):
        out = []

        for key in ("have_primitives", "no_obvious_primitives"):
            out.extend(items.get(key, []))

        return out

    return list(items)


def _remember_split_item(self, target, item, have_primitives, no_obvious_primitives, have_keys, no_obvious_keys):
    key = self.generation_item_key(item)

    if target == "have":
        if key not in have_keys:
            have_keys.add(key)
            have_primitives.append(item)
        return

    if key not in no_obvious_keys:
        no_obvious_keys.add(key)
        no_obvious_primitives.append(item)


def _split_generated_by_primitive_status(
    self,
    generated,
    record=True,
    include_primitive_details=True,
):
    have_primitives = []
    no_obvious_primitives = []
    primitive_data = {}
    have_keys = set()
    no_obvious_keys = set()

    for M in _generated_items_from_result(generated):
        if not isinstance(M, MasseyProduct):
            item_key = self.generation_item_key(M)
            product_data = getattr(self, "generated_mp_expression_data", {}).get(item_key, {})
            primitive_data[item_key] = product_data

            if product_data.get("classification") == "have_primitives":
                _remember_split_item(
                    self,
                    "have",
                    M,
                    have_primitives,
                    no_obvious_primitives,
                    have_keys,
                    no_obvious_keys,
                )
            else:
                _remember_split_item(
                    self,
                    "no_obvious",
                    M,
                    have_primitives,
                    no_obvious_primitives,
                    have_keys,
                    no_obvious_keys,
                )

            continue

        primitive_record = self.classify_massey_product_primitives(
            M,
            record=record,
            minimal_only=True,
            include_primitive_details=include_primitive_details,
        )
        primitive_data[self.mp_key(*M.inputs)] = primitive_record

        if primitive_record.get("has_obvious_primitive"):
            obvious_M = primitive_record.get("obvious_massey_product", None)

            if obvious_M is not None:
                obvious_key = self.mp_key(*obvious_M.inputs)
                primitive_data[obvious_key] = {
                    **primitive_record,
                    "source_generated_massey_product": M,
                }
                _remember_split_item(
                    self,
                    "have",
                    obvious_M,
                    have_primitives,
                    no_obvious_primitives,
                    have_keys,
                    no_obvious_keys,
                )
            else:
                _remember_split_item(
                    self,
                    "have",
                    M,
                    have_primitives,
                    no_obvious_primitives,
                    have_keys,
                    no_obvious_keys,
                )
        else:
            induced = primitive_record.get("induced_massey_products", [])

            if induced:
                for induced_M in induced:
                    induced_key = self.mp_key(*induced_M.inputs)
                    primitive_data[induced_key] = {
                        **primitive_record,
                        "source_generated_massey_product": M,
                    }
                    _remember_split_item(
                        self,
                        "no_obvious",
                        induced_M,
                        have_primitives,
                        no_obvious_primitives,
                        have_keys,
                        no_obvious_keys,
                    )
            else:
                _remember_split_item(
                    self,
                    "no_obvious",
                    M,
                    have_primitives,
                    no_obvious_primitives,
                    have_keys,
                    no_obvious_keys,
                )

    result = {
        "have_primitives": have_primitives,
        "no_obvious_primitives": no_obvious_primitives,
        "primitive_data": primitive_data,
        "include_primitive_details": include_primitive_details,
    }

    print("Have primitives:", have_primitives)
    print("No obvious primitives:", no_obvious_primitives)

    return result


def generate_massey_products(
    self,
    cells=None,
    record=True,
    verbose=False,
    split_by_primitives=True,
    include_primitive_details=True,
):
    """
    Generate Massey products, optionally classifying primitive status lazily.

    The notebook implementation is preserved as
    _cyclic_base_generate_massey_products.  Passing
    include_primitive_details=False still computes the generated names and
    primitive-status buckets, but returns summaries instead of concrete
    primitive formulas/candidates.
    """

    use_fast_generation = (
        not include_primitive_details
        and getattr(self, "fast_massey_generation", True)
    )

    if use_fast_generation:
        generated = self.fast_generate_massey_products(
            cells=cells,
            record=record,
            verbose=verbose,
        )

        if not split_by_primitives:
            return generated

        return _split_generated_by_primitive_status(
            self,
            generated,
            record=record,
            include_primitive_details=False,
        )

    base = getattr(
        type(self),
        "_cyclic_base_generate_massey_products",
        None,
    )

    if base is None:
        return [] if not split_by_primitives else _split_generated_by_primitive_status(
            self,
            [],
            record=record,
            include_primitive_details=include_primitive_details,
        )

    if not split_by_primitives:
        return base(
            self,
            cells=cells,
            record=record,
            verbose=verbose,
            split_by_primitives=False,
        )

    if include_primitive_details:
        return base(
            self,
            cells=cells,
            record=record,
            verbose=verbose,
            split_by_primitives=True,
        )

    generated = base(
        self,
        cells=cells,
        record=record,
        verbose=verbose,
        split_by_primitives=False,
    )

    return _split_generated_by_primitive_status(
        self,
        generated,
        record=record,
        include_primitive_details=False,
    )


def classify_massey_product_primitive_summary(
    self,
    M,
    record=True,
    minimal_only=True,
):
    """
    Primitive-status classifier that keeps touched-block metadata only.

    This avoids materializing the actual primitive expression such as
    v[x*y]*z +/- x*v[y*z].  It still records which candidate blocks/profiles
    made a status decision.
    """

    if isinstance(M, MasseyProduct) and self.has_zero_mp_input(M.inputs):
        result = _empty_primitive_classification(
            has_obvious_primitive=True,
            detail_mode="summary",
        )
        result["obvious_massey_product"] = M
        result["obvious_massey_products"] = [M]
        return result

    tower_records = _fast_tower_records(self)

    if isinstance(M, MasseyProduct):
        tower_report = _tower_elimination_report_with_replacements(
            self,
            M.inputs,
            records=tower_records,
        )

        if tower_report is not None:
            result = _empty_primitive_classification(
                has_obvious_primitive=True,
                detail_mode="summary",
            )
            result["obvious_massey_product"] = M
            result["obvious_massey_products"] = [M]
            result["candidate_summaries"] = [{
                "kind": "completed_massey_tower",
                "source": "completed_massey_tower",
                "block": tuple(M.inputs),
                "flat_word": tuple(tower_report.get("flat_word", ())),
                "seed_inputs": tuple(tower_report.get("seed_inputs", ())),
            }]
            return result

        pair_tower_report = self.pair_tower_elimination_report(
            *M.inputs,
            tower_records=tower_records,
        )

        if pair_tower_report is not None:
            result = _empty_primitive_classification(
                has_obvious_primitive=True,
                detail_mode="summary",
            )
            result["obvious_massey_product"] = M
            result["obvious_massey_products"] = [M]
            result["candidate_summaries"] = [{
                "kind": "completed_massey_pair_tower",
                "source": "completed_massey_pair_tower",
                "block": tuple(M.inputs),
                "flat_word": tuple(pair_tower_report.get("flat_word", ())),
                "left_seed_inputs": tuple(pair_tower_report.get("left_seed_inputs", ())),
                "right_seed_inputs": tuple(pair_tower_report.get("right_seed_inputs", ())),
                "boundary_split": pair_tower_report.get("boundary_split"),
            }]
            return result

    product = self.massey_product_input_product(M)

    if product is None:
        return _empty_primitive_classification(detail_mode="summary")

    ambient_factors = tuple(product.factors)
    primitive_keys, _primitive_records, source_by_key = _fast_known_mp_primitive_records(self)
    termination_by_key = _fast_known_mp_termination_records(self)
    candidates = _fast_primitive_candidates_for_product(
        self,
        product,
        minimal_only=minimal_only,
        primitive_keys=primitive_keys,
        source_by_key=source_by_key,
        termination_by_key=termination_by_key,
        tower_records=tower_records,
    )
    profile_groups = [
        self.primitive_candidate_profiles_for_obvious_test(
            candidate,
            ambient_factors,
        )
        for candidate in candidates
    ]
    candidate_summaries = [
        _primitive_candidate_summary(self, candidate)
        for candidate in candidates
    ]
    profile_summaries = [
        [_profile_summary(profile) for profile in profiles]
        for profiles in profile_groups
    ]
    induced_massey_products = []
    induced_keys = set()
    bridge_interval_summaries = []
    unsettled_termination_pairs = []
    unsettled_pair_keys = set()

    def remember_unsettled_pair(
        first_index,
        second_index,
        first_profile,
        second_profile,
        first_termination,
        second_termination,
    ):
        first_key = _termination_record_identity(first_termination)
        second_key = _termination_record_identity(second_termination)

        if first_key == second_key:
            return

        ordered_keys = tuple(sorted((repr(first_key), repr(second_key))))
        pair_key = (
            repr(first_profile.get("context_key")),
            first_profile.get("span"),
            second_profile.get("span"),
            ordered_keys,
        )

        if pair_key in unsettled_pair_keys:
            return

        unsettled_pair_keys.add(pair_key)
        unsettled_termination_pairs.append(
            _unsettled_termination_pair_summary(
                first_index,
                second_index,
                first_profile,
                second_profile,
                first_termination,
                second_termination,
            )
        )

    for i, candidate in enumerate(candidates):
        termination_records = tuple(candidate.get("termination_records", ()))

        if len(termination_records) < 2:
            continue

        for profile in profile_groups[i]:
            for first_index in range(len(termination_records)):
                for second_index in range(first_index + 1, len(termination_records)):
                    remember_unsettled_pair(
                        i,
                        i,
                        profile,
                        profile,
                        termination_records[first_index],
                        termination_records[second_index],
                    )

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            first_terminations = tuple(candidates[i].get("termination_records", ()))
            second_terminations = tuple(candidates[j].get("termination_records", ()))

            if not first_terminations or not second_terminations:
                continue

            for first_profile in profile_groups[i]:
                for second_profile in profile_groups[j]:
                    if first_profile["context_key"] != second_profile["context_key"]:
                        continue

                    if self.spans_are_disjoint(
                        first_profile["span"],
                        second_profile["span"],
                    ):
                        continue

                    for first_termination in first_terminations:
                        for second_termination in second_terminations:
                            remember_unsettled_pair(
                                i,
                                j,
                                first_profile,
                                second_profile,
                                first_termination,
                                second_termination,
                            )

    if record:
        key = self.generation_item_key(M)
        summaries = getattr(self, "mp_primitive_candidate_summaries", {})
        summaries[key] = candidate_summaries
        self.mp_primitive_candidate_summaries = summaries

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            for first_profile in profile_groups[i]:
                for second_profile in profile_groups[j]:
                    if first_profile["context_key"] != second_profile["context_key"]:
                        continue

                    if not self.spans_are_disjoint(
                        first_profile["span"],
                        second_profile["span"],
                    ):
                        # Summary mode classifies the generated product itself.
                        # Product-level induced names are generated by the fast
                        # overlap pass, so do not replace an m_n by a lower m_3
                        # while bucketing primitive status.
                        continue

                    if first_profile["span"][0] <= second_profile["span"][0]:
                        left_profile = first_profile
                        right_profile = second_profile
                    else:
                        left_profile = second_profile
                        right_profile = first_profile

                    split_index = left_profile["span"][1]
                    context_factors = tuple(left_profile["context_factors"])
                    obvious_massey_product = None
                    zero_inputs = self.zero_m3_inputs_from_disjoint_profiles(
                        left_profile,
                        right_profile,
                    )

                    if zero_inputs is not None:
                        obvious_massey_product = _fast_register_generated_mp_if_defined(
                            self,
                            zero_inputs,
                            primitive_keys,
                            tower_records=tower_records,
                            record=record,
                        )

                    if obvious_massey_product is None:
                        continue

                    return {
                        "has_obvious_primitive": True,
                        "candidates": [],
                        "candidate_summaries": candidate_summaries,
                        "profiles": [],
                        "profile_summaries": profile_summaries,
                        "obvious_pair": None,
                        "obvious_pair_summaries": (
                            candidate_summaries[i],
                            candidate_summaries[j],
                        ),
                        "obvious_profiles": (),
                        "obvious_profile_summaries": (
                            _profile_summary(first_profile),
                            _profile_summary(second_profile),
                        ),
                        "ordered_obvious_profiles": (),
                        "ordered_obvious_profile_summaries": (
                            _profile_summary(left_profile),
                            _profile_summary(right_profile),
                        ),
                        "obvious_split": split_index,
                        "obvious_factorization": (
                            context_factors[:split_index],
                            context_factors[split_index:],
                        ),
                        "ambient_product": product,
                        "obvious_massey_product": obvious_massey_product,
                        "obvious_massey_products": (
                            [obvious_massey_product]
                            if obvious_massey_product is not None
                            else []
                        ),
                        "induced_massey_products": induced_massey_products,
                        "bridge_interval_summaries": bridge_interval_summaries,
                        "unsettled_termination_pairs": unsettled_termination_pairs,
                        "detail_mode": "summary",
                    }

    return {
        "has_obvious_primitive": False,
        "candidates": [],
        "candidate_summaries": candidate_summaries,
        "profiles": [],
        "profile_summaries": profile_summaries,
        "obvious_pair": None,
        "obvious_split": None,
        "obvious_factorization": None,
        "ambient_product": product,
        "obvious_massey_product": None,
        "obvious_massey_products": [],
        "induced_massey_products": induced_massey_products,
        "bridge_interval_summaries": bridge_interval_summaries,
        "unsettled_termination_pairs": unsettled_termination_pairs,
        "detail_mode": "summary",
    }


def classify_massey_product_primitives(
    self,
    M,
    record=True,
    minimal_only=True,
    include_primitive_details=True,
):
    """
    Use the notebook classifier, but do not count zero-input witnesses as
    actual primitives for a generated Massey product.
    """

    if not include_primitive_details:
        return self.classify_massey_product_primitive_summary(
            M,
            record=record,
            minimal_only=minimal_only,
        )

    base = getattr(
        type(self),
        "_cyclic_base_classify_massey_product_primitives",
        None,
    )

    if base is None:
        return {
            "has_obvious_primitive": False,
            "candidates": [],
            "profiles": [],
            "obvious_pair": None,
            "obvious_split": None,
            "obvious_factorization": None,
            "obvious_massey_product": None,
            "obvious_massey_products": [],
            "induced_massey_products": [],
        }

    if isinstance(M, MasseyProduct):
        tower_report = _tower_elimination_report_with_replacements(
            self,
            M.inputs,
        )

        if tower_report is not None:
            result = _empty_primitive_classification(
                has_obvious_primitive=True,
            )
            result["obvious_massey_product"] = M
            result["obvious_massey_products"] = [M]
            result["candidate_summaries"] = [{
                "kind": "completed_massey_tower",
                "source": "completed_massey_tower",
                "block": tuple(M.inputs),
                "flat_word": tuple(tower_report.get("flat_word", ())),
                "seed_inputs": tuple(tower_report.get("seed_inputs", ())),
                "presentation_factors": tuple(tower_report.get("presentation_factors", ())),
                "replacement_used": bool(tower_report.get("replacement_used", False)),
            }]
            return result

        pair_tower_report = self.pair_tower_elimination_report(*M.inputs)

        if pair_tower_report is not None:
            result = _empty_primitive_classification(
                has_obvious_primitive=True,
            )
            result["obvious_massey_product"] = M
            result["obvious_massey_products"] = [M]
            result["candidate_summaries"] = [{
                "kind": "completed_massey_pair_tower",
                "source": "completed_massey_pair_tower",
                "block": tuple(M.inputs),
                "flat_word": tuple(pair_tower_report.get("flat_word", ())),
                "left_seed_inputs": tuple(pair_tower_report.get("left_seed_inputs", ())),
                "right_seed_inputs": tuple(pair_tower_report.get("right_seed_inputs", ())),
                "boundary_split": pair_tower_report.get("boundary_split"),
            }]
            return result

    result = base(
        self,
        M,
        record=record,
        minimal_only=minimal_only,
    )

    if not isinstance(result, dict):
        return result

    if not result.get("has_obvious_primitive"):
        return result

    if result.get("obvious_massey_product") is not None:
        return result

    if result.get("obvious_massey_products"):
        return result

    corrected = dict(result)
    corrected["has_obvious_primitive"] = False
    corrected["discarded_zero_obvious_primitive"] = True
    corrected["discarded_obvious_pair"] = result.get("obvious_pair")
    corrected["discarded_obvious_profiles"] = result.get("obvious_profiles")
    corrected["discarded_obvious_split"] = result.get("obvious_split")
    corrected["discarded_obvious_factorization"] = result.get("obvious_factorization")
    corrected["obvious_pair"] = None
    corrected["obvious_profiles"] = ()
    corrected["ordered_obvious_profiles"] = ()
    corrected["obvious_split"] = None
    corrected["obvious_factorization"] = None
    corrected["obvious_massey_product"] = None
    corrected["obvious_massey_products"] = []
    corrected["induced_massey_products"] = []
    return corrected


def bridge_interval_representative_data(self, record_data, interval_data):
    """
    Optionally suppress the expanded bridge-interval representative.

    The detailed notebook method builds an actual cycle representative from
    primitive candidates.  In metadata-only generation the game only needs the
    interval/touched-block data, so returning None skips that expansion while
    keeping the detailed method available outside the fast context.
    """

    if getattr(self, "_suppress_primitive_expansion", False):
        return None

    base = getattr(
        type(self),
        "_cyclic_base_bridge_interval_representative_data",
        None,
    )

    if base is None:
        return None

    return base(self, record_data, interval_data)


_BRIDGE_REPLACEMENT_DEPTH_UNSET = object()


def _bridge_replacement_depth_limit(
    self,
    max_depth=_BRIDGE_REPLACEMENT_DEPTH_UNSET,
):
    if max_depth is _BRIDGE_REPLACEMENT_DEPTH_UNSET:
        max_depth = getattr(self, "bridge_replacement_max_depth", None)

    if isinstance(max_depth, str):
        normalized = max_depth.strip().lower()

        if normalized in {"legacy", "full", "unbounded", "none"}:
            return None

        if normalized in {"off", "disabled", "false"}:
            return 0

    if max_depth is None:
        return None

    try:
        return max(0, int(max_depth))
    except (TypeError, ValueError):
        return None


def _metadata_replacement_edge_records(self):
    """
    Replacement edges for primitive-certificate search.

    Product-frontier searches keep the self-expanding guard in place for
    context-free quotienting.  Primitive certificates carry origin metadata, so
    they may use bridge and A-inf replacements in any order.  A guarded
    self-expanding edge can be used only on factors still coming from the
    original product, never on factors introduced by a previous replacement.
    A-inf edges are algebraic slides, so the metadata search treats them as
    reversible even though replacement_edge_records stores one orientation.
    """

    try:
        raw_edges = list(self.replacement_edge_records(
            filter_self_expanding=False,
        ))
    except TypeError:
        try:
            raw_edges = list(self.replacement_edge_records())
        except Exception:
            raw_edges = []
    except Exception:
        raw_edges = []

    edges = []
    seen = set()

    def add_edge(edge, reversed_ainf=False):
        edge = dict(edge)

        if reversed_ainf:
            for left_key, right_key in (
                ("target_product", "replacement_product"),
                ("target_factors", "replacement_factors"),
                ("target_key", "replacement_key"),
            ):
                left_value = edge.get(left_key)
                edge[left_key] = edge.get(right_key)
                edge[right_key] = left_value

            edge["reversed_ainf"] = True

        if edge.get("target_factors") is None or edge.get("replacement_factors") is None:
            return

        if repr(edge.get("target_key")) == repr(edge.get("replacement_key")):
            return

        if (
            edge.get("replacement_type", "bridge") == "bridge"
            and _edge_is_self_expanding_replacement(self, edge)
        ):
            edge["guarded_self_expanding"] = True

        edge["target_recursive_key_reprs"] = tuple(sorted(
            _replacement_target_letter_key_reprs(
                self,
                edge.get("target_factors", ()),
            )
        ))
        edge["replacement_recursive_key_reprs"] = tuple(sorted(
            _replacement_top_level_key_reprs(
                self,
                edge.get("replacement_factors", ()),
            )
        ))

        key = (
            edge.get("replacement_type", "bridge"),
            repr(edge.get("target_key")),
            repr(edge.get("replacement_key")),
            bool(edge.get("reversed_ainf")),
        )

        if key in seen:
            return

        seen.add(key)
        edges.append(edge)

    for edge in raw_edges:
        add_edge(edge)

        if edge.get("replacement_type", "bridge") != "bridge":
            add_edge(edge, reversed_ainf=True)

    return edges


def _metadata_factor_is_atomic_for_guarded_expansion(factor):
    if isinstance(factor, MasseyProduct):
        return len(tuple(getattr(factor, "inputs", ()))) <= 1

    return True


def _metadata_can_apply_guarded_self_expansion(
    edge,
    current_origins,
    start,
    stop,
    path_records,
):
    if not edge.get("guarded_self_expanding"):
        return True

    if any(origin is None for origin in tuple(current_origins)[start:stop]):
        return False

    return all(
        _metadata_factor_is_atomic_for_guarded_expansion(factor)
        for factor in tuple(edge.get("target_factors", ()))
    )


def _metadata_bridge_replacement_primitive_candidates(
    self,
    P,
    record=True,
    minimal_only=True,
    max_depth=_BRIDGE_REPLACEMENT_DEPTH_UNSET,
    allow_single_factor=False,
    allow_guarded_self_expanding_after_replacement=False,
):
    if isinstance(P, MasseyProduct):
        P = P.as_product()

    if not isinstance(P, MPProduct):
        return []

    self.ensure_bridge_history()

    try:
        factors = self.canonical_mp_factors(P)
    except Exception:
        return []

    if len(factors) < 1:
        return []

    if len(factors) < 2 and not allow_single_factor:
        return []

    primitive_keys, _primitive_records, source_by_key = _fast_known_mp_primitive_records(self)
    termination_by_key = _fast_known_mp_termination_records(self)
    tower_records = _fast_tower_records(self)

    def factors_key(some_factors):
        return tuple(self.mp_factor_key(factor) for factor in tuple(some_factors))

    edges = _metadata_replacement_edge_records(self)

    if not edges:
        return []

    candidates = []

    def replacement_side_for_span(start, stop, state_len):
        if start == 0:
            return "right"

        if stop == state_len:
            return "left"

        return "middle"

    def path_profile_contexts(path_records, primitive_span):
        contexts = []

        for prefix_len in range(0, len(path_records) + 1):
            if prefix_len == 0:
                context = "original"
                context_factors = factors
                context_key = ("original", self.mp_factor_tuple_key(context_factors))
            else:
                context = "bridge_prefix"
                context_factors = tuple(path_records[prefix_len - 1]["source_product_after"])
                prefix_key = tuple(
                    self.bridge_edge_key(edge)
                    for edge in path_records[:prefix_len]
                )
                context_key = (
                    "bridge_prefix",
                    self.mp_factor_tuple_key(context_factors),
                    prefix_key,
                )

            touched = set()
            context_origins = list(range(len(context_factors)))

            for record in path_records[prefix_len:]:
                start, stop = record["occurrence_span_before"]
                touched.update(
                    origin
                    for origin in context_origins[start:stop]
                    if origin is not None
                )
                context_origins = (
                    context_origins[:start]
                    + [None] * len(record["replacement_factors"])
                    + context_origins[stop:]
                )

            if primitive_span is not None:
                for i in range(primitive_span[0], primitive_span[1]):
                    if 0 <= i < len(context_origins):
                        touched.add(context_origins[i])

            span = self.span_from_touched_positions(touched)

            if span is None:
                continue

            contexts.append({
                "context": context,
                "context_factors": context_factors,
                "context_key": context_key,
                "span": span,
                "block": tuple(context_factors[span[0]:span[1]]),
                "prefix_length": prefix_len,
            })

        return contexts

    def search_replacement_state(current_factors, path_records):
        source_product = MPProduct(self, current_factors)
        source_candidates = _fast_primitive_candidates_for_product(
            self,
            source_product,
            primitive_keys=primitive_keys,
            source_by_key=source_by_key,
            termination_by_key=termination_by_key,
            tower_records=tower_records,
            minimal_only=minimal_only,
        )

        for source_candidate in source_candidates:
            source_block = tuple(source_candidate.get("block", ()))
            source_left = tuple(source_candidate.get("left", ()))
            source_right = tuple(source_candidate.get("right", ()))
            termination_records = tuple(source_candidate.get("termination_records", ()))
            source_block_start = len(source_left)
            source_block_end = source_block_start + len(source_block)
            primitive_span = (source_block_start, source_block_end)
            profile_contexts = path_profile_contexts(path_records, primitive_span)

            if not profile_contexts:
                continue

            bridge_replacements = [
                {
                    "from": record["target_factors"],
                    "to": record["replacement_factors"],
                    "bridge": record["bridge_cell"],
                    "bridge_expression": record["bridge_expression"],
                    "occurrence_span": record["occurrence_span_before"],
                    "source_before": record["source_product_before"],
                    "source_after": record["source_product_after"],
                }
                for record in path_records
            ]
            first_record = path_records[0]
            last_record = path_records[-1]
            replacement_record = {
                "original_product_factors": factors,
                "original_replaced_block": first_record["target_factors"],
                "original_replaced_span": first_record["occurrence_span_before"],
                "first_step_source_product_factors": first_record["source_product_after"],
                "first_step_replacement_span": first_record["replacement_span_after"],
                "source_product_factors": current_factors,
                "replacement_block": last_record["replacement_factors"],
                "replacement_span": last_record["replacement_span_after"],
                "primitive_block": source_block,
                "primitive_block_span": primitive_span,
                "primitive_left": source_left,
                "primitive_right": source_right,
                "bridge_replacements": bridge_replacements,
                "profile_contexts": profile_contexts,
                "termination_records": termination_records,
                "termination_count": len(termination_records),
            }

            candidates.append({
                "kind": "bridge_replacement",
                "deferred_primitive": True,
                "side": replacement_side_for_span(
                    first_record["occurrence_span_before"][0],
                    first_record["occurrence_span_before"][1],
                    len(factors),
                ),
                "left": (),
                "right": (),
                "block": source_block,
                "original_product_factors": factors,
                "original_replaced_block": first_record["target_factors"],
                "original_replaced_span": first_record["occurrence_span_before"],
                "first_step_source_product_factors": first_record["source_product_after"],
                "first_step_replacement_span": first_record["replacement_span_after"],
                "source_product_factors": current_factors,
                "replacement_block": last_record["replacement_factors"],
                "replacement_span": last_record["replacement_span_after"],
                "primitive_block": source_block,
                "primitive_block_span": primitive_span,
                "primitive_left": source_left,
                "primitive_right": source_right,
                "bridge_replacements": bridge_replacements,
                "bridge_left_factors": tuple(factors[:first_record["occurrence_span_before"][0]]),
                "bridge_right_factors": tuple(factors[first_record["occurrence_span_before"][1]:]),
                "replacement_record": replacement_record,
                "sign_source": (),
                "bridge": first_record["bridge_cell"],
                "bridge_expression": first_record["bridge_expression"],
                "bridge_path": list(path_records),
                "target_term": first_record["target_product"],
                "replacement_term": last_record["replacement_product"],
                "replacement_factors": current_factors,
                "source_primitive": source_candidate,
                "profile_contexts": profile_contexts,
                "termination_records": termination_records,
                "termination_count": len(termination_records),
            })

    queue = [(
        factors,
        list(range(len(factors))),
        [],
        {factors_key(factors)},
        frozenset(),
    )]
    searched_states = 0
    state_limit = getattr(self, "bridge_replacement_search_state_limit", 2000)

    try:
        state_limit = max(1, int(state_limit))
    except (TypeError, ValueError):
        state_limit = 2000

    while queue:
        searched_states += 1

        if searched_states > state_limit:
            break

        (
            current_factors,
            current_origins,
            path_records,
            seen_state_keys,
            replaced_key_reprs,
        ) = queue.pop(0)

        if path_records:
            search_replacement_state(current_factors, path_records)

        state_len = len(current_factors)

        for edge in edges:
            target_len = len(edge["target_factors"])

            if state_len < target_len:
                continue

            for start in range(0, state_len - target_len + 1):
                stop = start + target_len

                if not self.mp_factors_equal(
                    current_factors[start:stop],
                    edge["target_factors"],
                ):
                    continue

                if (
                    not allow_guarded_self_expanding_after_replacement
                    and not _metadata_can_apply_guarded_self_expansion(
                        edge,
                        current_origins,
                        start,
                        stop,
                        path_records,
                    )
                ):
                    continue

                if _replacement_edge_reintroduces_replaced_key(
                    self,
                    edge,
                    replaced_key_reprs,
                ):
                    continue

                next_factors = (
                    current_factors[:start]
                    + edge["replacement_factors"]
                    + current_factors[stop:]
                )
                next_key = factors_key(next_factors)

                if next_key in seen_state_keys:
                    continue

                next_origins = (
                    current_origins[:start]
                    + [None] * len(edge["replacement_factors"])
                    + current_origins[stop:]
                )
                path_record = dict(edge)
                path_record.update({
                    "from": edge["target_factors"],
                    "to": edge["replacement_factors"],
                    "occurrence_span_before": (start, stop),
                    "replacement_span_after": (start, start + len(edge["replacement_factors"])),
                    "source_product_before": current_factors,
                    "source_product_after": next_factors,
                    "origins_before": tuple(current_origins),
                    "origins_after": tuple(next_origins),
                })
                queue.append((
                    next_factors,
                    next_origins,
                    path_records + [path_record],
                    seen_state_keys | {next_key},
                    (
                        replaced_key_reprs
                        | _replacement_edge_target_key_reprs(self, edge)
                    ),
                ))

    out = []
    seen = set()

    for candidate in candidates:
        source_key = self.primitive_candidate_interval_key(
            candidate.get("source_primitive", None)
        )
        path_key = tuple(
            (
                record.get("occurrence_span_before"),
                record.get("target_key"),
                record.get("replacement_key"),
            )
            for record in candidate.get("bridge_path", [])
        )
        key = (
            source_key,
            path_key,
            candidate.get("primitive_block_span", None),
        )

        if key not in seen:
            seen.add(key)
            out.append(candidate)

    if record:
        key = tuple(factors)
        self.mp_primitive_candidates[key] = out

    return out


def bridge_replacement_primitive_candidates(
    self,
    P,
    record=True,
    minimal_only=True,
    max_depth=_BRIDGE_REPLACEMENT_DEPTH_UNSET,
):
    return _metadata_bridge_replacement_primitive_candidates(
        self,
        P,
        record=record,
        minimal_only=minimal_only,
        max_depth=max_depth,
    )


def _massey_tower_find_rotation_index(self, rotations, inputs):
    input_key = _massey_tower_factor_keys(self, inputs)

    for index, rotation in enumerate(rotations):
        if _massey_tower_factor_keys(self, rotation) == input_key:
            return index

    return None


def _massey_tower_cyclic_word(base_inputs, offset, length):
    base_inputs = tuple(base_inputs)
    repeated = list(base_inputs)

    while len(repeated) < offset + length:
        repeated.extend(base_inputs)

    return tuple(repeated[offset:offset + length])


def _massey_tower_direct_cycle_status(self, inputs):
    inputs = tuple(inputs)

    try:
        defined = self.can_define_mp(*inputs)
    except Exception:
        defined = False

    M = None
    cycle = False
    error = None

    if defined:
        try:
            M = self.virtual_mp(*inputs)
            if (
                _massey_formula_disabled(self)
                or getattr(self, "_suppress_primitive_expansion", False)
            ):
                cycle = True
                error = "Accepted defined Massey product certificate."
            else:
                cycle = self.d(M.expand()).is_zero()
        except Exception as exc:
            error = str(exc)
            M = None
            cycle = False

    return {
        "defined_now": defined,
        "massey_product": M,
        "cycle_now": cycle,
        "error": error,
    }


def massey_orbit_tower_plan(
    self,
    seed_inputs,
    leave_inputs=None,
    require_all_other_rotations=True,
    max_level=None,
    include_resolved=False,
    verify_now=True,
):
    """
    Plan the pointed tower forced by one cyclic Massey orbit.

    The chosen leave_inputs rotation is treated as the missing representative.
    Consecutive directly resolved rotations after it generate a triangular
    tower of higher pure Massey products, independent of the product frontier.
    """

    seed_inputs = tuple(self.normalize_mp_inputs(tuple(seed_inputs)))

    if len(seed_inputs) < 3:
        return {
            "status": "blocked",
            "reason": "tower seed must have arity at least 3",
            "attachments": [],
            "levels": [],
        }

    if leave_inputs is None:
        leave_inputs = seed_inputs
    else:
        leave_inputs = tuple(self.normalize_mp_inputs(tuple(leave_inputs)))

    seed_rotations = self.cyclic_rotations(seed_inputs)
    seed_leave_index = _massey_tower_find_rotation_index(
        self,
        seed_rotations,
        leave_inputs,
    )

    if seed_leave_index is None:
        return {
            "status": "blocked",
            "reason": "leave_inputs is not a cyclic rotation of seed_inputs",
            "attachments": [],
            "levels": [],
        }

    base_inputs = seed_rotations[seed_leave_index]
    rotations = self.cyclic_rotations(base_inputs)
    resolved = getattr(self, "resolved_massey_products", {})
    base_records = []
    missing_other_rotations = []

    for offset, rotation in enumerate(rotations):
        key = self.mp_key(*rotation)
        primitive = resolved.get(key, None)

        try:
            defined = self.can_define_mp(*rotation)
        except Exception:
            defined = False

        record = {
            "offset": offset,
            "inputs": rotation,
            "defined": defined,
            "directly_resolved": primitive is not None,
            "primitive": primitive,
            "is_leave": offset == 0,
        }
        base_records.append(record)

        if (
            offset != 0
            and require_all_other_rotations
            and primitive is None
        ):
            missing_other_rotations.append(record)

    if missing_other_rotations:
        return {
            "status": "blocked_base_orbit",
            "reason": "not all non-left cyclic rotations are directly resolved",
            "base_inputs": base_inputs,
            "leave_inputs": base_inputs,
            "base_rotations": base_records,
            "missing_other_rotations": missing_other_rotations,
            "attachments": [],
            "levels": [],
        }

    run_length = 0

    for record in base_records[1:]:
        if not record["directly_resolved"]:
            break

        run_length += 1

    if run_length < 2:
        return {
            "status": "complete",
            "reason": "there is no nontrivial resolved run after leave_inputs",
            "base_inputs": base_inputs,
            "leave_inputs": base_inputs,
            "run_length": run_length,
            "base_rotations": base_records,
            "attachments": [],
            "levels": [],
        }

    highest_level = run_length - 1

    if max_level is not None:
        highest_level = min(highest_level, int(max_level))

    levels = []
    attachments = []

    for level in range(1, highest_level + 1):
        arity = len(base_inputs) + level
        count = run_length - level
        level_items = []

        for offset in range(1, count + 1):
            inputs = _massey_tower_cyclic_word(base_inputs, offset, arity)
            key = self.mp_key(*inputs)
            primitive = resolved.get(key, None)
            status = (
                _massey_tower_direct_cycle_status(self, inputs)
                if verify_now
                else {
                    "defined_now": None,
                    "massey_product": None,
                    "cycle_now": None,
                    "error": None,
                }
            )
            entry = {
                "kind": "pure_massey",
                "reason": "massey_orbit_tower",
                "level": level,
                "arity": arity,
                "offset": offset,
                "inputs": inputs,
                "key": key,
                "resolved": primitive is not None,
                "primitive": primitive,
                "defined_now": status["defined_now"],
                "cycle_now": status["cycle_now"],
                "massey_product": status["massey_product"],
                "error": status["error"],
            }
            level_items.append(entry)

            if include_resolved or primitive is None:
                attachments.append(entry)

        levels.append({
            "level": level,
            "arity": arity,
            "candidates": level_items,
        })

    unresolved = [
        item
        for item in attachments
        if not item.get("resolved")
    ]

    if not unresolved:
        return {
            "status": "complete",
            "reason": "tower candidates are already resolved",
            "base_inputs": base_inputs,
            "leave_inputs": base_inputs,
            "run_length": run_length,
            "base_rotations": base_records,
            "attachments": [],
            "levels": levels,
        }

    return {
        "status": "tower",
        "reason": "planned pointed Massey orbit tower",
        "base_inputs": base_inputs,
        "leave_inputs": base_inputs,
        "run_length": run_length,
        "base_rotations": base_records,
        "attachments": unresolved,
        "levels": levels,
    }


def apply_massey_orbit_tower(
    self,
    seed_inputs,
    leave_inputs=None,
    require_all_other_rotations=True,
    max_level=None,
    max_cells=50,
    dry_run=False,
    verify_cycles=True,
):
    """
    Attach the pointed Massey orbit tower level by level.
    """

    self.ensure_attachment_history()
    start_history_length = len(getattr(self, "attachment_history", []))
    plan = self.massey_orbit_tower_plan(
        seed_inputs,
        leave_inputs=leave_inputs,
        require_all_other_rotations=require_all_other_rotations,
        max_level=max_level,
        include_resolved=False,
        verify_now=True,
    )
    attached = []
    generated_keys_added = []
    status = None
    reason = None

    if plan.get("status") != "tower":
        return {
            "status": plan.get("status"),
            "reason": plan.get("reason"),
            "plan": plan,
            "attached": [],
            "attached_count": 0,
            "undo_token": None,
            "start_attachment_history_length": start_history_length,
            "final_attachment_history_length": start_history_length,
        }

    for level in plan.get("levels", []):
        candidates = [
            item
            for item in level.get("candidates", [])
            if not item.get("resolved")
        ]

        if len(attached) + len(candidates) > max_cells:
            status = "budget_exceeded"
            reason = "max_cells would be exceeded"
            break

        if dry_run:
            status = "dry_run"
            reason = "dry run stopped before applying attachments"
            break

        for candidate in candidates:
            inputs = tuple(candidate.get("inputs", ()))

            if self.mp_key(*inputs) in getattr(self, "resolved_massey_products", {}):
                continue

            try:
                defined = self.can_define_mp(*inputs)
            except Exception:
                defined = False

            if not defined:
                status = "blocked"
                reason = "tower candidate is not definable by current certificates at this level"
                candidate = dict(candidate)
                candidate["defined_now"] = False
                attached.append({
                    "failed_candidate": candidate,
                })
                break

            M = self.virtual_mp(*inputs)

            if (
                verify_cycles
                and not _massey_formula_disabled(self)
                and not getattr(self, "_suppress_primitive_expansion", False)
                and not self.d(M.expand()).is_zero()
            ):
                status = "blocked"
                reason = "tower candidate expansion is not a cycle"
                candidate = dict(candidate)
                candidate["massey_product"] = M
                candidate["cycle_now"] = False
                attached.append({
                    "failed_candidate": candidate,
                })
                break

            before = len(getattr(self, "attachment_history", []))
            cell = self.attach_mp_cell(M)
            after = len(getattr(self, "attachment_history", []))

            if cell is None or after == before:
                status = "blocked"
                reason = "attachment failed or did not add a new cell"
                break

            generated_key = _cyclic_autocomplete_remember_generated(self, M)

            if generated_key is not None:
                generated_keys_added.append(generated_key)

            record = dict(candidate)
            record["massey_product"] = M
            record["cell"] = cell
            record["history_index"] = after - 1
            attached.append(record)

        if status is not None:
            break

    if status is None:
        status = "complete"
        reason = "tower attachments complete"

    final_history_length = len(getattr(self, "attachment_history", []))
    token = {
        "kind": "massey_orbit_tower_undo",
        "start_attachment_history_length": start_history_length,
        "final_attachment_history_length": final_history_length,
        "attached_count": len([
            item
            for item in attached
            if item.get("cell") is not None
        ]),
        "attached_cells": [
            item.get("cell")
            for item in attached
            if item.get("cell") is not None
        ],
        "generated_keys_added": list(generated_keys_added),
    }

    if token["attached_count"]:
        stack = getattr(self, "_massey_orbit_tower_undo_stack", None)

        if stack is None:
            stack = []
            self._massey_orbit_tower_undo_stack = stack

        stack.append(token)

    return {
        "status": status,
        "reason": reason,
        "plan": plan,
        "attached": attached,
        "attached_count": token["attached_count"],
        "undo_token": token if token["attached_count"] else None,
        "start_attachment_history_length": start_history_length,
        "final_attachment_history_length": final_history_length,
    }


def undo_massey_orbit_tower(
    self,
    token=None,
    force=False,
    verbose=True,
):
    """
    Undo one pointed Massey orbit tower run.
    """

    stack = getattr(self, "_massey_orbit_tower_undo_stack", [])

    if token is None:
        if not stack:
            return {
                "undone": False,
                "reason": "no Massey orbit tower undo token available",
            }

        token = stack[-1]

    start = token.get("start_attachment_history_length")
    final = token.get("final_attachment_history_length")
    current = len(getattr(self, "attachment_history", []))

    if current != final and not force:
        return {
            "undone": False,
            "reason": "attachment history changed after tower autocomplete; pass force=True to undo anyway",
            "current_attachment_history_length": current,
            "expected_attachment_history_length": final,
        }

    undone = []

    while len(getattr(self, "attachment_history", [])) > start:
        result = self.undo_latest_attachment(verbose=verbose)

        if result is None:
            break

        undone.append(result)

    removed_generated = _cyclic_autocomplete_forget_generated_keys(
        self,
        token.get("generated_keys_added", [])
    )

    if stack and token in stack:
        stack.remove(token)

    return {
        "undone": True,
        "undone_count": len(undone),
        "undo_results": undone,
        "removed_generated": removed_generated,
        "remaining_attachment_history_length": len(getattr(self, "attachment_history", [])),
    }


def _fast_missing_requirements_for_mp(self, inputs):
    inputs = tuple(self.normalize_mp_inputs(tuple(inputs)))
    primitive_keys, _primitive_records, _source_by_key = _fast_known_mp_primitive_records(self)
    tower_records = _fast_tower_records(self)
    missing = []

    for subkey in self.required_lower_mps(*inputs):
        if _fast_block_has_primitive_certificate(
            self,
            subkey,
            primitive_keys,
            tower_records=tower_records,
        ):
            continue

        missing.append(subkey)

    return missing


def cyclic_massey_rotation_report(
    self,
    M_or_inputs,
    require_direct_primitives=False,
    record=True,
):
    if isinstance(M_or_inputs, MasseyProduct):
        inputs = tuple(M_or_inputs.inputs)
    else:
        inputs = self.normalize_mp_inputs(tuple(M_or_inputs))

    rotations = self.cyclic_rotations(inputs)
    records = []

    for index, rotation in enumerate(rotations):
        if require_direct_primitives:
            defined = self.can_define_mp_direct(*rotation)
            M = self.get_or_create_mp_direct(*rotation) if defined and record else None
        else:
            defined = self.can_define_mp(*rotation)
            M = self.mp(*rotation) if defined and record else None

        key = self.mp_key(*rotation)
        primitive = getattr(self, "resolved_massey_products", {}).get(key, None)
        bridge_promoted_primitive = (
            primitive is not None
            and _is_bridge_promoted_massey_primitive_for_inputs(
                self,
                primitive,
                rotation,
            )
        )
        tower_resolution = None
        pair_tower_resolution = None
        equivalent_resolution = None

        if (
            defined
            and primitive is None
            and not require_direct_primitives
            and not getattr(self, "skip_deep_tower_resolution", False)
        ):
            try:
                tower_resolution = self.tower_elimination_report(*rotation)
            except Exception:
                tower_resolution = None

            if tower_resolution is None:
                try:
                    pair_tower_resolution = self.pair_tower_elimination_report(
                        *rotation,
                    )
                except Exception:
                    pair_tower_resolution = None

        tower_resolved = tower_resolution is not None
        pair_tower_resolved = pair_tower_resolution is not None
        virtual_tower_resolved = tower_resolved or pair_tower_resolved

        if (
            primitive is None
            and not virtual_tower_resolved
            and not require_direct_primitives
            and not getattr(self, "skip_deep_tower_resolution", False)
        ):
            try:
                equivalent_resolution = self.mp_presentation_equivalent_primitive_report(
                    rotation,
                    include_self=False,
                )
            except Exception:
                equivalent_resolution = None

        equivalent_resolved = equivalent_resolution is not None

        if equivalent_resolved:
            defined = True

        records.append({
            "index": index,
            "inputs": rotation,
            "defined": defined,
            "massey_product": M,
            "resolved": primitive is not None or virtual_tower_resolved or equivalent_resolved,
            "primitive": primitive,
            "bridge_promoted_primitive": bridge_promoted_primitive,
            "independent_primitive": (
                primitive is not None and not bridge_promoted_primitive
            ),
            "tower_resolved": tower_resolved,
            "tower_resolution": tower_resolution,
            "pair_tower_resolved": pair_tower_resolved,
            "pair_tower_resolution": pair_tower_resolution,
            "virtual_tower_resolved": virtual_tower_resolved,
            "equivalent_resolved": equivalent_resolved,
            "equivalent_resolution": equivalent_resolution,
            "missing_requirements": (
                []
                if defined
                else (
                    _fast_missing_requirements_for_mp(self, rotation)
                    if require_direct_primitives
                    else self.missing_requirements_for_mp(*rotation)
                )
            ),
        })

    return records


def _pure_massey_bridge_resolution_report(
    self,
    M,
    max_depth=None,
):
    if not isinstance(M, MasseyProduct):
        return None

    if max_depth is None:
        max_depth = _bridge_replacement_depth_limit(self)

    if max_depth is None:
        max_depth = 3

    try:
        max_depth = max(1, int(max_depth))
    except (TypeError, ValueError):
        max_depth = 3

    try:
        relations = self.product_replacement_relations()
    except Exception:
        return None

    start = (M,)
    queue = [(start, 0, [start], False)]
    seen = {self.cyclic_factor_tuple_key(start)}

    while queue:
        word, depth, path, has_non_ainf_step = queue.pop(0)

        if depth > 0 and has_non_ainf_step:
            try:
                cyclic = self.mp_factors_composable(word, cyclic=True)
            except Exception:
                cyclic = False

            if not cyclic:
                return {
                    "resolved": True,
                    "source": "bridge_replacement",
                    "resolved_word": word,
                    "path": path,
                    "cyclically_zero": True,
                    "cyclically_zero_reason": "non_loop_replacement",
                }

            try:
                product_resolution = self.product_cyclic_class_is_bridge_resolved(
                    word,
                    relations=relations,
                )
            except Exception:
                product_resolution = None

            if product_resolution and product_resolution.get("resolved"):
                return {
                    "resolved": True,
                    "source": "bridge_replacement",
                    "resolved_word": word,
                    "path": path,
                    "product_resolution": product_resolution,
                }

            if len(word) == 1 and isinstance(word[0], MasseyProduct):
                key = self.mp_key(*tuple(word[0].inputs))
                primitive = getattr(self, "resolved_massey_products", {}).get(key, None)

                if primitive is not None:
                    return {
                        "resolved": True,
                        "source": "bridge_replacement",
                        "resolved_word": word,
                        "path": path,
                        "primitive": primitive,
                    }

        if depth >= max_depth:
            continue

        try:
            neighbors = []
            n = len(word)

            for relation in tuple(relations or ()):
                directions = (
                    (("left", "right"),)
                    if relation.get("directed")
                    else (("left", "right"), ("right", "left"))
                )

                for source_name, target_name in directions:
                    source = tuple(relation.get(source_name, ()) or ())
                    target = tuple(relation.get(target_name, ()) or ())
                    source_len = len(source)

                    if source_len == 0 or source_len > n:
                        continue

                    for start_index in range(0, n - source_len + 1):
                        if not self.mp_factors_equal(
                            word[start_index:start_index + source_len],
                            source,
                        ):
                            continue

                        neighbor = (
                            word[:start_index]
                            + target
                            + word[start_index + source_len:]
                        )

                        if neighbor and not self.mp_factors_composable(
                            neighbor,
                            cyclic=False,
                        ):
                            continue

                        neighbors.append((
                            neighbor,
                            not _replacement_relation_is_ainf_equivalence(
                                relation
                            ),
                        ))
        except Exception:
            neighbors = []

        for neighbor, step_is_non_ainf in neighbors:
            key = self.cyclic_factor_tuple_key(neighbor)

            if key in seen:
                continue

            seen.add(key)
            queue.append((
                neighbor,
                depth + 1,
                path + [neighbor],
                has_non_ainf_step or step_is_non_ainf,
            ))

    return None


def _pure_massey_product_bridge_resolution_report(self, inputs):
    try:
        factors = tuple(
            item if isinstance(item, MasseyProduct) else self.mp(item)
            for item in tuple(inputs)
        )
        report = self.cyclic_product_class_report(factors, verify=False)
    except Exception:
        return None

    if not report.get("resolved") or report.get("likely_over"):
        return None

    sources = tuple(report.get("minimal_resolution_sources", ()))

    if not sources:
        return None

    if not all(source.get("source") == "bridge_replacement" for source in sources):
        return None

    return {
        "resolved": True,
        "source": "bridge_replacement_product_presentation",
        "product_report": report,
    }


def pure_massey_cyclic_class_report(
    self,
    M_or_inputs,
    require_direct_primitives=False,
    record=True,
    search_bridge_resolvers=None,
):
    explicit_search_bridge_resolvers = search_bridge_resolvers

    if isinstance(M_or_inputs, MasseyProduct):
        inputs = tuple(M_or_inputs.inputs)
        M = M_or_inputs
    else:
        inputs = self.normalize_mp_inputs(tuple(M_or_inputs))

        if record:
            M = (
                self.get_or_create_mp_direct(*inputs)
                if require_direct_primitives
                else self.mp(*inputs)
            )
        else:
            key = self.mp_key(*inputs)
            M = getattr(self, "massey_products", {}).get(key, None)

            if M is None:
                try:
                    defined = (
                        self.can_define_mp_direct(*inputs)
                        if require_direct_primitives
                        else self.can_define_mp(*inputs)
                    )
                except Exception:
                    defined = False

                if defined:
                    M = MasseyProduct(self, key)

    if len(inputs) < 3:
        return {
            "kind": "pure_massey_cyclic_class",
            "inputs": inputs,
            "is_genuine": False,
            "reason": "pure Massey cyclic classes require arity at least 3",
        }

    rotations = self.cyclic_massey_rotation_report(
        inputs,
        require_direct_primitives=require_direct_primitives,
        record=record,
    )
    cyclically_zero = (
        getattr(M, "source", None) != getattr(M, "target", None)
    )

    if cyclically_zero:
        return {
            "kind": "pure_massey_cyclic_class",
            "inputs": inputs,
            "massey_product": M,
            "is_genuine": True,
            "arity": len(inputs),
            "require_direct_primitives": require_direct_primitives,
            "complete_compatible_orbit": False,
            "rotations": rotations,
            "resolved": True,
            "directly_resolved": False,
            "bridge_resolved": False,
            "preferred_resolved_by_other_rotations": False,
            "cyclically_zero": True,
            "cyclically_zero_reason": "non_loop_massey_product",
            "likely_over": False,
        }

    directly_resolved = (
        bool(rotations[0].get("independent_primitive", False))
        if rotations
        else False
    )
    complete_compatible_orbit = all(
        rotation["defined"]
        for rotation in rotations
    )
    other_rotations_resolved = all(
        rotation["resolved"]
        for rotation in rotations[1:]
    )
    preferred_resolved_without_bridge = (
        complete_compatible_orbit
        and other_rotations_resolved
    )
    bridge_resolution = None

    if search_bridge_resolvers is None:
        search_bridge_resolvers = bool(
            getattr(self, "search_pure_bridge_resolvers", False)
        )

    if (
        search_bridge_resolvers
        and not (rotations[0]["resolved"] if rotations else False)
        and not preferred_resolved_without_bridge
    ):
        bridge_resolution = _pure_massey_bridge_resolution_report(self, M)

    if bridge_resolution is not None:
        rotations = list(rotations)

        if rotations:
            rotations[0] = dict(rotations[0])
            rotations[0]["resolved"] = True
            rotations[0]["bridge_resolved"] = True
            rotations[0]["bridge_resolution"] = bridge_resolution

    product_bridge_resolution = None

    if (
        bridge_resolution is None
        and not require_direct_primitives
        and not (rotations[0]["resolved"] if rotations else False)
        and explicit_search_bridge_resolvers is not False
    ):
        product_bridge_resolution = _pure_massey_product_bridge_resolution_report(
            self,
            inputs,
        )

    if product_bridge_resolution is not None:
        rotations = list(rotations)

        if rotations:
            rotations[0] = dict(rotations[0])
            rotations[0]["resolved"] = True
            rotations[0]["product_bridge_resolved"] = True
            rotations[0]["product_bridge_resolution"] = product_bridge_resolution

    self_resolution_is_bridge_promoted_only = (
        bool(rotations)
        and bool(rotations[0].get("bridge_promoted_primitive", False))
        and not bool(rotations[0].get("independent_primitive", False))
        and not bool(rotations[0].get("tower_resolved", False))
        and not bool(rotations[0].get("pair_tower_resolved", False))
        and not bool(rotations[0].get("equivalent_resolved", False))
    )
    self_resolved = (
        bool(rotations[0]["resolved"])
        and not self_resolution_is_bridge_promoted_only
        if rotations
        else False
    )
    self_resolution_is_virtual_tower_only = (
        bool(rotations)
        and bool(rotations[0].get("virtual_tower_resolved", False))
        and rotations[0].get("primitive") is None
        and not bool(rotations[0].get("equivalent_resolved", False))
    )
    other_rotations_resolved = all(
        rotation["resolved"]
        for rotation in rotations[1:]
    )

    if complete_compatible_orbit:
        preferred_resolved = other_rotations_resolved
        cyclic_class_resolved = self_resolved or preferred_resolved
        preferred_independently_resolved = all(
            bool(rotation.get("independent_primitive", False))
            for rotation in rotations[1:]
        )
        likely_over = directly_resolved and preferred_independently_resolved
    else:
        preferred_resolved = False
        preferred_independently_resolved = False
        cyclic_class_resolved = (
            self_resolved
            and not self_resolution_is_virtual_tower_only
        )
        likely_over = False

    return {
        "kind": "pure_massey_cyclic_class",
        "inputs": inputs,
        "massey_product": M,
        "is_genuine": True,
        "arity": len(inputs),
        "require_direct_primitives": require_direct_primitives,
        "complete_compatible_orbit": complete_compatible_orbit,
        "rotations": rotations,
        "resolved": cyclic_class_resolved,
        "directly_resolved": directly_resolved,
        "tower_resolved": bool(
            rotations and rotations[0].get("tower_resolved", False)
        ),
        "pair_tower_resolved": bool(
            rotations and rotations[0].get("pair_tower_resolved", False)
        ),
        "virtual_tower_resolved": bool(
            rotations and rotations[0].get("virtual_tower_resolved", False)
        ),
        "bridge_resolved": bool(bridge_resolution),
        "bridge_resolution": bridge_resolution,
        "product_bridge_resolved": bool(product_bridge_resolution),
        "product_bridge_resolution": product_bridge_resolution,
        "self_resolution_is_bridge_promoted_only": (
            self_resolution_is_bridge_promoted_only
        ),
        "preferred_resolved_by_other_rotations": preferred_resolved,
        "preferred_independently_resolved_by_other_rotations": (
            preferred_independently_resolved
        ),
        "likely_over": likely_over,
    }
