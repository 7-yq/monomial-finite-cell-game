from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

import pytest

import monomial_finite_cell_game as game_module
from monomial_finite_cell_game import MonomialGameEngine, SAVE_SCHEMA, create_server


LEGACY_SAVES = Path(__file__).resolve().parent.parent / "program-A-inf" / "saved quivers"


def arrow(name: str) -> dict[str, str]:
    return {"type": "arrow", "name": name}


def product(*names: str) -> dict:
    return {
        "type": "product",
        "coefficient": "1",
        "factors": [arrow(name) for name in names],
    }


def massey(*names: str) -> dict:
    return {
        "type": "massey",
        "inputs": [arrow(name) for name in names],
    }


@pytest.fixture
def engine() -> MonomialGameEngine:
    game = MonomialGameEngine()
    with contextlib.redirect_stdout(io.StringIO()):
        game.add_vertices("v")
        for name in ("x", "y", "z", "w"):
            game.add_arrow({
                "name": name,
                "source": "v",
                "target": "v",
                "grading": None,
            })
    return game


def test_packaged_server_can_request_an_ephemeral_port(monkeypatch) -> None:
    calls = []

    class FakeServer:
        def __init__(self, address, handler):
            calls.append((address, handler))

    monkeypatch.setattr(game_module, "ThreadingHTTPServer", FakeServer)
    server = create_server(preferred_port=0)

    assert isinstance(server, FakeServer)
    assert calls == [(("127.0.0.1", 0), game_module.MonomialRequestHandler)]


