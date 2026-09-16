"""Local web game for monomial proper finite-cell DG algebras.

This is the monomial ruleset of the A-infinity game.  It deliberately shares
the proven quiver/search engine with ``program-A-inf`` while giving the ruleset
its own launcher, UI, save directory, and validation boundary.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
LEGACY_ROOT = ROOT.parent / "program-A-inf"
STATIC_DIR = ROOT / "web"


def default_saved_games_dir() -> Path:
    """Return a writable save location in source and packaged builds."""

    if getattr(sys, "frozen", False):
        if sys.platform == "win32":
            application_support = Path(
                os.environ.get(
                    "LOCALAPPDATA",
                    Path.home() / "AppData" / "Local",
                )
            )
        elif sys.platform == "darwin":
            application_support = Path.home() / "Library" / "Application Support"
        else:
            application_support = Path(
                os.environ.get(
                    "XDG_DATA_HOME",
                    Path.home() / ".local" / "share",
                )
            )
        return application_support / "Monomial Finite Cell Game" / "saved games"

    return ROOT / "saved games"


SAVED_GAMES_DIR = default_saved_games_dir()

if str(LEGACY_ROOT) not in sys.path:
    sys.path.insert(0, str(LEGACY_ROOT))

import ainf_game_ui as legacy  # noqa: E402
from monomial_extensions import install_monomial_extensions  # noqa: E402
from monomial_kernel import (  # noqa: E402
    analyze_monomial_actions,
    compute_victory_invariants,
)


SAVE_SCHEMA = "monomial-finite-cell-game-save"
LOCKED_MONOMIAL_SETTINGS: dict[str, Any] = {
    "includePrimitiveDetails": False,
    "fastMasseyGeneration": True,
    "bridgeReplacementMaxDepth": 0,
    "ainfReplacementMaxOuterArity": "infinity",
    "maxPureArity": 8,
    "filterSelfExpandingReplacements": True,
    "skipSusceptibleSearch": True,
    "generateAfterResolve": True,
    "detectRedundantGenerators": False,
    "searchPureBridgeResolvers": False,
    "disableMasseyFormula": True,
}


class MonomialGameEngine(legacy.GameEngine):
    """A bridge-free, formula-free specialization of the original game."""

    def __init__(self) -> None:
        super().__init__()
        install_monomial_extensions(self.Quiver)
        self.computation_settings.update(LOCKED_MONOMIAL_SETTINGS)
        self._configure_monomial_quiver()
        self.messages = [
            "Ready: attach cells along monomials and generate compatible Massey products."
        ]

    def _configure_monomial_quiver(self) -> None:
        # A Massey input tuple has one canonical object in the quiver registry.
        # In this ruleset those objects are, by definition, representatives in
        # one compatible defining system; no cochain formulas are materialized.
        self.Q.monomial_finite_cell_mode = True
        self.Q.compatible_massey_system = True
        self.Q.disable_massey_formula = True
        self.Q._disable_massey_formula = True

        # Lemma 1: completed compatible pair towers also certify their
        # admissible collapsed monomial blocks.
        self.Q.enable_lemma1_collapsed_product_blocks = True

    def _normalize_computation_settings(
        self,
        data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        settings = super()._normalize_computation_settings(data)
        settings.update(LOCKED_MONOMIAL_SETTINGS)
        return settings

    def reset(self) -> dict[str, Any]:
        super().reset()
        self.computation_settings.update(LOCKED_MONOMIAL_SETTINGS)
        self._configure_monomial_quiver()
        self.messages = ["Started a new monomial finite-cell game."]
        return self.state()

    def _apply_action(
        self,
        action: dict[str, Any],
        replay: bool = False,
    ) -> list[str]:
        self._configure_monomial_quiver()

        if action.get("kind") == "attach_bridge":
            raise legacy.GameError(
                "Bridge cells are not part of the monomial finite-cell game. "
                "Resolve one monomial differential instead."
            )

        return super()._apply_action(action, replay=replay)

    def attach_bridge(self, data: dict[str, Any]) -> dict[str, Any]:
        raise legacy.GameError(
            "Bridge cells are not part of the monomial finite-cell game. "
            "Resolve one monomial differential instead."
        )

    def import_save(self, data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise legacy.GameError("Save file must contain a JSON object.")

        schema = data.get("schema")

        if schema not in {SAVE_SCHEMA, "ainf-game-save"}:
            raise legacy.GameError(
                "This does not look like a monomial finite-cell game save file."
            )

        actions = data.get("actions")

        if not isinstance(actions, list):
            raise legacy.GameError("Save file is missing its action log.")

        if any(
            isinstance(action, dict) and action.get("kind") == "attach_bridge"
            for action in actions
        ):
            raise legacy.GameError(
                "This save contains a bridge cell and cannot be loaded in monomial mode."
            )

        compatible_data = json.loads(json.dumps(data))
        compatible_data["schema"] = "ainf-game-save"
        super().import_save(compatible_data)
        self.computation_settings.update(LOCKED_MONOMIAL_SETTINGS)
        self._configure_monomial_quiver()
        self.messages = [
            f"Loaded monomial game with {len(self.actions)} move(s)."
        ]
        return self.state()

    def export_save(self) -> dict[str, Any]:
        data = super().export_save()
        data.update({
            "schema": SAVE_SCHEMA,
            "game": "monomial-finite-cell",
            "rules": {
                "monomialDifferentials": True,
                "bridges": False,
                "higherProductsAreMassey": True,
                "compatibleMasseySystem": True,
                "explicitHigherProductFormulas": False,
                "ainfReplacements": True,
                "lemma1": True,
            },
        })
        return data

    def _exact_pair_poset_report(self, analysis: dict[str, Any]) -> None:
        kind = analysis.get("kind")
        proper = analysis.get("proper")

        if kind == "incomplete_pair_poset":
            missing = list(analysis.get("missingCells") or [])
            missing_words = list(analysis.get("missingCellWords") or [])
            first = missing[0] if missing else "a descent cell"
            summary = {
                "status": "not_yet",
                "headline": f"Not yet victorious: attach the missing descent cell {first}.",
                "nextKind": "missing_descent_cell",
                "productPartWon": False,
                "productFirstLength": (
                    len(missing_words[0]) if missing_words else None
                ),
                "pureUnresolvedCount": 0,
                "productCycleCount": 0,
                "redundantGeneratorCount": 0,
                "likelyOverCount": 0,
                "notLikelyReason": None,
            }
            detail = (
                f"Exact pair-poset check found {len(missing)} missing descent "
                f"cell(s): {', '.join(missing[:8])}."
            )
        elif proper:
            dimension = analysis.get("cohomologyDimension")
            max_length = analysis.get("maxSupportedLength")
            summary = {
                "status": "win",
                "headline": (
                    "Victory! The exact support automaton is acyclic "
                    f"(dim H* = {dimension}, maximum support length {max_length})."
                ),
                "nextKind": None,
                "productPartWon": True,
                "productFirstLength": None,
                "pureUnresolvedCount": 0,
                "productCycleCount": 0,
                "redundantGeneratorCount": 0,
                "likelyOverCount": 0,
                "notLikelyReason": None,
            }
            detail = (
                "Exact pair-poset certificate: the reachable and coaccessible "
                "support automaton is acyclic."
            )
        else:
            witness = analysis.get("supportedWordWitness") or "an accepted word"
            repeatable = analysis.get("repeatableBlock") or "a productive cycle"
            summary = {
                "status": "lose",
                "headline": (
                    "Not proper: the exact support automaton contains a "
                    f"productive cycle ({repeatable})."
                ),
                "nextKind": "support_cycle",
                "productPartWon": False,
                "productFirstLength": analysis.get("supportedWordWitnessLength"),
                "pureUnresolvedCount": 0,
                "productCycleCount": 1,
                "redundantGeneratorCount": 0,
                "likelyOverCount": 0,
                "notLikelyReason": "the exact support language is infinite.",
            }
            detail = f"Supported-word witness: {witness}."

        report = {
            "won": bool(proper),
            "product_part_won": bool(proper),
            "next_kind": summary["nextKind"],
            "product_result": {
                "won": bool(proper),
                "first_unresolved_length": summary["productFirstLength"],
                "searched_max_length": analysis.get("maxSupportedLength"),
                "search_incomplete": False,
                "terminating_unresolved_classes": [],
                "deferred_unresolved_classes": [],
                "likely_over_classes": [],
            },
            "pure_generated_result": {
                "won": bool(proper),
                "unresolved_classes": [],
                "likely_over_classes": [],
            },
            "generated_product_cycle_result": {
                "unresolved_classes": [],
                "likely_over_classes": [],
            },
            "generator_redundancy_result": {"redundant_generators": []},
            "pure_search_result": None,
            "monomial_kernel": analysis,
        }
        self.last_run = {
            "summary": summary,
            "report": report,
            "monomial_kernel": analysis,
        }
        self.messages = [detail, summary["headline"]]

    def _run_stage_report(self) -> None:
        analysis = analyze_monomial_actions(self.actions)

        if analysis.get("kind") in {"pair_poset", "incomplete_pair_poset"}:
            self._exact_pair_poset_report(analysis)
            return

        super()._run_stage_report()
        if self.last_run is not None:
            self.last_run["monomial_kernel"] = analysis

    def _serialize_last_run(self) -> dict[str, Any] | None:
        data = super()._serialize_last_run()

        if data is None or not self.last_run:
            return data

        analysis = self.last_run.get("monomial_kernel")
        if analysis:
            data["monomialKernel"] = analysis

        return data

    def _serialize_resolved_products(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        seen: set[str] = set()

        for entry in self.Q.known_resolved_product_blocks():
            factors = tuple(entry.get("factors", ()))

            if len(factors) < 2:
                continue

            spec = {
                "type": "product",
                "coefficient": "1",
                "factors": [self._factor_spec(factor) for factor in factors],
            }
            key = json.dumps(spec, sort_keys=True)

            if key in seen:
                continue

            seen.add(key)
            resolution = entry.get("resolution") or {}
            rows.append({
                "spec": spec,
                "factorCount": len(factors),
                "source": entry.get("source") or resolution.get("source") or "",
                "reason": resolution.get("reason") or "",
            })

        return rows

    def _computed_victory_invariants(self) -> dict[str, Any]:
        if not self.last_run or self.last_run.get("summary", {}).get("status") != "win":
            raise legacy.GameError("Run the game to a verified victory first.")

        invariants = compute_victory_invariants(self.actions)

        if not invariants.get("available"):
            raise legacy.GameError(
                str(invariants.get("reason") or "No exact finite basis is available.")
            )

        return invariants

    def cohomology_basis(self) -> dict[str, Any]:
        with self.lock:
            invariants = self._computed_victory_invariants()
            dimension = int(invariants["dimension"])
            self.messages = [
                f"Computed a finite cohomology basis with {dimension} classes."
            ]
            return {
                "cohomologyBasis": {
                    "available": True,
                    "victory": True,
                    "finite": True,
                    "dimension": dimension,
                    "vertices": invariants["vertices"],
                    "basis": invariants["basis"],
                    "gradingConvention": invariants["gradingConvention"],
                },
                "state": self.state(),
            }

    def cartan_invariants(self) -> dict[str, Any]:
        with self.lock:
            invariants = self._computed_victory_invariants()
            ordinary = invariants["ordinaryCartan"]["determinant"]
            cellular = invariants["cellularCartan"]["determinant"]
            self.messages = [
                "Computed Cartan determinants: "
                f"ordinary {ordinary}, cellular {cellular}."
            ]
            return {
                "cartanInvariants": {
                    "available": True,
                    "victory": True,
                    "finite": True,
                    "vertices": invariants["vertices"],
                    "ordinaryCartan": invariants["ordinaryCartan"],
                    "cellularCartan": invariants["cellularCartan"],
                    "gradingConvention": invariants["gradingConvention"],
                },
                "state": self.state(),
            }

    def state(self) -> dict[str, Any]:
        self._configure_monomial_quiver()
        data = super().state()

        if data.get("busy"):
            return data

        data["bridgeProducts"] = []
        data["resolvedProducts"] = self._serialize_resolved_products()
        data["game"] = {
            "name": "Monomial finite-cell game",
            "mode": "monomial-finite-cell",
            "rules": {
                "monomialDifferentials": True,
                "bridges": False,
                "higherProductsAreMassey": True,
                "compatibleMasseySystem": True,
                "explicitHigherProductFormulas": False,
                "ainfReplacements": True,
                "lemma1": True,
            },
        }
        return data


class MonomialRequestHandler(legacy.UIRequestHandler):
    server_version = "MonomialFiniteCellGame/1.0"

    def _dispatch_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if path == "/api/attach-bridge":
            raise FileNotFoundError("Bridge operations do not exist in monomial mode.")

        if path == "/api/cohomology-basis":
            return legacy.ENGINE.cohomology_basis()

        if path == "/api/cartan-invariants":
            return legacy.ENGINE.cartan_invariants()

        return super()._dispatch_post(path, payload)


def default_save_file_name() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"monomial-finite-cell-{stamp}.json"


legacy.STATIC_DIR = STATIC_DIR
legacy.SAVED_QUIVERS_DIR = SAVED_GAMES_DIR
legacy.default_save_file_name = default_save_file_name
legacy.ENGINE = MonomialGameEngine()


def create_server(
    host: str = "127.0.0.1",
    preferred_port: int = 8600,
) -> ThreadingHTTPServer:
    """Create a game server, allowing port 0 for an OS-assigned private port."""

    port = 0 if preferred_port == 0 else legacy.find_port(preferred_port)
    return ThreadingHTTPServer((host, port), MonomialRequestHandler)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Serve the monomial proper finite-cell DG algebra game."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8600)
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    port = int(server.server_address[1])
    url = f"http://{args.host}:{port}"
    print(f"Monomial finite-cell game running at {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