def test_windows_package_uses_local_app_data_for_saves(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(game_module.sys, "frozen", True, raising=False)
    monkeypatch.setattr(game_module.sys, "platform", "win32")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    assert game_module.default_saved_games_dir() == (
        tmp_path / "Monomial Finite Cell Game" / "saved games"
    )


def test_monomial_rules_are_locked_and_exported(engine: MonomialGameEngine) -> None:
    engine.update_settings({
        "includePrimitiveDetails": True,
        "bridgeReplacementMaxDepth": "legacy",
        "ainfReplacementMaxOuterArity": 2,
        "maxPureArity": 20,
        "filterSelfExpandingReplacements": False,
        "skipSusceptibleSearch": False,
        "generateAfterResolve": False,
        "detectRedundantGenerators": True,
        "searchPureBridgeResolvers": True,
        "disableMasseyFormula": False,
    })

    settings = engine.state()["computation"]["settings"]
    saved = engine.export_save()

    assert settings["includePrimitiveDetails"] is False
    assert settings["bridgeReplacementMaxDepth"] == 0
    assert settings["ainfReplacementMaxOuterArity"] == "infinity"
    assert settings["maxPureArity"] == 8
    assert settings["filterSelfExpandingReplacements"] is True
    assert settings["skipSusceptibleSearch"] is True
    assert settings["generateAfterResolve"] is True
    assert settings["detectRedundantGenerators"] is False
    assert settings["searchPureBridgeResolvers"] is False
    assert settings["disableMasseyFormula"] is True
    assert engine.Q.compatible_massey_system is True
    assert engine.Q.enable_lemma1_collapsed_product_blocks is True
    assert saved["schema"] == SAVE_SCHEMA
    assert saved["rules"]["ainfReplacements"] is True
    assert saved["rules"]["lemma1"] is True


def test_bridge_actions_are_rejected(engine: MonomialGameEngine) -> None:
    with pytest.raises(Exception, match="Bridge cells are not part"):
        engine.attach_bridge({"left": product("x"), "right": product("y")})

    bridged_save = engine.export_save()
    bridged_save["actions"].append({
        "kind": "attach_bridge",
        "left": product("x"),
        "right": product("y"),
    })

    with pytest.raises(Exception, match="contains a bridge cell"):
        engine.import_save(bridged_save)


def test_seed_monomials_generate_formula_free_massey_products(
    engine: MonomialGameEngine,
) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        engine.attach_mp_cell({"expression": product("x", "y")})
        state = engine.attach_mp_cell({"expression": product("y", "z")})

    triples = [
        item
        for item in state["generated"]["items"]
        if item["arity"] == 3 and item["shortLabel"] == "Q.mp(x,y,z)"
    ]

    assert triples
    assert triples[0]["spec"]["type"] == "mp"
    assert len(state["resolvedProducts"]) == 2
    assert all(item["factorCount"] == 2 for item in state["resolvedProducts"])
    assert engine.Q._disable_massey_formula is True


def test_singleton_massey_cell_is_not_a_resolved_product(
    engine: MonomialGameEngine,
) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        engine.attach_mp_cell({"expression": product("x", "y")})
        engine.attach_mp_cell({"expression": product("y", "z")})
        state = engine.attach_mp_cell({"expression": massey("x", "y", "z")})

    assert len(state["attachments"]) == 3
    assert len(state["resolvedProducts"]) == 2
    assert all(item["spec"]["type"] == "product" for item in state["resolvedProducts"])


def test_ainf_replacements_survive_without_bridges(engine: MonomialGameEngine) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        for left, right in (("x", "y"), ("y", "z"), ("z", "w")):
            engine.attach_mp_cell({"expression": product(left, right)})

        engine.attach_mp_cell({"expression": massey("x", "y", "z")})
        engine.attach_mp_cell({"expression": massey("y", "z", "w")})

    relations = engine.Q.product_replacement_relations(
        include_bridge=False,
        include_ainf=True,
    )
    formatted = {
        frozenset((
            engine.Q.format_mp_input_product(relation["left"]),
            engine.Q.format_mp_input_product(relation["right"]),
        ))
        for relation in relations
        if relation.get("replacement_type") == "ainf"
    }

    assert frozenset(("Q.mp(x,y,z)w", "xQ.mp(y,z,w)")) in formatted
    assert all(
        relation.get("formula_free") is True
        for relation in relations
        if relation.get("ainf_kind") == "compatible_massey_slide"
    )
    assert engine.state()["bridgeProducts"] == []


def test_reset_and_replay_keep_lemma1_enabled(engine: MonomialGameEngine) -> None:
    saved = engine.export_save()
    engine.reset()
    assert engine.Q.enable_lemma1_collapsed_product_blocks is True

    engine.import_save(saved)
    assert engine.Q.enable_lemma1_collapsed_product_blocks is True
    assert engine.Q.compatible_massey_system is True


def test_run_uses_exact_pair_poset_verdict_for_triangle() -> None:
    game = MonomialGameEngine()
    data = json.loads((LEGACY_SAVES / "triangle quiver.json").read_text())
    data["fastLoad"] = True

    with contextlib.redirect_stdout(io.StringIO()):
        game.import_save(data)
        state = game.run({})

    assert state["run"]["summary"]["status"] == "win"
    assert state["run"]["monomialKernel"]["exact"] is True
    assert state["run"]["monomialKernel"]["cohomologyDimension"] == 7
    assert state["run"]["product"]["likelyOver"] == []

    basis_payload = game.cohomology_basis()
    cartan_payload = game.cartan_invariants()

    assert basis_payload["cohomologyBasis"]["dimension"] == 7
    assert len(basis_payload["cohomologyBasis"]["basis"]) == 7
    assert cartan_payload["cartanInvariants"]["ordinaryCartan"]["determinant"] == 1
    assert cartan_payload["cartanInvariants"]["cellularCartan"]["determinant"] == 1


def test_run_refuses_false_victory_for_incomplete_g5() -> None:
    game = MonomialGameEngine()
    data = json.loads((LEGACY_SAVES / "G5 Green algebra incomplete.json").read_text())
    data["fastLoad"] = True

    with contextlib.redirect_stdout(io.StringIO()):
        game.import_save(data)
        state = game.run({})

    assert state["run"]["summary"]["status"] == "not_yet"
    assert state["run"]["summary"]["productFirstLength"] == 5
    assert state["run"]["monomialKernel"]["kind"] == "incomplete_pair_poset"
    assert state["run"]["monomialKernel"]["missingCells"] == ["x1x2x3x4x5"]
