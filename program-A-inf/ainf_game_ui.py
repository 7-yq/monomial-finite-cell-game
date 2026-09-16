"""Local web UI for the A_infinity quiver game.

The algebra still lives in A_inf.ipynb and cyclic_extensions.py.  This module
loads those notebook definitions, wraps them in structured game operations, and
serves a small dependency-free browser UI.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import io
import json
import math
import os
import re
import socket
import sys
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock, RLock, Timer, get_ident
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
NOTEBOOK_PATH = ROOT / "A_inf.ipynb"
STATIC_DIR = ROOT / "web"
SAVED_QUIVERS_DIR = ROOT / "saved quivers"


class GameError(Exception):
    """A user-facing game operation error."""


def load_notebook_namespace(notebook_path: Path = NOTEBOOK_PATH) -> dict[str, Any]:
    """Load the definition cells from the notebook without running examples."""

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    notebook = json.loads(notebook_path.read_text())
    namespace: dict[str, Any] = {
        "__name__": "ainf_notebook_runtime",
        "__file__": str(notebook_path),
    }

    for index in range(3, 26):
        source = "".join(notebook["cells"][index]["source"])
        exec(source, namespace)

    return namespace


def capture_output(fn, *args, **kwargs):
    """Call fn while collecting notebook-style print output."""

    stream = io.StringIO()

    with contextlib.redirect_stdout(stream):
        result = fn(*args, **kwargs)

    output = [
        line
        for line in stream.getvalue().splitlines()
        if line.strip()
    ]
    return result, output


def visible_computation_output(lines: list[str] | tuple[str, ...] | None) -> list[str]:
    hidden_prefixes = (
        "Warning: cannot expand",
        "Warning: no primitive recorded",
        "Missing primitive in split",
    )

    return [
        line
        for line in (lines or [])
        if not any(line.startswith(prefix) for prefix in hidden_prefixes)
    ]


class OperationCancelled(BaseException):
    """Raised inside a worker thread when the user presses Stop."""


def raise_in_thread(thread_id: int, exception_type: type[BaseException]) -> int:
    result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(thread_id),
        ctypes.py_object(exception_type),
    )

    if result > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_id), None)
        raise RuntimeError("Stop request affected more than one Python thread.")

    return int(result)


class CancellationManager:
    def __init__(self) -> None:
        self._lock = Lock()
        self._thread_id: int | None = None
        self._label: str | None = None
        self._stop_requested = False

    @contextlib.contextmanager
    def operation(self, label: str):
        thread_id = get_ident()
        registered = False

        with self._lock:
            if self._thread_id is None:
                self._thread_id = thread_id
                self._label = label
                self._stop_requested = False
                registered = True

        try:
            yield
        finally:
            if registered:
                with self._lock:
                    if self._thread_id == thread_id:
                        self._thread_id = None
                        self._label = None
                        self._stop_requested = False

    def request_stop(self) -> dict[str, Any]:
        with self._lock:
            if self._thread_id is None:
                return {
                    "running": False,
                    "stopping": False,
                    "label": None,
                    "message": "No long computation is running.",
                }

            thread_id = self._thread_id
            label = self._label
            self._stop_requested = True
            result = raise_in_thread(thread_id, OperationCancelled)

        if result == 0:
            return {
                "running": False,
                "stopping": False,
                "label": label,
                "message": "The computation finished before the stop request arrived.",
            }

        return {
            "running": True,
            "stopping": True,
            "label": label,
            "message": f"Stopping {label or 'current computation'}.",
        }

    def request_force_stop(self) -> dict[str, Any]:
        soft_result = self.request_stop()

        def exit_process():
            os._exit(130)

        timer = Timer(0.35, exit_process)
        timer.daemon = True
        timer.start()

        return {
            **soft_result,
            "running": True,
            "stopping": True,
            "force": True,
            "message": (
                "Force-stopping the local server process. "
                "Restart the server after this page disconnects."
            ),
        }

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "running": self._thread_id is not None,
                "stopping": self._stop_requested,
                "label": self._label,
            }


def clean_name(value: Any, label: str) -> str:
    name = str(value or "").strip()

    if not name:
        raise GameError(f"{label} is required.")

    return name


def parse_optional_int(value: Any) -> int | None:
    if value is None or str(value).strip() == "":
        return None

    try:
        return int(str(value).strip())
    except ValueError as exc:
        raise GameError("Grading must be an integer when provided.") from exc


def clean_quiver_name(value: Any) -> str:
    text = str(value or "").strip()
    return " ".join(text.split())


def quiver_file_name_from_name(name: str) -> str:
    stem = clean_quiver_name(name)
    safe = []

    for char in stem:
        if char.isalnum() or char in {" ", "-", "_", ".", "(", ")"}:
            safe.append(char)
        else:
            safe.append("-")

    file_stem = "".join(safe).strip(" .-_") or "untitled-quiver"
    return f"{file_stem[:120]}.json"


def clean_quiver_file_name(value: Any) -> str:
    text = str(value or "").strip()

    if not text:
        return ""

    name = Path(text).name.strip()

    if not name:
        return ""

    if not name.lower().endswith(".json"):
        name = f"{name}.json"

    return name


def saved_quiver_path(file_name: str) -> Path:
    clean_name = clean_quiver_file_name(file_name)

    if not clean_name:
        raise GameError("Save file name is empty.")

    path = (SAVED_QUIVERS_DIR / clean_name).resolve()
    root = SAVED_QUIVERS_DIR.resolve()

    if not path.is_relative_to(root):
        raise GameError("Save file name must stay inside the saved quivers folder.")

    return path


def default_save_file_name() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"ainf-quiver-{stamp}.json"


DEFAULT_COMPUTATION_SETTINGS: dict[str, Any] = {
    "includePrimitiveDetails": False,
    "fastMasseyGeneration": True,
    "bridgeReplacementMaxDepth": "legacy",
    "ainfReplacementMaxOuterArity": 3,
    "maxPureArity": 8,
    "filterSelfExpandingReplacements": True,
    "skipSusceptibleSearch": True,
    "generateAfterResolve": False,
    "detectRedundantGenerators": False,
    "searchPureBridgeResolvers": False,
    "disableMasseyFormula": False,
}
COMPUTATION_SETTING_KEYS = set(DEFAULT_COMPUTATION_SETTINGS)


def empty_pure_classes_payload(dirty: bool = False) -> dict[str, Any]:
    return {
        "won": True,
        "sourceCount": 0,
        "classes": [],
        "unresolved": [],
        "likelyOver": [],
        "dirty": dirty,
    }


class GameEngine:
    """Stateful wrapper around one Quiver and a replayable operation log."""

    def __init__(self) -> None:
        self.namespace = load_notebook_namespace()
        self.Quiver = self.namespace["Quiver"]
        self.Arrow = self.namespace["Arrow"]
        self.Path = self.namespace["Path"]
        self.Element = self.namespace["Element"]
        self.MasseyProduct = self.namespace["MasseyProduct"]
        self.MPProduct = self.namespace["MPProduct"]
        self.MPElement = self.namespace["MPElement"]
        self.actions: list[dict[str, Any]] = []
        self.messages: list[str] = []
        self.last_generation: dict[str, Any] | None = None
        self.last_pure_classes: dict[str, Any] = empty_pure_classes_payload()
        self.last_run: dict[str, Any] | None = None
        self.last_autocomplete_plan: dict[str, Any] | None = None
        self.computation_settings: dict[str, Any] = dict(DEFAULT_COMPUTATION_SETTINGS)
        self.quiver_name = ""
        self.quiver_file_name = ""
        self.generator_order: list[str] = []
        self.generator_order_custom = False
        self.lock = RLock()
        self.Q = self.Quiver()

    def reset(self) -> dict[str, Any]:
        with self.lock:
            self.Q = self.Quiver()
            self.actions = []
            self.messages = ["Started a new game."]
            self.last_generation = None
            self.last_pure_classes = empty_pure_classes_payload()
            self.last_run = None
            self.last_autocomplete_plan = None
            self.quiver_name = ""
            self.quiver_file_name = ""
            self.generator_order = []
            self.generator_order_custom = False
            return self.state()

    def _setting_payload(self, data: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(data, dict):
            return {}

        payload: dict[str, Any] = {}

        for container_key in ("settings", "computationSettings"):
            nested = data.get(container_key)

            if isinstance(nested, dict):
                payload.update(nested)

        for key in COMPUTATION_SETTING_KEYS:
            if key in data:
                payload[key] = data[key]

        return payload

    def _coerce_bool_setting(self, value: Any, fallback: bool) -> bool:
        if value is None:
            return fallback

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in {"1", "true", "yes", "on"}:
                return True

            if normalized in {"0", "false", "no", "off"}:
                return False

            return fallback

        return bool(value)

    def _coerce_bridge_depth_setting(self, value: Any) -> int | str:
        if value is None:
            return DEFAULT_COMPUTATION_SETTINGS["bridgeReplacementMaxDepth"]

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in {"legacy", "full", "unbounded", "none"}:
                return "legacy"

            if normalized in {"off", "disabled", "false"}:
                return 0

            if not normalized:
                return DEFAULT_COMPUTATION_SETTINGS["bridgeReplacementMaxDepth"]

            value = normalized

        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return DEFAULT_COMPUTATION_SETTINGS["bridgeReplacementMaxDepth"]

    def _coerce_max_pure_arity_setting(self, value: Any) -> int:
        if value is None:
            return int(DEFAULT_COMPUTATION_SETTINGS["maxPureArity"])

        try:
            return max(3, int(value))
        except (TypeError, ValueError):
            return int(DEFAULT_COMPUTATION_SETTINGS["maxPureArity"])

    def _coerce_ainf_outer_arity_setting(self, value: Any) -> int | str:
        if value is None:
            return DEFAULT_COMPUTATION_SETTINGS["ainfReplacementMaxOuterArity"]

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in {"infinity", "inf", "unbounded", "legacy", "full"}:
                return "infinity"

            if normalized in {"off", "disabled", "false"}:
                return 0

            if not normalized:
                return DEFAULT_COMPUTATION_SETTINGS["ainfReplacementMaxOuterArity"]

            value = normalized

        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return DEFAULT_COMPUTATION_SETTINGS["ainfReplacementMaxOuterArity"]

    def _normalize_computation_settings(self, data: dict[str, Any] | None) -> dict[str, Any]:
        settings = dict(DEFAULT_COMPUTATION_SETTINGS)
        settings.update(self.computation_settings)
        payload = self._setting_payload(data)

        if not payload:
            return settings

        for key in (
            "includePrimitiveDetails",
            "fastMasseyGeneration",
            "filterSelfExpandingReplacements",
            "skipSusceptibleSearch",
            "generateAfterResolve",
            "detectRedundantGenerators",
            "searchPureBridgeResolvers",
            "disableMasseyFormula",
        ):
            if key in payload:
                settings[key] = self._coerce_bool_setting(payload[key], bool(settings[key]))

        if "bridgeReplacementMaxDepth" in payload:
            settings["bridgeReplacementMaxDepth"] = self._coerce_bridge_depth_setting(
                payload["bridgeReplacementMaxDepth"],
            )

        if "ainfReplacementMaxOuterArity" in payload:
            settings["ainfReplacementMaxOuterArity"] = self._coerce_ainf_outer_arity_setting(
                payload["ainfReplacementMaxOuterArity"],
            )

        if "maxPureArity" in payload:
            settings["maxPureArity"] = self._coerce_max_pure_arity_setting(
                payload["maxPureArity"],
            )

        return settings

    def _update_computation_settings_from_payload(
        self,
        data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        self.computation_settings = self._normalize_computation_settings(data)
        return self.computation_settings

    def undo(self, auto_run: bool = False, data: dict[str, Any] | None = None) -> dict[str, Any]:
        with self.lock:
            self._update_computation_settings_from_payload(data)

            if not self.actions:
                self.messages = ["Nothing to undo."]
                return self.state()

            removed = self.actions.pop()
            self._rebuild_from_actions()
            self.messages = [f"Undid {removed.get('kind', 'operation')}."]

            if auto_run:
                self._run_stage_report()

            return self.state()

    def export_save(self) -> dict[str, Any]:
        with self.lock:
            return {
                "schema": "ainf-game-save",
                "version": 1,
                "quiverName": self.quiver_name,
                "fileName": self.quiver_file_name,
                "savedAt": datetime.now(timezone.utc).isoformat(),
                "actions": json.loads(json.dumps(self.actions)),
                "computationSettings": json.loads(json.dumps(self.computation_settings)),
                "restoreRun": self.last_run is not None,
                "restoreGenerated": self.last_generation is not None,
                "summary": {
                    "vertices": sorted(self.Q.vertices, key=str),
                    "generators": [
                        item["label"]
                        for item in self._serialize_generators()
                    ],
                    "attachedCells": len(getattr(self.Q, "attachment_history", [])),
                    "actionCount": len(self.actions),
                },
            }

    def save_current_quiver(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        data = data if isinstance(data, dict) else {}
        save_as = bool(data.get("saveAs"))
        requested_file_name = clean_quiver_file_name(data.get("fileName"))
        overwrite = bool(data.get("overwrite"))

        with self.lock:
            current_file_name = clean_quiver_file_name(self.quiver_file_name)
            target_file_name = requested_file_name or current_file_name

            if not target_file_name:
                if self.quiver_name:
                    target_file_name = quiver_file_name_from_name(self.quiver_name)
                else:
                    target_file_name = default_save_file_name()

            path = saved_quiver_path(target_file_name)

            if (
                save_as
                and path.exists()
                and target_file_name != current_file_name
                and not overwrite
            ):
                raise GameError(
                    f"{target_file_name} already exists. Confirm overwrite to replace it."
                )

            self.quiver_file_name = target_file_name

            if not self.quiver_name:
                self.quiver_name = Path(target_file_name).stem

            save_data = self.export_save()
            text = f"{json.dumps(save_data, indent=4)}\n"
            SAVED_QUIVERS_DIR.mkdir(parents=True, exist_ok=True)
            tmp_path = path.with_name(f".{path.name}.tmp")
            tmp_path.write_text(text, encoding="utf-8")
            tmp_path.replace(path)

            self.messages = [f"Saved quiver to {target_file_name}."]
            state = self.state()
            state["saved"] = {
                "fileName": target_file_name,
                "path": str(path),
                "saveAs": save_as,
            }
            return state

    def import_save(self, data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise GameError("Save file must contain a JSON object.")

        if data.get("schema") != "ainf-game-save":
            raise GameError("This does not look like an A infinity game save file.")

        if int(data.get("version") or 0) != 1:
            raise GameError("This save file version is not supported.")

        actions = data.get("actions")

        if not isinstance(actions, list):
            raise GameError("Save file is missing its action log.")

        try:
            clean_actions = json.loads(json.dumps(actions))
        except Exception as exc:
            raise GameError("Save file contains non-JSON action data.") from exc

        if not all(isinstance(action, dict) for action in clean_actions):
            raise GameError("Save file action log is malformed.")

        with self.lock:
            old_Q = self.Q
            old_actions = self.actions
            old_messages = self.messages
            old_generation = self.last_generation
            old_pure_classes = self.last_pure_classes
            old_run = self.last_run
            old_plan = self.last_autocomplete_plan
            old_settings = dict(self.computation_settings)
            old_quiver_name = self.quiver_name
            old_quiver_file_name = self.quiver_file_name
            old_generator_order = list(self.generator_order)
            old_generator_order_custom = self.generator_order_custom

            try:
                self.Q = self.Quiver()
                self.actions = []
                self.messages = []
                self.last_generation = None
                self.last_pure_classes = empty_pure_classes_payload()
                self.last_run = None
                self.last_autocomplete_plan = None
                self._set_quiver_metadata_from_save(data)
                self._update_computation_settings_from_payload(data)
                self.generator_order = []
                self.generator_order_custom = False

                obsolete_stop = None

                fast_load = bool(data.get("fastLoad"))
                had_replay_flag = hasattr(self.Q, "_loading_replay")
                old_replay_flag = getattr(self.Q, "_loading_replay", False)

                if fast_load:
                    self.Q._loading_replay = True

                try:
                    for index, action in enumerate(clean_actions):
                        self._last_replay_action_skipped = False

                        try:
                            output = self._apply_action(action, replay=True)
                        except GameError as exc:
                            kind = action.get("kind", "unknown")
                            raise GameError(
                                "Could not load save at "
                                f"move {index + 1}/{len(clean_actions)} ({kind}): {exc}"
                            ) from exc

                        if getattr(self, "_last_replay_action_skipped", False):
                            obsolete_stop = {
                                "index": index,
                                "total": len(clean_actions),
                                "kind": action.get("kind", "unknown"),
                                "output": output,
                            }
                            break

                        self.actions.append(action)
                finally:
                    if fast_load:
                        if had_replay_flag:
                            self.Q._loading_replay = old_replay_flag
                        elif hasattr(self.Q, "_loading_replay"):
                            delattr(self.Q, "_loading_replay")

                partial_load = obsolete_stop is not None

                if data.get("restoreGenerated") and not partial_load:
                    self._refresh_generated()

                if data.get("restoreRun") and not partial_load:
                    self._run_stage_report()

                if partial_load:
                    move_number = obsolete_stop["index"] + 1
                    total = obsolete_stop["total"]
                    kind = obsolete_stop["kind"]
                    message = (
                        f"Loaded partial quiver save with {len(self.actions)} move(s). "
                        f"Stopped before obsolete move {move_number}/{total} "
                        f"({kind}); later moves were not loaded."
                    )
                else:
                    message = f"Loaded quiver save with {len(self.actions)} move(s)."

                self.messages = [message]
                return self.state()
            except Exception:
                self.Q = old_Q
                self.actions = old_actions
                self.messages = old_messages
                self.last_generation = old_generation
                self.last_pure_classes = old_pure_classes
                self.last_run = old_run
                self.last_autocomplete_plan = old_plan
                self.computation_settings = old_settings
                self.quiver_name = old_quiver_name
                self.quiver_file_name = old_quiver_file_name
                self.generator_order = old_generator_order
                self.generator_order_custom = old_generator_order_custom
                raise

    def _set_quiver_metadata_from_save(self, data: dict[str, Any]) -> None:
        file_name = clean_quiver_file_name(
            data.get("sourceFileName")
            or data.get("fileName")
            or data.get("quiverFileName")
        )
        name = clean_quiver_name(
            data.get("quiverName")
            or data.get("name")
        )

        if not name and file_name:
            name = Path(file_name).stem

        self.quiver_name = name
        self.quiver_file_name = file_name

    def update_quiver_name(self, data: dict[str, Any]) -> dict[str, Any]:
        name = clean_quiver_name(data.get("name"))

        if not name:
            raise GameError("Quiver name cannot be empty.")

        rename_file = bool(data.get("renameFile"))
        target_file_name = clean_quiver_file_name(
            data.get("fileName") or quiver_file_name_from_name(name)
        )
        renamed = False

        with self.lock:
            old_name = self.quiver_name
            old_file_name = self.quiver_file_name

            if rename_file and old_file_name and old_file_name != target_file_name:
                old_path = saved_quiver_path(old_file_name)
                new_path = saved_quiver_path(target_file_name)

                if not old_path.exists():
                    raise GameError(
                        f"Cannot rename {old_file_name}; it was not found in saved quivers."
                    )

                if new_path.exists():
                    raise GameError(
                        f"Cannot rename to {target_file_name}; that save file already exists."
                    )

                old_path.rename(new_path)
                self.quiver_file_name = target_file_name
                renamed = True

            self.quiver_name = name

            if not self.quiver_file_name and rename_file:
                self.quiver_file_name = target_file_name

            if renamed:
                self.messages = [f"Renamed quiver file to {self.quiver_file_name}."]
            elif old_name != name:
                self.messages = [f"Renamed quiver to {self.quiver_name}."]

            return self.state()

    def add_vertices(self, values: Any) -> dict[str, Any]:
        if isinstance(values, str):
            names = [
                item.strip()
                for item in values.replace("\n", ",").split(",")
                if item.strip()
            ]
        else:
            names = [clean_name(item, "Vertex") for item in values or []]

        if not names:
            raise GameError("Enter at least one vertex.")

        with self.lock:
            added = []

            for name in names:
                action = {"kind": "add_vertex", "name": clean_name(name, "Vertex")}
                self._apply_and_record(action)
                added.append(action["name"])

            self._clear_stage_analysis()
            self.messages = [f"Added vertices: {', '.join(added)}."]
            return self.state()

    def add_arrow(self, data: dict[str, Any]) -> dict[str, Any]:
        action = {
            "kind": "add_arrow",
            "name": clean_name(data.get("name"), "Arrow name"),
            "source": clean_name(data.get("source"), "Source"),
            "target": clean_name(data.get("target"), "Target"),
            "grading": parse_optional_int(data.get("grading")),
        }

        with self.lock:
            self._apply_and_record(action)
            self._clear_stage_analysis()
            self.messages = [
                f"Added generator {action['name']}: "
                f"{action['source']} -> {action['target']}."
            ]
            return self.state()

    def set_generator_order(self, data: dict[str, Any]) -> dict[str, Any]:
        order = data.get("order")

        if not isinstance(order, list):
            raise GameError("Generator order must be a list.")

        clean_order = [clean_name(name, "Generator") for name in order]

        if len(set(clean_order)) != len(clean_order):
            raise GameError("Generator order contains a duplicate.")

        with self.lock:
            current = self._current_generator_names()

            if set(clean_order) != set(current):
                raise GameError("Generator order must contain every current generator exactly once.")

            self._apply_and_record({
                "kind": "set_generator_order",
                "order": clean_order,
            })
            self.messages = ["Updated generator order."]
            return self.state()

    def remove_generator(self, data: dict[str, Any]) -> dict[str, Any]:
        name = clean_name(data.get("name"), "Generator")

        with self.lock:
            arrow = self.Q.arrows.get(name)

            if arrow is None or hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"):
                raise GameError(f"Generator {name} is not present.")

            if getattr(self.Q, "attachment_history", []):
                raise GameError("Undo attached cells before removing a generator.")

            kept_actions = [
                (
                    {
                        **action,
                        "order": [
                            item
                            for item in action.get("order", [])
                            if item != name
                        ],
                    }
                    if action.get("kind") == "set_generator_order"
                    else action
                )
                for action in self.actions
                if not (
                    action.get("kind") == "add_arrow"
                    and action.get("name") == name
                )
            ]

            if len(kept_actions) == len(self.actions):
                raise GameError(f"Could not find the creation record for {name}.")

            self.actions = kept_actions
            self._rebuild_from_actions()
            self._clear_stage_analysis()
            self.messages = [f"Removed generator {name}."]
            return self.state()

    def _coeff_is_zero(self, coeff: Any) -> bool:
        is_zero_coeff = self.namespace.get("is_zero_coeff")

        if callable(is_zero_coeff):
            try:
                return bool(is_zero_coeff(coeff))
            except Exception:
                pass

        try:
            simplify_coeff = self.namespace.get("simplify_coeff")

            if callable(simplify_coeff):
                coeff = simplify_coeff(coeff)
        except Exception:
            pass

        return str(coeff) == "0"

    def _single_product_from_expression(self, expression: Any) -> Any | None:
        if isinstance(expression, self.MPProduct):
            return expression

        if isinstance(expression, self.MasseyProduct):
            try:
                return expression.as_product()
            except Exception:
                return None

        if isinstance(expression, self.MPElement):
            products = [
                product
                for product, coeff in expression.terms.items()
                if (
                    isinstance(product, self.MPProduct)
                    and not self._coeff_is_zero(coeff)
                )
            ]

            if len(products) == 1:
                return products[0]

        return None

    def _format_product_for_warning(self, product: Any) -> str:
        try:
            factors = self.Q.canonical_mp_factors(product.factors)
            return self.Q.format_mp_input_product(factors)
        except Exception:
            return self._safe_str(product)

    def _primitive_warning_for_product(self, product: Any, label: str) -> dict[str, str] | None:
        product = self._single_product_from_expression(product) or product

        if not isinstance(product, self.MPProduct):
            return None

        try:
            candidates = self.Q.find_primitives_mp_product(
                product,
                record=False,
                minimal_only=False,
                use_bridge_replacements=True,
            )
        except Exception:
            candidates = []

        if not candidates:
            return None

        candidate = candidates[0]
        source = (
            candidate.get("source")
            or candidate.get("kind")
            or "primitive certificate"
        )
        block = tuple(candidate.get("block", ()) or ())
        block_text = ""

        if block:
            try:
                block_text = self.Q.format_mp_input_product(block)
            except Exception:
                block_text = self._safe_str(block)

        return {
            "label": label,
            "product": self._format_product_for_warning(product),
            "source": str(source).replace("_", " "),
            "block": block_text,
        }

    def _attachment_primitive_warning(self, expression: Any) -> str | None:
        product = self._single_product_from_expression(expression)

        if product is None:
            return None

        warning = self._primitive_warning_for_product(product, "the selected differential")

        if warning is None:
            return None

        detail = f" via {warning['source']}"

        if warning["block"]:
            detail += f" on {warning['block']}"

        return (
            "Warning: not attaching this cell because "
            f"{warning['product']} already has a primitive{detail}. "
            "Attaching d f to that element would make the new generator redundant."
        )

    def _bridge_primitive_warning(self, left: Any, right: Any) -> str | None:
        warnings = []

        for label, product in (("left side", left), ("right side", right)):
            warning = self._primitive_warning_for_product(product, label)

            if warning is not None:
                detail = (
                    f"{warning['label']} {warning['product']} already has "
                    f"a primitive via {warning['source']}"
                )

                if warning["block"]:
                    detail += f" on {warning['block']}"

                warnings.append(detail)

        if not warnings:
            return None

        return (
            "Warning: not attaching this bridge because "
            + "; ".join(warnings)
            + ". A bridge v[A-B] with a primitive side is equivalent to "
            "attaching a cell resolving the other side."
        )

    def attach_mp_cell(self, data: dict[str, Any]) -> dict[str, Any]:
        expression = self._normalize_expression_spec(data.get("expression"))
        action = {
            "kind": "attach_mp_cell",
            "expression": expression,
        }

        with self.lock:
            self._update_computation_settings_from_payload(data)

            with self._computation_context(include_primitive_details=False):
                expression_object = self._expression_from_spec(expression)
                warning = self._attachment_primitive_warning(expression_object)

            if warning is not None:
                self.messages = [warning]
                raise GameError(warning)

            self._apply_and_record(action)

            if data.get("autoRun"):
                self._run_stage_report()

            return self.state()

    def attach_bridge(self, data: dict[str, Any]) -> dict[str, Any]:
        left = self._normalize_product_spec(data.get("left"))
        right = self._normalize_product_spec(data.get("right"))
        action = {
            "kind": "attach_bridge",
            "left": left,
            "right": right,
        }

        with self.lock:
            self._update_computation_settings_from_payload(data)

            with self._computation_context(include_primitive_details=False):
                left_product = self._product_from_spec(left)
                right_product = self._product_from_spec(right)
                warning = self._bridge_primitive_warning(left_product, right_product)

            if warning is not None:
                self.messages = [warning]
                raise GameError(warning)

            self._apply_and_record(action)

            if data.get("autoRun"):
                self._run_stage_report()

            return self.state()

    def generate(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        data = data or {}

        with self.lock:
            self._update_computation_settings_from_payload(data)
            include_details = (
                bool(self.computation_settings["includePrimitiveDetails"])
                and not bool(self.computation_settings["disableMasseyFormula"])
            )
            self._refresh_generated(include_primitive_details=include_details)
            detail_text = " with primitive details" if include_details else ""
            self.messages = [f"Generated Massey products{detail_text} from the current stage."]
            return self.state()

    def run(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        with self.lock:
            self._update_computation_settings_from_payload(data)
            self._run_stage_report()
            return self.state()

    def update_settings(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        with self.lock:
            self._update_computation_settings_from_payload(data)
            self.messages = ["Updated computation settings."]
            return self.state()

    def stopped_state(self) -> dict[str, Any]:
        with self.lock:
            self.messages = ["Stopped current computation."]
            return self.state()

    def autocomplete_plan(self, data: dict[str, Any] | None = None) -> dict[str, Any]:
        data = data or {}

        with self.lock:
            self._update_computation_settings_from_payload(data)
            kwargs = self._autocomplete_kwargs_from_payload(data)
            with self._computation_context(include_primitive_details=False):
                plan, output = capture_output(self.Q.cyclic_autocomplete_plan, **kwargs)
            self.last_autocomplete_plan = plan
            self.messages = output or [self._autocomplete_plan_message(plan)]
            return self.state()

    def autocomplete_plan_selected(self, data: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            self._update_computation_settings_from_payload(data)
            inputs = self._validated_isolated_selected_inputs(data.get("choiceInputs"))
            max_pure_arity = int(data.get("maxPureArity") or 8)
            max_level = max(max_pure_arity - len(inputs), 0)
            with self._computation_context(include_primitive_details=False):
                plan, output = capture_output(
                    self.Q.massey_orbit_tower_plan,
                    inputs,
                    leave_inputs=inputs,
                    require_all_other_rotations=True,
                    max_level=max_level,
                )
            self.last_autocomplete_plan = plan
            self.messages = output or [self._autocomplete_plan_message(plan)]
            return self.state()

    def autocomplete_apply(self, data: dict[str, Any]) -> dict[str, Any]:
        action = {
            "kind": "autocomplete",
            "choice_inputs": data.get("choiceInputs"),
            "max_pure_arity": int(data.get("maxPureArity") or 8),
        }

        with self.lock:
            self._update_computation_settings_from_payload(data)
            self._apply_and_record(action)

            if data.get("autoRun"):
                self._run_stage_report()

            return self.state()

    def autocomplete_apply_selected(self, data: dict[str, Any]) -> dict[str, Any]:
        action = {
            "kind": "autocomplete_selected",
            "choice_inputs": data.get("choiceInputs"),
            "max_pure_arity": int(data.get("maxPureArity") or 8),
        }

        with self.lock:
            self._update_computation_settings_from_payload(data)
            self._apply_and_record(action)

            if data.get("autoRun"):
                self._run_stage_report()

            return self.state()

    def _apply_and_record(self, action: dict[str, Any]) -> None:
        messages = self._apply_action(action)
        self.actions.append(action)
        self.messages = messages

    def _clear_stage_analysis(self) -> None:
        self.last_generation = None
        self.last_pure_classes = empty_pure_classes_payload()
        self.last_run = None
        self.last_autocomplete_plan = None

    def _rebuild_from_actions(self) -> None:
        actions = list(self.actions)
        self.Q = self.Quiver()
        self.actions = []
        self.generator_order = []
        self.generator_order_custom = False
        self.last_generation = None
        self.last_pure_classes = empty_pure_classes_payload(dirty=True)
        self.last_run = None
        self.last_autocomplete_plan = None

        for action in actions:
            self._last_replay_action_skipped = False
            self._apply_action(action, replay=True)

            if not getattr(self, "_last_replay_action_skipped", False):
                self.actions.append(action)

    @staticmethod
    def _is_obsolete_replay_massey_error(exc: GameError) -> bool:
        message = str(exc)
        return (
            "A selected Massey product is not defined now." in message
            or "A selected Massey input is not defined now." in message
            or "That Massey product is not defined at this stage." in message
        )

    def _apply_action(self, action: dict[str, Any], replay: bool = False) -> list[str]:
        kind = action.get("kind")

        if kind == "add_vertex":
            _, output = capture_output(self.Q.add_vertex, action["name"])
            return output

        if kind == "add_arrow":
            _, output = capture_output(
                self.Q.add_arrow,
                action["name"],
                action["source"],
                action["target"],
                grading=action.get("grading"),
            )
            if self.generator_order_custom and action["name"] not in self.generator_order:
                self.generator_order.append(action["name"])
            return output

        if kind == "set_generator_order":
            order = [clean_name(name, "Generator") for name in action.get("order", [])]
            current = self._current_generator_names()

            if set(order) != set(current):
                raise GameError("Saved generator order does not match the current generators.")

            self.generator_order = list(order)
            self.generator_order_custom = True
            return [] if replay else ["Updated generator order."]

        if kind == "attach_mp_cell":
            try:
                expression = self._expression_from_spec(action["expression"])
            except GameError as exc:
                if replay and self._is_obsolete_replay_massey_error(exc):
                    self._last_replay_action_skipped = True
                    return [
                        "Skipped saved MP cell: the selected Massey product is no longer defined.",
                    ]
                raise

            include_details = bool(self.computation_settings["includePrimitiveDetails"])
            self.Q.last_refused_mp_cell = None

            with self._computation_context(include_primitive_details=include_details):
                cell, output = capture_output(self.Q.attach_mp_cell, expression)

            if cell is None:
                refusal = getattr(self.Q, "last_refused_mp_cell", None)
                equivalent_refusal = (
                    isinstance(refusal, dict)
                    and refusal.get("reason") == "equivalent_resolved"
                )

                if replay and equivalent_refusal:
                    self._last_replay_action_skipped = True
                    return [
                        *output,
                        "Skipped saved MP cell: an equivalent Massey presentation is already resolved.",
                    ]

                if equivalent_refusal:
                    raise GameError(
                        "An equivalent Massey presentation already has a primitive."
                    )

                raise GameError("The MP cell could not be attached.")

            generation_output = [] if replay else self._refresh_after_resolve(cells=[cell])

            if not replay:
                self.last_run = None
                self.last_autocomplete_plan = None

            return [*output, *generation_output]

        if kind == "attach_bridge":
            try:
                left = self._product_from_spec(action["left"])
                right = self._product_from_spec(action["right"])
            except GameError as exc:
                if replay and self._is_obsolete_replay_massey_error(exc):
                    self._last_replay_action_skipped = True
                    return [
                        "Skipped saved bridge: the selected Massey product is no longer defined.",
                    ]
                raise

            include_details = bool(self.computation_settings["includePrimitiveDetails"])
            self.Q.last_refused_bridge_cell = None

            with self._computation_context(include_primitive_details=include_details):
                cell, output = capture_output(self.Q.attach_bridge, left, right)

            if cell is None:
                refusal = getattr(self.Q, "last_refused_bridge_cell", None)
                redundant_generator_refusal = (
                    isinstance(refusal, dict)
                    and refusal.get("reason") == "generator_redundant_bridge"
                )

                if redundant_generator_refusal:
                    warning = next(
                        (
                            line
                            for line in output
                            if line.startswith("Warning: not attaching this bridge")
                        ),
                        "The bridge would make a generator redundant.",
                    )

                    if replay:
                        self._last_replay_action_skipped = True
                        return [
                            *output,
                            "Skipped saved bridge: it would make a generator redundant.",
                        ]

                    raise GameError(warning)

                raise GameError("The bridge cell could not be attached.")

            generation_output = [] if replay else self._refresh_after_resolve(cells=[cell])

            if not replay:
                self.last_run = None
                self.last_autocomplete_plan = None

            return [*output, *generation_output]

        if kind == "autocomplete":
            kwargs = self._autocomplete_kwargs_from_action(action)
            with self._computation_context(include_primitive_details=False):
                result, output = capture_output(self.Q.apply_cyclic_autocomplete, **kwargs)
            self.last_autocomplete_plan = None

            if result.get("attached_count", 0) == 0 and result.get("status") not in {"won", "dry_run"}:
                raise GameError(result.get("reason") or "Autocomplete did not attach a cell.")

            generation_output = [] if replay else self._refresh_after_resolve()

            if not replay:
                self.last_run = None

            message = (
                f"Autocomplete {result.get('status')}: "
                f"attached {result.get('attached_count', 0)} cell(s)."
            )
            return [*output, message, *generation_output]

        if kind == "autocomplete_selected":
            inputs = self._validated_isolated_selected_inputs(action.get("choice_inputs"))
            max_pure_arity = int(action.get("max_pure_arity") or 8)
            max_level = max(max_pure_arity - len(inputs), 0)
            with self._computation_context(include_primitive_details=False):
                result, output = capture_output(
                    self.Q.apply_massey_orbit_tower,
                    inputs,
                    leave_inputs=inputs,
                    require_all_other_rotations=True,
                    max_level=max_level,
                    max_cells=50,
                )
            self.last_autocomplete_plan = None

            if result.get("attached_count", 0) == 0 and result.get("status") not in {"complete", "dry_run"}:
                raise GameError(result.get("reason") or "Selected autocomplete did not attach a cell.")

            generation_output = [] if replay else self._refresh_after_resolve()

            if not replay:
                self.last_run = None

            message = (
                f"Selected autocomplete {result.get('status')}: "
                f"attached {result.get('attached_count', 0)} cell(s)."
            )
            return [*output, message, *generation_output]

        raise GameError(f"Unknown operation: {kind}")

    def _refresh_generated(
        self,
        cells: list[Any] | None = None,
        include_primitive_details: bool | None = None,
    ) -> list[str]:
        include_details = (
            bool(self.computation_settings["includePrimitiveDetails"])
            if include_primitive_details is None
            else bool(include_primitive_details)
        )
        include_details = (
            include_details
            and not bool(self.computation_settings["disableMasseyFormula"])
        )

        with self._computation_context(include_primitive_details=include_details):
            result, output = capture_output(
                self.Q.generate_massey_products,
                cells=cells,
                record=True,
                verbose=False,
                split_by_primitives=include_details,
                include_primitive_details=include_details,
            )

        self.last_generation = result
        self.last_pure_classes = empty_pure_classes_payload(dirty=True)
        return [
            line
            for line in output
            if line != "Warning: cannot convert a sum to an MPProduct."
        ]

    def _refresh_after_resolve(self, cells: list[Any] | None = None) -> list[str]:
        if self.computation_settings.get("generateAfterResolve"):
            return self._refresh_generated(cells=cells)

        self.last_generation = None
        self.last_pure_classes = empty_pure_classes_payload(dirty=True)
        return []

    @contextlib.contextmanager
    def _computation_context(self, include_primitive_details: bool | None = None):
        settings = dict(DEFAULT_COMPUTATION_SETTINGS)
        settings.update(self.computation_settings)
        include_details = (
            bool(settings["includePrimitiveDetails"])
            if include_primitive_details is None
            else bool(include_primitive_details)
        )
        disable_massey_formula = bool(settings["disableMasseyFormula"])
        suppress_primitive_expansion = not include_details or disable_massey_formula
        skip_susceptible_search = bool(settings["skipSusceptibleSearch"])
        detect_redundant_generators = bool(settings["detectRedundantGenerators"])
        search_pure_bridge_resolvers = bool(settings["searchPureBridgeResolvers"])

        original_susceptible_search = getattr(self.Q, "susceptible_mp_products_from_factors", None)
        had_suppress_flag = hasattr(self.Q, "_suppress_primitive_expansion")
        original_suppress_flag = getattr(self.Q, "_suppress_primitive_expansion", False)
        had_bridge_depth = hasattr(self.Q, "bridge_replacement_max_depth")
        original_bridge_depth = getattr(self.Q, "bridge_replacement_max_depth", None)
        had_ainf_outer_arity = hasattr(self.Q, "ainf_replacement_max_outer_arity")
        original_ainf_outer_arity = getattr(self.Q, "ainf_replacement_max_outer_arity", None)
        had_self_filter = hasattr(self.Q, "filter_self_expanding_replacements")
        original_self_filter = getattr(self.Q, "filter_self_expanding_replacements", None)
        had_fast_generation = hasattr(self.Q, "fast_massey_generation")
        original_fast_generation = getattr(self.Q, "fast_massey_generation", None)
        had_defer_bridge = hasattr(self.Q, "defer_bridge_expansion")
        original_defer_bridge = getattr(self.Q, "defer_bridge_expansion", None)
        had_redundant_detector = hasattr(self.Q, "detect_redundant_generators")
        original_redundant_detector = getattr(self.Q, "detect_redundant_generators", None)
        had_pure_bridge_search = hasattr(self.Q, "search_pure_bridge_resolvers")
        original_pure_bridge_search = getattr(self.Q, "search_pure_bridge_resolvers", None)
        had_disable_formula = hasattr(self.Q, "_disable_massey_formula")
        original_disable_formula = getattr(self.Q, "_disable_massey_formula", False)

        if skip_susceptible_search and original_susceptible_search is not None:
            self.Q.susceptible_mp_products_from_factors = lambda *args, **kwargs: []

        if suppress_primitive_expansion:
            self.Q._suppress_primitive_expansion = True
        elif had_suppress_flag:
            self.Q._suppress_primitive_expansion = False

        self.Q.bridge_replacement_max_depth = settings["bridgeReplacementMaxDepth"]
        self.Q.ainf_replacement_max_outer_arity = settings["ainfReplacementMaxOuterArity"]
        self.Q.filter_self_expanding_replacements = bool(settings["filterSelfExpandingReplacements"])
        self.Q.fast_massey_generation = bool(settings["fastMasseyGeneration"])
        self.Q.defer_bridge_expansion = suppress_primitive_expansion
        self.Q.detect_redundant_generators = detect_redundant_generators
        self.Q.search_pure_bridge_resolvers = search_pure_bridge_resolvers
        self.Q._disable_massey_formula = disable_massey_formula

        try:
            yield
        finally:
            if skip_susceptible_search and original_susceptible_search is not None:
                self.Q.susceptible_mp_products_from_factors = original_susceptible_search

            if had_suppress_flag:
                self.Q._suppress_primitive_expansion = original_suppress_flag
            elif hasattr(self.Q, "_suppress_primitive_expansion"):
                delattr(self.Q, "_suppress_primitive_expansion")

            if had_bridge_depth:
                self.Q.bridge_replacement_max_depth = original_bridge_depth
            elif hasattr(self.Q, "bridge_replacement_max_depth"):
                delattr(self.Q, "bridge_replacement_max_depth")

            if had_ainf_outer_arity:
                self.Q.ainf_replacement_max_outer_arity = original_ainf_outer_arity
            elif hasattr(self.Q, "ainf_replacement_max_outer_arity"):
                delattr(self.Q, "ainf_replacement_max_outer_arity")

            if had_self_filter:
                self.Q.filter_self_expanding_replacements = original_self_filter
            elif hasattr(self.Q, "filter_self_expanding_replacements"):
                delattr(self.Q, "filter_self_expanding_replacements")

            if had_fast_generation:
                self.Q.fast_massey_generation = original_fast_generation
            elif hasattr(self.Q, "fast_massey_generation"):
                delattr(self.Q, "fast_massey_generation")

            if had_defer_bridge:
                self.Q.defer_bridge_expansion = original_defer_bridge
            elif hasattr(self.Q, "defer_bridge_expansion"):
                delattr(self.Q, "defer_bridge_expansion")

            if had_redundant_detector:
                self.Q.detect_redundant_generators = original_redundant_detector
            elif hasattr(self.Q, "detect_redundant_generators"):
                delattr(self.Q, "detect_redundant_generators")

            if had_pure_bridge_search:
                self.Q.search_pure_bridge_resolvers = original_pure_bridge_search
            elif hasattr(self.Q, "search_pure_bridge_resolvers"):
                delattr(self.Q, "search_pure_bridge_resolvers")

            if had_disable_formula:
                self.Q._disable_massey_formula = original_disable_formula
            elif hasattr(self.Q, "_disable_massey_formula"):
                delattr(self.Q, "_disable_massey_formula")

    @contextlib.contextmanager
    def _temporary_quiver_flag(self, name: str, value: Any):
        had_flag = hasattr(self.Q, name)
        old_value = getattr(self.Q, name, None)
        setattr(self.Q, name, value)

        try:
            yield
        finally:
            if had_flag:
                setattr(self.Q, name, old_value)
            elif hasattr(self.Q, name):
                delattr(self.Q, name)

    def _run_stage_report(self) -> None:
        max_pure_arity = int(
            self.computation_settings.get(
                "maxPureArity",
                DEFAULT_COMPUTATION_SETTINGS["maxPureArity"],
            )
        )
        with self._temporary_quiver_flag("skip_deep_tower_resolution", True):
            generation_output = self._refresh_generated(
                include_primitive_details=False,
            )

        with (
            self._computation_context(include_primitive_details=False),
            self._temporary_quiver_flag("skip_deep_tower_resolution", True),
        ):
            report, output = capture_output(
                self.Q.cyclic_search_stage_report,
                max_pure_arity=max_pure_arity,
                include_higher_massey_products=False,
                record=True,
            )
            summary = self._summarize_run(report)
        visible_output = visible_computation_output(output)
        self.last_run = {
            "summary": summary,
            "report": report,
        }
        self.last_pure_classes = self._serialize_pure_class_result(
            report.get("pure_generated_result", {}),
            dirty=False,
        )
        self.messages = [
            *generation_output,
            *(visible_output or [summary["headline"]]),
        ]

    def _normalize_expression_spec(self, spec: Any) -> dict[str, Any]:
        if not isinstance(spec, dict):
            raise GameError("Choose an MP expression first.")

        kind = spec.get("type")

        if kind == "massey":
            inputs = spec.get("inputs") or []

            if not inputs:
                raise GameError("Choose at least one input for the Massey product.")

            return {
                "type": "massey",
                "inputs": [self._normalize_factor_spec(item) for item in inputs],
            }

        if kind == "product":
            return self._normalize_product_spec(spec)

        raise GameError("Unknown MP expression type.")

    def _normalize_product_spec(self, spec: Any) -> dict[str, Any]:
        if not isinstance(spec, dict) or spec.get("type") != "product":
            raise GameError("Choose an MP product first.")

        factors = spec.get("factors") or []

        if not factors:
            raise GameError("Choose at least one factor.")

        return {
            "type": "product",
            "coefficient": self._coefficient_text_from_spec(
                spec.get("coefficient", "1")
            ),
            "factors": [self._normalize_factor_spec(item) for item in factors],
        }

    def _normalize_factor_spec(self, spec: Any) -> dict[str, Any]:
        if not isinstance(spec, dict):
            raise GameError("Invalid factor.")

        kind = spec.get("type")

        if kind == "arrow":
            return {
                "type": "arrow",
                "name": clean_name(spec.get("name"), "Arrow"),
            }

        if kind == "path":
            names = spec.get("arrows") or []

            if not names:
                raise GameError("Path factors need at least one arrow.")

            return {
                "type": "path",
                "arrows": [clean_name(item, "Path arrow") for item in names],
            }

        if kind == "zero":
            return {
                "type": "zero",
                "value": 0,
            }

        if kind == "mp":
            inputs = spec.get("inputs") or []

            if not inputs:
                raise GameError("Massey product factors need inputs.")

            return {
                "type": "mp",
                "inputs": [self._normalize_factor_spec(item) for item in inputs],
            }

        if kind == "product":
            return self._normalize_product_spec(spec)

        raise GameError("Unknown factor type.")

    def _expression_from_spec(self, spec: dict[str, Any]) -> Any:
        if spec["type"] == "massey":
            inputs = [self._factor_input_from_spec(item) for item in spec["inputs"]]
            return self._massey_product_from_inputs(
                inputs,
                "That Massey product is not defined at this stage.",
            )

        if spec["type"] == "product":
            return self._product_from_spec(spec)

        raise GameError("Unknown expression type.")

    def _product_from_spec(self, spec: dict[str, Any]) -> Any:
        factors = [self._mp_factor_from_spec(item) for item in spec["factors"]]
        product = self.Q.multiply_mp_factors(factors)

        if product is None:
            raise GameError("Could not build the selected product.")

        coeff = self._coefficient_from_spec(spec.get("coefficient", "1"))

        if str(coeff) != "1":
            product = coeff * product

        return product

    def _coefficient_from_spec(self, value: Any) -> Any:
        text = str(value if value is not None else "1").strip() or "1"

        try:
            rational_coeff = self.namespace.get("rational_coeff")

            if callable(rational_coeff):
                return rational_coeff(text)

            sp = self.namespace.get("sp")
            coeff = sp.Rational(text.replace(" ", "")) if sp is not None else int(text)
            simplify_coeff = self.namespace.get("simplify_coeff")

            if callable(simplify_coeff):
                coeff = simplify_coeff(coeff)

            return coeff
        except Exception as exc:
            raise GameError(
                "Coefficient must be a rational number, for example 1, -2, or 3/4."
            ) from exc

    def _coefficient_text_from_spec(self, value: Any) -> str:
        return str(self._coefficient_from_spec(value))

    def _mp_factor_from_spec(self, spec: dict[str, Any]) -> Any:
        if spec["type"] == "arrow":
            arrow = self._arrow_from_spec(spec)
            factor = self.Q.mp(arrow)

            if factor is None:
                raise GameError(f"Could not build Q.mp({arrow}).")

            return factor

        if spec["type"] == "mp":
            inputs = [self._factor_input_from_spec(item) for item in spec["inputs"]]
            return self._massey_product_from_inputs(
                inputs,
                "A selected Massey product is not defined now.",
            )

        raise GameError("Unknown factor type.")

    def _factor_input_from_spec(self, spec: dict[str, Any]) -> Any:
        if spec["type"] == "arrow":
            return self._arrow_from_spec(spec)

        if spec["type"] == "path":
            return self._path_from_spec(spec)

        if spec["type"] == "zero":
            return 0

        if spec["type"] == "mp":
            inputs = [self._factor_input_from_spec(item) for item in spec["inputs"]]
            return self._massey_product_from_inputs(
                inputs,
                "A selected Massey input is not defined now.",
            )

        if spec["type"] == "product":
            return self._product_from_spec(spec)

        raise GameError("Unknown input type.")

    def _massey_product_from_inputs(self, inputs: list[Any], error_message: str) -> Any:
        if getattr(self.Q, "_loading_replay", False):
            return self.MasseyProduct(self.Q, tuple(inputs))

        virtual_mp = getattr(self.Q, "virtual_mp", None)

        if callable(virtual_mp):
            M = virtual_mp(*inputs)
        else:
            M = self.Q.mp(*inputs)

        if M is None:
            raise GameError(error_message)

        return M

    def _path_from_spec(self, spec: dict[str, Any]) -> Any:
        names = spec.get("arrows") or []

        try:
            return self.Q.path_from_names(names)
        except Exception as exc:
            raise GameError("Could not build the selected path input.") from exc

    def _arrow_from_spec(self, spec: dict[str, Any]) -> Any:
        name = clean_name(spec.get("name"), "Arrow")
        arrow = self.Q.arrows.get(name)

        if arrow is None:
            raise GameError(f"Arrow {name} is not present in the current quiver.")

        return arrow

    def _autocomplete_kwargs_from_payload(self, data: dict[str, Any]) -> dict[str, Any]:
        max_pure_arity = int(data.get("maxPureArity") or 8)
        choice_inputs = data.get("choiceInputs")
        kwargs: dict[str, Any] = {
            "max_pure_arity": max_pure_arity,
            "resolve_non_isolated": data.get("resolveNonIsolated") or "stop",
        }

        if choice_inputs:
            inputs = self._autocomplete_presentation_inputs_from_specs(choice_inputs)
            kwargs["pure_inputs"] = inputs
            kwargs["leave_inputs"] = inputs

        return kwargs

    def _autocomplete_kwargs_from_action(self, action: dict[str, Any]) -> dict[str, Any]:
        data = {
            "maxPureArity": action.get("max_pure_arity", 8),
            "choiceInputs": action.get("choice_inputs"),
            "resolveNonIsolated": "attach_all_but_leave",
        }
        kwargs = self._autocomplete_kwargs_from_payload(data)
        kwargs.update({
            "resolve_non_isolated": "attach_all_but_leave",
            "max_steps": 20,
            "max_cells": 50,
        })
        return kwargs

    def _validated_isolated_selected_inputs(self, choice_inputs: Any) -> tuple[Any, ...]:
        if not choice_inputs:
            raise GameError("Select an A_infinity monomial before using selected autocomplete.")

        inputs = self._autocomplete_presentation_inputs_from_specs(choice_inputs)

        if len(inputs) < 3:
            raise GameError("Selected autocomplete needs a Massey product of arity at least 3.")

        try:
            defined = self.Q.can_define_mp(*inputs)
        except Exception:
            defined = False

        if not defined:
            raise GameError("The selected A_infinity monomial is not defined by current certificates now.")

        report, _ = capture_output(
            self.Q.pure_massey_cyclic_class_report,
            inputs,
            require_direct_primitives=False,
            record=True,
        )
        rotations = report.get("rotations") or []

        if not rotations:
            raise GameError(report.get("reason") or "The selected monomial does not define a cyclic class.")

        selected_key = tuple(self.Q.mp_factor_key(item) for item in inputs)
        selected_index = 0

        for index, rotation in enumerate(rotations):
            rotation_key = tuple(self.Q.mp_factor_key(item) for item in rotation.get("inputs", ()))

            if rotation_key == selected_key:
                selected_index = index
                break

        missing = []

        for index, rotation in enumerate(rotations):
            if index == selected_index:
                continue

            if not rotation.get("defined"):
                missing.append(f"rotation {index + 1} is not defined")
            elif not rotation.get("resolved"):
                missing.append(f"rotation {index + 1} is not resolved")

        if missing:
            detail = "; ".join(missing[:3])

            if len(missing) > 3:
                detail += f"; and {len(missing) - 3} more"

            raise GameError(
                "The selected Massey product is not isolated yet: "
                f"{detail}."
            )

        return inputs

    def _autocomplete_presentation_inputs_from_specs(self, choice_inputs: Any) -> tuple[Any, ...]:
        """
        Interpret a selected autocomplete monomial by its presentation.

        A single selected factor Q.mp(x1,...,xn) should autocomplete the pure
        n-fold presentation, not the length-one factor represented by that
        object.  Other products are still interpreted as their displayed list
        of factors.
        """

        specs = list(choice_inputs or [])

        if len(specs) == 1 and isinstance(specs[0], dict):
            spec = specs[0]

            if spec.get("type") in {"mp", "massey"}:
                specs = list(spec.get("inputs") or [])

        return tuple(self._factor_input_from_spec(item) for item in specs)

    def _autocomplete_plan_message(self, plan: dict[str, Any]) -> str:
        status = plan.get("status", "unknown")

        if status == "needs_choice":
            return "Autocomplete needs a class choice."

        if status == "attach":
            return "Autocomplete can attach the proposed cell(s)."

        if status == "won":
            return "Autocomplete found no remaining class in range."

        return plan.get("reason") or f"Autocomplete status: {status}."

    def state(self) -> dict[str, Any]:
        if not self.lock.acquire(blocking=False):
            return self.busy_state()

        try:
            with self._computation_context(include_primitive_details=False):
                configuration_graph = self._serialize_configuration_graph()
                with self._temporary_quiver_flag("skip_deep_tower_resolution", True):
                    generated, _ = capture_output(self._serialize_generated)

            return {
                "quiver": self._serialize_quiver_metadata(),
                "vertices": sorted(self.Q.vertices, key=str),
                "arrows": self._serialize_arrows(),
                "generators": self._serialize_generators(),
                "configurationGraph": configuration_graph,
                "generated": generated,
                "attachments": self._serialize_attachments(),
                "bridgeProducts": self._serialize_bridge_products(),
                "run": self._serialize_last_run(),
                "autocompletePlan": self._serialize_autocomplete_plan(),
                "computation": self._serialize_computation(),
                "operation": CANCELLER.status(),
                "messages": list(self.messages[-12:]),
                "canUndo": bool(self.actions),
                "actionCount": len(self.actions),
            }
        finally:
            self.lock.release()

    def busy_state(self) -> dict[str, Any]:
        return {
            "busy": True,
            "operation": CANCELLER.status(),
            "messages": ["A computation is still running."],
        }

    def _serialize_quiver_metadata(self) -> dict[str, Any]:
        file_name = clean_quiver_file_name(self.quiver_file_name)
        name = clean_quiver_name(self.quiver_name)
        suggested_file_name = quiver_file_name_from_name(name) if name else (file_name or "")
        local_path_exists = False

        if file_name:
            try:
                local_path_exists = saved_quiver_path(file_name).exists()
            except GameError:
                local_path_exists = False

        return {
            "name": name,
            "fileName": file_name,
            "suggestedFileName": suggested_file_name,
            "localFileExists": bool(file_name and local_path_exists),
            "canRenameFile": bool(file_name and local_path_exists),
        }

    def _serialize_computation(self) -> dict[str, Any]:
        settings = dict(DEFAULT_COMPUTATION_SETTINGS)
        settings.update(self.computation_settings)
        tower_history = list(getattr(self.Q, "completed_massey_tower_history", []) or [])
        tower_uses = list(getattr(self.Q, "completed_massey_tower_primitive_uses", []) or [])
        filtered_edges = list(getattr(self.Q, "filtered_self_expanding_replacement_edges", []) or [])

        return {
            "settings": settings,
            "towerHistoryCount": len(tower_history),
            "activeTowerCount": sum(
                1
                for item in tower_history
                if not isinstance(item, dict) or item.get("active", True)
            ),
            "towerPrimitiveUseCount": len(tower_uses),
            "filteredSelfExpandingReplacementCount": len(filtered_edges),
        }

    def _serialize_arrows(self) -> list[dict[str, Any]]:
        arrows = []

        for name in sorted(self.Q.arrows.keys(), key=str):
            arrow = self.Q.arrows[name]
            arrows.append({
                "name": name,
                "label": str(arrow),
                "graphLabel": self._graph_arrow_label(arrow),
                "source": arrow.source,
                "target": arrow.target,
                "grading": str(arrow.grading) if arrow.grading is not None else "",
                "height": getattr(arrow, "height", 0),
                "isCell": hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"),
                "cellPrefix": getattr(arrow, "cell_prefix", None),
                "differential": self._safe_str(self.Q.differential.get(arrow)),
            })

        return arrows

    def _graph_arrow_label(self, arrow: Any) -> str:
        if hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"):
            prefix = getattr(arrow, "cell_prefix", None) or "u"
            index = getattr(arrow, "index", None)

            if index is not None and str(index).isdigit():
                return f"{prefix}{index}"

            name = str(getattr(arrow, "name", ""))

            if name.startswith("cell_") and name.rsplit("_", 1)[-1].isdigit():
                return f"{prefix}{name.rsplit('_', 1)[-1]}"

            return str(arrow).split("[", 1)[0] or str(arrow)

        label = str(arrow)

        if "Q.mp" in label or len(label) > 18:
            return label.split("*", 1)[0].split("[", 1)[0] or label[:12]

        return label

    def _current_generator_names(self) -> list[str]:
        return [
            name
            for name, arrow in self.Q.arrows.items()
            if not (hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"))
        ]

    def _serialize_generators(self) -> list[dict[str, Any]]:
        items = []
        current_names = set(self._current_generator_names())

        if self.generator_order_custom:
            ordered_names = [
                name
                for name in self.generator_order
                if name in current_names
            ]
            ordered_seen = set(ordered_names)
            ordered_names.extend(
                name
                for name in sorted(current_names, key=str)
                if name not in ordered_seen
            )
        else:
            ordered_names = sorted(current_names, key=str)

        for name in ordered_names:
            arrow = self.Q.arrows[name]

            items.append({
                "label": str(arrow),
                "detail": f"{arrow.source} -> {arrow.target}",
                "source": arrow.source,
                "target": arrow.target,
                "spec": self._factor_spec(arrow),
                "kind": "generator",
                "resolved": False,
            })

        return items

    def _generator_name_from_mp_factor(self, factor: Any) -> str | None:
        try:
            factor = self.Q.normalize_mp_input(factor)
        except Exception:
            pass

        if isinstance(factor, self.MasseyProduct):
            inputs = tuple(getattr(factor, "inputs", ()) or ())

            if len(inputs) != 1:
                return None

            factor = inputs[0]

        if isinstance(factor, self.Arrow):
            if hasattr(factor, "cell_prefix") or hasattr(factor, "index"):
                return None

            return str(factor.name)

        if isinstance(factor, self.Path) and len(factor.arrows) == 1:
            arrow = factor.arrows[0]

            if isinstance(arrow, self.Arrow):
                if hasattr(arrow, "cell_prefix") or hasattr(arrow, "index"):
                    return None

                return str(arrow.name)

        return None

    def _configuration_factor_key(self, factor: Any) -> str | None:
        try:
            factor = self.Q.normalize_mp_input(factor)
        except Exception:
            pass

        if isinstance(factor, self.MasseyProduct):
            inputs = tuple(getattr(factor, "inputs", ()) or ())

            if len(inputs) == 1:
                return self._configuration_factor_key(inputs[0])

        try:
            key = self.Q.mp_factor_key(factor)
        except Exception:
            try:
                key = self.Q.mp_key(*tuple(getattr(factor, "inputs", ()) or ()))
            except Exception:
                key = repr(factor)

        return f"factor:{repr(key)}"

    def _configuration_factor_record(self, factor: Any) -> dict[str, Any] | None:
        try:
            factor = self.Q.normalize_mp_input(factor)
        except Exception:
            pass

        if isinstance(factor, self.MasseyProduct):
            inputs = tuple(getattr(factor, "inputs", ()) or ())

            if len(inputs) == 1:
                return self._configuration_factor_record(inputs[0])

            key = self._configuration_factor_key(factor)

            if not key:
                return None

            return {
                "name": key,
                "label": self._format_mp_factor(factor),
                "kind": "massey",
                "arity": len(inputs),
                "source": str(getattr(factor, "source", "")),
                "target": str(getattr(factor, "target", "")),
                "spec": self._factor_spec(factor),
                "inputs": [
                    self._configuration_factor_record(item)
                    for item in inputs
                ],
            }

        if isinstance(factor, self.Arrow):
            if hasattr(factor, "cell_prefix") or hasattr(factor, "index"):
                return None

            key = self._configuration_factor_key(factor)

            if not key:
                return None

            return {
                "name": key,
                "label": str(factor.name),
                "kind": "generator",
                "source": str(getattr(factor, "source", "")),
                "target": str(getattr(factor, "target", "")),
                "spec": self._factor_spec(factor),
            }

        if isinstance(factor, self.Path):
            if len(factor.arrows) == 1:
                arrow = factor.arrows[0]

                if isinstance(arrow, self.Arrow):
                    return self._configuration_factor_record(arrow)

            key = self._configuration_factor_key(factor)

            if not key:
                return None

            return {
                "name": key,
                "label": self._format_mp_input_atom(factor),
                "kind": "path",
                "source": str(getattr(factor, "source", "")),
                "target": str(getattr(factor, "target", "")),
                "spec": self._factor_spec(factor),
            }

        return None

    def _configuration_window_record(
        self,
        factors: tuple[Any, ...],
        level: int,
    ) -> dict[str, Any] | None:
        records = [
            self._configuration_factor_record(factor)
            for factor in factors
        ]

        if any(record is None for record in records):
            return None

        labels = [str(record["label"]) for record in records if record is not None]
        key_parts = [str(record["name"]) for record in records if record is not None]

        return {
            "name": f"window:{level}:{'|'.join(key_parts)}",
            "label": "(" + ", ".join(labels) + ")",
            "kind": "window",
            "level": level,
            "source": str(getattr(factors[0], "source", "")) if factors else "",
            "target": str(getattr(factors[-1], "target", "")) if factors else "",
            "spec": {
                "type": "window",
                "level": level,
                "inputs": [
                    self._factor_spec(factor)
                    for factor in factors
                ],
            },
            "inputs": records,
        }

    def _configuration_resolution_record(self, block: dict[str, Any]) -> dict[str, Any]:
        resolution = block.get("resolution", {})

        if not isinstance(resolution, dict):
            resolution = {}

        primitive = resolution.get("raw_primitive", None)

        if primitive is None:
            primitive = resolution.get("primitive", None)

        if primitive is None:
            if resolution.get("virtual_zero"):
                primitive_label = "virtual zero"
            elif resolution.get("virtual_primitive"):
                primitive_label = "virtual primitive"
            else:
                primitive_label = ""
        else:
            primitive_label = self._safe_str(primitive)

        stasheff_terms = []

        for term in tuple(resolution.get("stasheff_terms", ()) or ()):
            if not isinstance(term, dict):
                continue

            term_record = {
                "coefficient": self._safe_str(term.get("coefficient")),
                "span": list(term.get("span", ()) or ()),
                "innerArity": term.get("inner_arity"),
                "outerArity": term.get("outer_arity"),
            }
            outer_inputs = tuple(term.get("outer_inputs", ()) or ())

            if outer_inputs:
                term_record["outer"] = self._format_product(outer_inputs)

            stasheff_terms.append(term_record)

        return {
            "source": str(block.get("source") or resolution.get("source") or ""),
            "primitive": primitive_label,
            "coefficient": self._safe_str(resolution.get("coefficient", "")),
            "verified": bool(resolution.get("verified", False)),
            "virtual": bool(
                resolution.get("virtual_primitive")
                or resolution.get("virtual_zero")
            ),
            "virtualZero": bool(resolution.get("virtual_zero", False)),
            "reason": self._safe_str(resolution.get("reason", "")),
            "stasheffTerms": stasheff_terms,
        }

    def _configuration_cycle_key(self, names: tuple[str, ...]) -> tuple[str, ...]:
        rotations = [
            names[index:] + names[:index]
            for index in range(len(names))
        ]

        return min(rotations)

    def _configuration_cycles_from_edges(
        self,
        edges_by_pair: dict[tuple[str, str], dict[str, Any]],
        *,
        level: int,
        kind: str,
        max_cycles: int,
        max_path_length: int,
    ) -> tuple[list[dict[str, Any]], bool]:
        adjacency: dict[str, list[str]] = {}

        for source, target in sorted(edges_by_pair.keys()):
            if source == target:
                continue

            adjacency.setdefault(source, []).append(target)

        cycles: list[tuple[str, ...]] = []
        seen_cycles: set[tuple[str, ...]] = set()

        for start in sorted(adjacency.keys()):
            stack: list[tuple[str, list[str]]] = [(start, [start])]

            while stack and len(cycles) < max_cycles:
                current, path = stack.pop()

                for target in sorted(adjacency.get(current, ()), reverse=True):
                    if target == start and len(path) >= 3:
                        cycle = tuple(path)
                        key = self._configuration_cycle_key(cycle)

                        if key not in seen_cycles:
                            seen_cycles.add(key)
                            cycles.append(key)

                        continue

                    if target in path:
                        continue

                    if len(path) >= max_path_length:
                        continue

                    stack.append((target, path + [target]))

        cycle_records = []

        for index, cycle in enumerate(cycles, start=1):
            edge_records = []

            for source, target in zip(cycle, cycle[1:] + cycle[:1]):
                edge_records.append(edges_by_pair[(source, target)])

            nodes = [
                edges_by_pair[(source, target)]["sourceNode"]
                for source, target in zip(cycle, cycle[1:] + cycle[:1])
            ]

            cycle_records.append({
                "id": f"configuration-level-{level}-{kind}-{index}",
                "number": index,
                "cycleNumber": index,
                "label": " -> ".join(
                    str(node["label"])
                    for node in nodes + nodes[:1]
                ),
                "level": level,
                "kind": kind,
                "nodes": nodes,
                "edges": edge_records,
            })

        return cycle_records, len(seen_cycles) >= max_cycles

    def _serialize_configuration_graph(self) -> dict[str, Any]:
        edges_by_pair: dict[tuple[str, str], dict[str, Any]] = {}

        def tower_resolved_product_blocks(base_blocks: Any) -> tuple[dict[str, Any], ...]:
            try:
                records = tuple(
                    self.Q.completed_massey_tower_elimination_records(record=False)
                    or ()
                )
            except Exception:
                records = ()

            if not records:
                return ()

            factors_by_key: dict[str, Any] = {}

            def factor_lookup_key(factor: Any) -> str | None:
                try:
                    return repr(self.Q.mp_factor_key(factor))
                except Exception:
                    try:
                        return repr(self.Q.mp_key(*tuple(getattr(factor, "inputs", ()) or ())))
                    except Exception:
                        return repr(factor)

            def remember_factor(factor: Any) -> None:
                try:
                    factor = self.Q.normalize_mp_input(factor)
                except Exception:
                    pass

                record = self._configuration_factor_record(factor)

                if record is None:
                    return

                if record.get("kind") == "massey":
                    return

                key = factor_lookup_key(factor)

                if key:
                    factors_by_key.setdefault(key, factor)

            for block in tuple(base_blocks or ()):
                if not isinstance(block, dict):
                    continue

                for factor in tuple(block.get("factors", ()) or ()):
                    remember_factor(factor)

            for record in records:
                if not isinstance(record, dict):
                    continue

                for factor in tuple(record.get("seed_inputs", ()) or ()):
                    remember_factor(factor)

                for factor in tuple(record.get("aliases", ()) or ()):
                    remember_factor(factor)

            factors = tuple(factors_by_key.values())
            blocks = []
            seen = set()

            for left in factors:
                for right in factors:
                    try:
                        product_factors = tuple(self.Q.canonical_mp_factors((left, right)))
                    except Exception:
                        product_factors = (left, right)

                    if len(product_factors) != 2:
                        continue

                    try:
                        if not self.Q.mp_factors_composable(product_factors, cyclic=False):
                            continue
                    except Exception:
                        continue

                    try:
                        report = self.Q.tower_elimination_report(
                            *product_factors,
                            records=records,
                        )
                    except Exception:
                        report = None

                    if report is None:
                        continue

                    key = tuple(factor_lookup_key(factor) for factor in product_factors)

                    if key in seen:
                        continue

                    seen.add(key)
                    blocks.append({
                        "factors": product_factors,
                        "key": key,
                        "source": "completed_massey_tower",
                        "resolution": {
                            "resolved": True,
                            "virtual_primitive": True,
                            "source": "completed_massey_tower",
                            "reason": "tower elimination",
                            "tower_report": report,
                            "record": report.get("record"),
                            "flat_word": tuple(report.get("flat_word", ())),
                            "seed_inputs": tuple(report.get("seed_inputs", ())),
                        },
                    })

            return tuple(blocks)

        try:
            blocks = tuple(self.Q.known_resolved_product_blocks() or ())
        except Exception:
            blocks = ()

        blocks = blocks + tower_resolved_product_blocks(blocks)

        for block in blocks:
            if not isinstance(block, dict):
                continue

            factors = tuple(block.get("factors", ()) or ())

            if len(factors) != 2:
                continue

            source_node = self._configuration_factor_record(factors[0])
            target_node = self._configuration_factor_record(factors[1])

            if not source_node or not target_node:
                continue

            source = str(source_node["name"])
            target = str(target_node["name"])

            pair = (source, target)
            resolution = self._configuration_resolution_record(block)

            if pair not in edges_by_pair:
                edges_by_pair[pair] = {
                    "id": f"resolved-product:{source}->{target}",
                    "source": source,
                    "target": target,
                    "label": self._format_product(factors),
                    "kind": "resolved_product",
                    "level": 1,
                    "sourceType": str(block.get("source", "")),
                    "sourceTypes": [],
                    "factors": [self._factor_spec(factor) for factor in factors],
                    "sourceNode": source_node,
                    "targetNode": target_node,
                    "primitives": [],
                }

            edge = edges_by_pair[pair]
            source_type = str(block.get("source", ""))

            if source_type and source_type not in edge["sourceTypes"]:
                edge["sourceTypes"].append(source_type)

            primitive_key = (
                resolution.get("source"),
                resolution.get("primitive"),
                resolution.get("coefficient"),
                resolution.get("virtual"),
            )
            seen_primitives = {
                (
                    item.get("source"),
                    item.get("primitive"),
                    item.get("coefficient"),
                    item.get("virtual"),
                )
                for item in edge["primitives"]
            }

            if primitive_key not in seen_primitives:
                edge["primitives"].append(resolution)

        product_polygons, product_truncated = self._configuration_cycles_from_edges(
            edges_by_pair,
            level=1,
            kind="resolved_product",
            max_cycles=80,
            max_path_length=10,
        )

        elevated_polygons: list[dict[str, Any]] = []
        elevated_edges_by_level: dict[int, dict[tuple[str, str], dict[str, Any]]] = {}

        massey_items = []

        try:
            massey_items.extend(getattr(self.Q, "massey_products", {}).values())
        except Exception:
            pass

        try:
            massey_items.extend(getattr(self.Q, "generated_massey_products", ()) or ())
        except Exception:
            pass

        seen_massey_keys = set()

        for item in massey_items:
            if not isinstance(item, self.MasseyProduct):
                continue

            inputs = tuple(getattr(item, "inputs", ()) or ())

            if len(inputs) < 3:
                continue

            normalized_inputs = []

            try:
                normalized_inputs = list(self.Q.normalize_mp_inputs(inputs))
            except Exception:
                normalized_inputs = list(inputs)

            if any(
                self._configuration_factor_record(input_item) is None
                for input_item in normalized_inputs
            ):
                continue

            level = len(normalized_inputs) - 1

            if level < 2:
                continue

            try:
                massey_key = self.Q.mp_key(*normalized_inputs)
            except Exception:
                massey_key = tuple(repr(input_item) for input_item in normalized_inputs)

            if massey_key in seen_massey_keys:
                continue

            seen_massey_keys.add(massey_key)
            source_node = self._configuration_window_record(
                tuple(normalized_inputs[:level]),
                level,
            )
            target_node = self._configuration_window_record(
                tuple(normalized_inputs[1:]),
                level,
            )

            if not source_node or not target_node:
                continue

            source = str(source_node["name"])
            target = str(target_node["name"])
            level_edges = elevated_edges_by_level.setdefault(level, {})
            pair = (source, target)

            if pair in level_edges:
                continue

            level_edges[pair] = {
                "id": f"elevated:{level}:{source}->{target}",
                "source": source,
                "target": target,
                "label": self._format_mp_factor(item),
                "kind": "elevated_massey",
                "level": level,
                "sourceType": "defined_massey_product",
                "sourceTypes": ["defined_massey_product"],
                "factors": [self._factor_spec(item)],
                "sourceNode": source_node,
                "targetNode": target_node,
                "massey": {
                    "label": self._format_mp_factor(item),
                    "arity": len(normalized_inputs),
                    "inputs": [
                        self._factor_spec(input_item)
                        for input_item in normalized_inputs
                    ],
                },
                "primitives": [],
            }

        elevated_truncated = False

        for level, level_edges in sorted(elevated_edges_by_level.items()):
            level_polygons, level_truncated = self._configuration_cycles_from_edges(
                level_edges,
                level=level,
                kind="elevated_massey",
                max_cycles=80,
                max_path_length=12,
            )
            elevated_polygons.extend(level_polygons)
            elevated_truncated = elevated_truncated or level_truncated

        polygons = product_polygons + elevated_polygons
        all_edges = list(edges_by_pair.values())

        for level_edges in elevated_edges_by_level.values():
            all_edges.extend(level_edges.values())

        levels = []

        for level in sorted({int(item.get("level", 1)) for item in polygons} | {1}):
            level_polygons = [
                polygon
                for polygon in polygons
                if int(polygon.get("level", 1)) == level
            ]
            level_edges = [
                edge
                for edge in all_edges
                if int(edge.get("level", 1)) == level
            ]

            levels.append({
                "level": level,
                "label": "Level 1 products" if level == 1 else f"Level {level} m{level + 1}",
                "polygonCount": len(level_polygons),
                "cycleCount": len(level_polygons),
                "edgeCount": len(level_edges),
            })

        return {
            "polygons": polygons,
            "circles": polygons,
            "edges": all_edges,
            "levels": levels,
            "edgeCount": len(all_edges),
            "truncated": product_truncated or elevated_truncated,
        }

    def _generated_equivalence_depth_limit(self) -> int:
        value = self.computation_settings.get("bridgeReplacementMaxDepth")

        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return 4

    def _generated_presentation_score(self, factors: Any) -> tuple[int, int, int, str]:
        factors = tuple(factors or ())

        def nested_massey_count(item: Any) -> int:
            if isinstance(item, self.MasseyProduct):
                return 1 + sum(nested_massey_count(part) for part in item.inputs)

            return 0

        label = self._format_product(factors)
        return (
            sum(nested_massey_count(factor) for factor in factors),
            len(label),
            len(factors),
            label,
        )

    def _simplest_equivalent_massey_inputs(self, item: Any) -> tuple[Any, ...]:
        if not isinstance(item, self.MasseyProduct):
            return ()

        try:
            start = tuple(self.Q.canonical_mp_factors(tuple(item.inputs)))
        except Exception:
            return tuple(item.inputs)

        include_ainf = bool(
            self.computation_settings.get("includePrimitiveDetails")
        ) and not bool(self.computation_settings.get("disableMasseyFormula"))

        try:
            relations = self.Q.mp_presentation_replacement_relations(
                include_bridge=True,
                include_ainf=include_ainf,
                include_self_expanding=True,
            )
        except Exception:
            relations = ()

        max_depth = self._generated_equivalence_depth_limit()
        state_limit = 200
        queue: list[tuple[tuple[Any, ...], int]] = [(start, 0)]
        seen = {repr(self._generation_factor_tuple_key(start))}
        best = start
        best_score = self._generated_presentation_score(start)
        checked = 0

        while queue and checked < state_limit:
            word, depth = queue.pop(0)
            checked += 1

            if len(word) >= 3:
                try:
                    composable = self.Q.mp_factors_composable(word, cyclic=False)
                except Exception:
                    composable = False

                if composable:
                    score = self._generated_presentation_score(word)

                    if score < best_score:
                        best = word
                        best_score = score

            if depth >= max_depth:
                continue

            try:
                neighbors = self.Q.linear_replacement_neighbors(
                    word,
                    relations=relations,
                )
            except Exception:
                neighbors = ()

            for neighbor in tuple(neighbors or ()):
                try:
                    neighbor = tuple(self.Q.canonical_mp_factors(neighbor))
                except Exception:
                    continue

                key = repr(self._generation_factor_tuple_key(neighbor))

                if key in seen:
                    continue

                seen.add(key)
                queue.append((neighbor, depth + 1))

        return best

    def _generation_factor_tuple_key(self, factors: Any) -> Any:
        try:
            return self.Q.mp_factor_tuple_key(tuple(factors or ()))
        except Exception:
            return tuple(repr(factor) for factor in tuple(factors or ()))

    def _generated_product_equivalence_label(self, inputs: Any) -> str | None:
        inputs = tuple(inputs or ())

        if len(inputs) < 3:
            return None

        try:
            M = self.Q.mp(*inputs)
        except Exception:
            M = None

        if not isinstance(M, self.MasseyProduct):
            return None

        start = (M,)
        start_key = repr(self._generation_factor_tuple_key(start))
        include_ainf = bool(
            self.computation_settings.get("includePrimitiveDetails")
        ) and not bool(self.computation_settings.get("disableMasseyFormula"))

        try:
            relations = self.Q.product_replacement_relations(include_ainf=include_ainf)
        except Exception:
            relations = ()

        max_depth = self._generated_equivalence_depth_limit()
        state_limit = 100
        queue: list[tuple[tuple[Any, ...], int]] = [(start, 0)]
        seen = {start_key}
        start_score = self._generated_presentation_score(start)
        best: tuple[Any, ...] | None = None
        best_score: tuple[int, int, int, str] | None = None
        checked = 0

        while queue and checked < state_limit:
            word, depth = queue.pop(0)
            checked += 1

            if depth > 0:
                score = self._generated_presentation_score(word)

                if score < start_score and (best_score is None or score < best_score):
                    best = word
                    best_score = score

            if depth >= max_depth:
                continue

            try:
                neighbors = self.Q.linear_replacement_neighbors(
                    word,
                    relations=relations,
                )
            except Exception:
                neighbors = ()

            for neighbor in tuple(neighbors or ()):
                try:
                    neighbor = tuple(self.Q.canonical_mp_factors(neighbor))
                except Exception:
                    continue

                key = repr(self._generation_factor_tuple_key(neighbor))

                if key in seen:
                    continue

                seen.add(key)
                queue.append((neighbor, depth + 1))

        if best is None:
            return None

        return self._format_product(best)

    def _generated_massey_slide_class_key(self, inputs: Any) -> str | None:
        inputs = tuple(inputs or ())

        if len(inputs) < 3:
            return None

        try:
            flat_word = tuple(self.Q.canonical_mp_factors(inputs))
        except Exception:
            return None

        try:
            flat_key = self._generation_factor_tuple_key(flat_word)
        except Exception:
            flat_key = tuple(repr(factor) for factor in flat_word)

        return repr((
            "massey-slide-class",
            len(inputs),
            flat_key,
        ))

    def _generated_display_records(self) -> list[dict[str, Any]]:
        raw_records = []

        for item in getattr(self.Q, "generated_massey_products", []):
            if not isinstance(item, self.MasseyProduct):
                continue

            try:
                if self.Q.generated_massey_inputs_have_zero_product_input(tuple(item.inputs)):
                    continue
            except Exception:
                pass

            try:
                if self.Q.generated_massey_inputs_are_product_multiple(tuple(item.inputs)):
                    continue
            except Exception:
                pass

            has_product_input = any(
                isinstance(input_item, self.MPProduct)
                for input_item in tuple(item.inputs)
            )
            representative_inputs = (
                tuple(item.inputs)
                if has_product_input
                else self._simplest_equivalent_massey_inputs(item)
            )

            try:
                if has_product_input:
                    representative_key = (
                        self._generated_massey_slide_class_key(tuple(item.inputs))
                    )
                else:
                    representative_key = repr(self.Q.mp_key(*representative_inputs))
            except Exception:
                representative_key = repr(self._generation_factor_tuple_key(representative_inputs))

            if representative_key is None:
                try:
                    representative_key = repr(self.Q.mp_key(*representative_inputs))
                except Exception:
                    representative_key = repr(
                        self._generation_factor_tuple_key(representative_inputs)
                    )

            try:
                item_key = repr(self.Q.mp_key(*tuple(item.inputs)))
            except Exception:
                item_key = self._generation_item_key(item)

            raw_records.append({
                "item": item,
                "item_key": item_key,
                "representative_inputs": representative_inputs,
                "representative_key": representative_key,
                "is_representative": item_key == representative_key,
                "score": self._generated_presentation_score(tuple(item.inputs)),
                "label": str(item),
            })

        grouped: dict[str, list[dict[str, Any]]] = {}

        for record in raw_records:
            grouped.setdefault(record["representative_key"], []).append(record)

        display_records = []

        for group in grouped.values():
            chosen = min(
                group,
                key=lambda record: (
                    not record["is_representative"],
                    record["score"],
                    record["label"],
                ),
            )
            hidden_records = sorted(
                (
                    record
                    for record in group
                    if record is not chosen
                ),
                key=lambda record: (record["score"], record["label"]),
            )
            hidden_count = len(group) - 1
            equivalent_label = self._generated_product_equivalence_label(
                chosen["representative_inputs"],
            )
            chosen = dict(chosen)
            chosen["hidden_equivalent_count"] = hidden_count
            chosen["hidden_equivalent_presentations"] = hidden_records
            chosen["equivalent_label"] = equivalent_label
            display_records.append(chosen)

        return display_records

    def _generated_item_has_bridge_promoted_only_resolution(self, item: Any) -> bool:
        if not isinstance(item, self.MasseyProduct):
            return False

        inputs = tuple(getattr(item, "inputs", ()) or ())

        if len(inputs) < 3:
            return False

        try:
            with self._computation_context(include_primitive_details=False):
                report, _ = capture_output(
                    self.Q.pure_massey_cyclic_class_report,
                    item,
                    record=False,
                    search_bridge_resolvers=False,
                )
        except Exception:
            return False

        return bool(report.get("self_resolution_is_bridge_promoted_only"))

    def _serialize_generated(self) -> dict[str, Any]:
        items = []
        visible_keys = set()
        have_keys, no_obvious_keys = self._last_generation_key_sets()

        for display_record in self._generated_display_records():
            item = display_record["item"]

            key = self.Q.mp_key(*item.inputs)
            visible_keys.add(repr(key))
            generation_key = self._generation_item_key(item)
            resolved = key in getattr(self.Q, "resolved_massey_products", {})
            bridge_promoted_only = False

            if resolved:
                bridge_promoted_only = (
                    self._generated_item_has_bridge_promoted_only_resolution(item)
                )

                if bridge_promoted_only:
                    resolved = False

            equivalent_label = display_record.get("equivalent_label")

            if (
                not resolved
                and not getattr(self.Q, "skip_deep_tower_resolution", False)
            ):
                try:
                    if self.Q.is_tower_eliminated_mp(tuple(item.inputs)):
                        continue
                except Exception:
                    pass

            status = "resolved" if resolved else "generated"
            primitive_record = self._primitive_record_for_generated_item(
                item,
                key,
                generation_key,
            )

            if equivalent_label and not resolved:
                status = "equivalent"
            elif not resolved and generation_key in have_keys:
                status = "have_primitives"
            elif not resolved and generation_key in no_obvious_keys:
                status = "no_obvious_primitives"
            elif not resolved:
                if primitive_record is None:
                    primitive_record = self._display_primitive_record_for_generated_item(item)

                primitive_status = self._primitive_status_from_record(primitive_record)

                if primitive_status is not None:
                    status = primitive_status

            spec = self._factor_spec(item)
            expression_inputs = [self._factor_spec(x) for x in item.inputs]
            can_resolve = (
                not resolved
                and not equivalent_label
                and not self._spec_contains_zero(spec)
            )
            primitive_info = self._generated_primitive_info(
                item,
                key,
                generation_key,
                primitive_record=primitive_record,
            )
            equivalence_note = None

            if equivalent_label:
                equivalence_note = f"equivalent to {equivalent_label}"

            hidden_count = int(display_record.get("hidden_equivalent_count") or 0)
            hidden_presentations = []

            for hidden_record in display_record.get("hidden_equivalent_presentations", []):
                hidden_item = hidden_record.get("item")

                if not isinstance(hidden_item, self.MasseyProduct):
                    continue

                hidden_inputs = tuple(hidden_item.inputs)
                hidden_presentations.append({
                    "label": str(hidden_item),
                    "shortLabel": self._format_inputs(hidden_inputs),
                    "arity": len(hidden_inputs),
                    "source": hidden_item.source,
                    "target": hidden_item.target,
                    "expression": {
                        "type": "massey",
                        "inputs": [
                            self._factor_spec(input_item)
                            for input_item in hidden_inputs
                        ],
                    },
                })

            items.append({
                "label": str(item),
                "shortLabel": self._format_inputs(item.inputs),
                "arity": len(item.inputs),
                "source": item.source,
                "target": item.target,
                "resolved": resolved,
                "status": status,
                "canResolve": can_resolve,
                "spec": spec,
                "expression": {
                    "type": "massey",
                    "inputs": expression_inputs,
                },
                "primitiveInfo": primitive_info,
                "equivalence": {
                    "equivalentTo": equivalent_label,
                    "note": equivalence_note,
                    "hiddenEquivalentCount": hidden_count,
                    "hiddenPresentations": hidden_presentations,
                    "bridgePromotedOnly": bridge_promoted_only,
                },
                "equivalenceNote": equivalence_note,
            })

        self._append_pure_search_generated_item(items, visible_keys)
        items.sort(key=lambda row: (row["resolved"], row["arity"], row["label"]))
        return {
            "items": items,
            "pureClasses": self._cached_pure_classes_payload(),
        }

    def _append_pure_search_generated_item(
        self,
        items: list[dict[str, Any]],
        visible_keys: set[str],
    ) -> None:
        if not self.last_run:
            return

        report = self.last_run.get("report", {})

        if not isinstance(report, dict):
            return

        pure_search = report.get("pure_search_result")

        if not isinstance(pure_search, dict) or not pure_search.get("found"):
            return

        search_report = pure_search.get("report")

        if not isinstance(search_report, dict):
            search_report = {}

        inputs = tuple(
            pure_search.get("inputs")
            or search_report.get("inputs")
            or ()
        )

        if not inputs:
            return

        try:
            normalized_inputs = tuple(self.Q.normalize_mp_inputs(inputs))
            key = self.Q.mp_key(*normalized_inputs)
        except Exception:
            normalized_inputs = inputs
            key = tuple(repr(item) for item in normalized_inputs)

        if repr(key) in visible_keys:
            return

        item = search_report.get("massey_product")

        if not isinstance(item, self.MasseyProduct):
            try:
                item = self.Q.mp(*normalized_inputs)
            except Exception:
                item = None

        if not isinstance(item, self.MasseyProduct):
            return

        spec = self._factor_spec(item)
        expression_inputs = [self._factor_spec(x) for x in normalized_inputs]
        resolved = bool(search_report.get("resolved")) or key in getattr(
            self.Q,
            "resolved_massey_products",
            {},
        )
        status = (
            "likely_over"
            if pure_search.get("status") == "likely_over"
            else "pure_search"
        )

        items.append({
            "label": str(item),
            "shortLabel": self._format_inputs(normalized_inputs),
            "arity": len(normalized_inputs),
            "source": item.source,
            "target": item.target,
            "resolved": resolved,
            "status": status,
            "canResolve": (
                not resolved
                and not self._spec_contains_zero(spec)
            ),
            "spec": spec,
            "expression": {
                "type": "massey",
                "inputs": expression_inputs,
            },
            "primitiveInfo": None,
            "equivalence": {
                "equivalentTo": None,
                "note": None,
                "hiddenEquivalentCount": 0,
                "hiddenPresentations": [],
            },
            "equivalenceNote": "found by pure search",
        })

    def _display_primitive_record_for_generated_item(self, item: Any) -> dict[str, Any] | None:
        if not isinstance(item, self.MasseyProduct):
            return None

        try:
            with self._computation_context(include_primitive_details=False):
                record, _ = capture_output(
                    self.Q.classify_massey_product_primitives,
                    item,
                    record=False,
                    minimal_only=True,
                    include_primitive_details=False,
                )
        except Exception:
            return None

        return record if isinstance(record, dict) else None

    def _primitive_status_from_record(self, record: Any) -> str | None:
        if not isinstance(record, dict):
            return None

        if record.get("has_obvious_primitive"):
            return "have_primitives"

        if "has_obvious_primitive" in record:
            return "no_obvious_primitives"

        return None

    def _generated_primitive_info(
        self,
        item: Any,
        mp_key: Any,
        generation_key: str,
        primitive_record: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        record = (
            primitive_record
            if primitive_record is not None
            else self._primitive_record_for_generated_item(
                item,
                mp_key,
                generation_key,
            )
        )

        if not isinstance(record, dict):
            return {
                "terminationCount": 0,
                "multipleTerminationBlocks": 0,
                "unsettledPairCount": 0,
                "unsettled": False,
                "terminations": [],
            }

        termination_labels: dict[str, None] = {}
        multiple_blocks = 0
        unsettled_pairs = record.get("unsettled_termination_pairs", []) or []

        for candidate in record.get("candidate_summaries", []) or []:
            if not isinstance(candidate, dict):
                continue

            local_labels: set[str] = set()

            for termination in candidate.get("terminations", []) or []:
                label = self._termination_summary_label(termination)

                if not label:
                    continue

                termination_labels.setdefault(label, None)
                local_labels.add(label)

            if len(local_labels) >= 2:
                multiple_blocks += 1

        labels = list(termination_labels.keys())
        return {
            "terminationCount": len(labels),
            "multipleTerminationBlocks": multiple_blocks,
            "unsettledPairCount": len(unsettled_pairs),
            "unsettled": bool(unsettled_pairs) or bool(multiple_blocks),
            "terminations": labels[:6],
        }

    def _primitive_record_for_generated_item(
        self,
        item: Any,
        mp_key: Any,
        generation_key: str,
    ) -> dict[str, Any] | None:
        if not isinstance(self.last_generation, dict):
            return None

        primitive_data = self.last_generation.get("primitive_data", {})

        if not isinstance(primitive_data, dict):
            return None

        lookup_keys = [mp_key, generation_key, repr(mp_key)]

        try:
            lookup_keys.append(self.Q.generation_item_key(item))
        except Exception:
            pass

        for lookup_key in lookup_keys:
            try:
                if lookup_key in primitive_data:
                    return primitive_data[lookup_key]
            except TypeError:
                continue

        return None

    def _termination_summary_label(self, termination: Any) -> str:
        if not isinstance(termination, dict):
            return str(termination)

        cell = str(termination.get("cell") or "").strip()
        expression = str(termination.get("expression") or "").strip()
        source = str(termination.get("source") or "").strip()
        path_key = termination.get("path_key") or ()

        if cell:
            label = cell
        elif expression:
            label = expression
        elif path_key:
            label = "path " + ".".join(str(part) for part in path_key)
        else:
            label = "terminal cell"

        if source:
            label = f"{label} ({source})"

        return label

    def _last_generation_key_sets(self) -> tuple[set[str], set[str]]:
        have = set()
        no_obvious = set()

        if not isinstance(self.last_generation, dict):
            return have, no_obvious

        for item in self.last_generation.get("have_primitives", []):
            have.add(self._generation_item_key(item))

        for item in self.last_generation.get("no_obvious_primitives", []):
            no_obvious.add(self._generation_item_key(item))

        return have, no_obvious

    def _generation_item_key(self, item: Any) -> str:
        try:
            key = self.Q.generation_item_key(item)
        except Exception:
            try:
                key = self.Q.mp_key(*item.inputs)
            except Exception:
                key = repr(item)

        return repr(key)

    def _serialize_pure_classes(self, record: bool = False) -> dict[str, Any]:
        try:
            with self._computation_context(include_primitive_details=False):
                result, _ = capture_output(
                    self.Q.generated_pure_massey_cyclic_class_reports,
                    unresolved_only=False,
                    record=record,
                )
        except Exception:
            return empty_pure_classes_payload(dirty=True)

        return self._serialize_pure_class_result(result, dirty=False)

    def _cached_pure_classes_payload(self) -> dict[str, Any]:
        return json.loads(json.dumps(
            self.last_pure_classes or empty_pure_classes_payload(dirty=True),
        ))

    def _serialize_pure_class_result(
        self,
        result: dict[str, Any],
        dirty: bool = False,
    ) -> dict[str, Any]:
        def convert(entry: dict[str, Any]) -> dict[str, Any]:
            inputs = tuple(entry.get("inputs", ()))
            return {
                "label": self._format_inputs(inputs),
                "arity": entry.get("arity", len(inputs)),
                "resolved": bool(entry.get("resolved")),
                "likelyOver": bool(entry.get("likely_over")),
                "cyclicallyZero": bool(
                    entry.get("cyclically_zero")
                    or entry.get("report", {}).get("cyclically_zero")
                ),
                "isolated": bool(entry.get("isolated")),
                "nonIsolated": bool(entry.get("non_isolated")),
                "choiceInputs": [self._factor_spec(x) for x in inputs],
                "expression": {
                    "type": "massey",
                    "inputs": [self._factor_spec(x) for x in inputs],
                },
            }

        classes = [convert(entry) for entry in result.get("classes", [])]
        unresolved = [convert(entry) for entry in result.get("unresolved_classes", [])]
        likely_over = [convert(entry) for entry in result.get("likely_over_classes", [])]
        return {
            "won": bool(result.get("won")),
            "sourceCount": result.get("source_count", 0),
            "classes": classes,
            "unresolved": unresolved,
            "likelyOver": likely_over,
            "dirty": dirty,
        }

    def _serialize_attachments(self) -> list[dict[str, Any]]:
        rows = []

        for index, entry in enumerate(getattr(self.Q, "attachment_history", []), start=1):
            expression = entry.get("expression")
            cell = entry.get("cell")
            kind = entry.get("kind", "cell")
            rows.append({
                "index": index,
                "kind": kind,
                "cell": str(cell) if cell is not None else "",
                "expression": self._safe_str(expression),
                "expressionSpec": self._expression_spec(expression),
                "expressionDisplay": self._format_mp_expression_display(expression),
                "differential": self._safe_str(entry.get("differential")),
                "differentialSpec": self._expression_spec(entry.get("differential")),
                "differentialDisplay": self._format_mp_expression_display(entry.get("differential")),
                "differentialPresentation": self._format_attachment_differential(
                    kind,
                    expression,
                    entry.get("differential"),
                ),
                "resolved": kind in {"mp_cell", "mp_expression_cell", "bridge", "ordinary_cell"},
            })

        return rows

    def _expression_spec(self, expression: Any) -> dict[str, Any] | None:
        if expression is None:
            return None

        if self._is_zero_factor(expression):
            return {
                "type": "zero",
                "value": 0,
                "label": "0",
            }

        if isinstance(expression, self.MasseyProduct):
            return {
                "type": "massey",
                "inputs": [self._factor_spec(x) for x in expression.inputs],
            }

        if isinstance(expression, self.MPProduct):
            return {
                "type": "product",
                "coefficient": "1",
                "factors": [self._factor_spec(factor) for factor in expression.factors],
            }

        if isinstance(expression, self.MPElement):
            terms = []

            for product, coeff in expression.terms.items():
                sign = -1 if str(coeff).startswith("-") else 1
                coeff_text = str(coeff)

                if coeff_text in {"1", "-1"}:
                    coefficient = "1"
                elif coeff_text.startswith("-"):
                    coefficient = coeff_text[1:]
                else:
                    coefficient = coeff_text

                if isinstance(product, self.MPProduct):
                    terms.append({
                        "sign": sign,
                        "coefficient": coefficient,
                        "product": {
                            "type": "product",
                            "coefficient": "1",
                            "factors": [
                                self._factor_spec(factor)
                                for factor in product.factors
                            ],
                        },
                    })

            if terms:
                return {
                    "type": "sum",
                    "terms": terms,
                }

        return None

    def _serialize_bridge_products(self) -> list[dict[str, Any]]:
        rows = []

        for key in getattr(self.Q, "bridge_history", []):
            expression = self.Q.bridge_expressions.get(key)
            rows.append({
                "label": self._format_mp_expression_display(expression),
                "cell": self._safe_str(self.Q.bridge_cells.get(key)),
            })

        return rows

    def primitive_graph(self) -> dict[str, Any]:
        with self.lock:
            return self._serialize_primitive_graph()

    def cyclic_class_graph(self) -> dict[str, Any]:
        with self.lock:
            return self._serialize_cyclic_class_graph()

    def _serialize_primitive_graph(self) -> dict[str, Any]:
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []
        seen_edges: set[tuple[str, str, str, str]] = set()
        cell_label_to_id: dict[str, str] = {}
        cell_id_by_mp_key: dict[str, str] = {}
        cell_id_by_block_key: dict[str, str] = {}

        def add_node(
            node_id: str,
            kind: str,
            label: str,
            detail: str = "",
            **extra: Any,
        ) -> str:
            if not node_id:
                node_id = f"{kind}:{len(nodes) + 1}"

            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "kind": kind,
                    "label": label or node_id,
                    "mathLabel": extra.pop("mathLabel", None) or self._math_from_display_label(label),
                    "detail": detail,
                    **extra,
                }
            else:
                node = nodes[node_id]
                if not node.get("detail") and detail:
                    node["detail"] = detail

                node.update({
                    key: value
                    for key, value in extra.items()
                    if value not in (None, "", [])
                })

            return node_id

        def add_edge(
            source: str,
            target: str,
            kind: str,
            label: str = "",
            **extra: Any,
        ) -> None:
            if not source or not target or source == target:
                return

            key = (source, target, kind, label)

            if key in seen_edges:
                return

            seen_edges.add(key)
            edges.append({
                "source": source,
                "target": target,
                "kind": kind,
                "label": label,
                **extra,
            })

        def presentation_id(label: str) -> str:
            return "presentation:" + label

        def add_presentation(
            label: str,
            detail: str = "",
            math_label: str | None = None,
        ) -> str:
            return add_node(
                presentation_id(label),
                "presentation",
                label,
                detail,
                mathLabel=math_label,
            )

        attachment_rows = self._serialize_attachments()
        attachment_entries = list(getattr(self.Q, "attachment_history", []))

        for row, entry in zip(attachment_rows, attachment_entries):
            expression = entry.get("expression") if isinstance(entry, dict) else None
            differential = entry.get("differential") if isinstance(entry, dict) else None
            cell_label = row.get("cell") or f"cell {row['index']}"
            kind = "bridge" if row.get("kind") == "bridge" else "cell"
            node_id = f"{kind}:{row['index']}"
            add_node(
                node_id,
                kind,
                self._attachment_graph_label(row, expression),
                detail=cell_label,
                mathLabel=self._attachment_graph_math_label(row, expression),
                attachmentIndex=row["index"],
                cell=row.get("cell", ""),
                attachmentKind=row.get("kind", ""),
            )
            cell_label_to_id[cell_label] = node_id
            self._primitive_graph_index_cell(
                expression,
                node_id,
                cell_id_by_mp_key,
                cell_id_by_block_key,
            )

            if kind == "bridge":
                for term in self._primitive_graph_bridge_terms(row.get("expression", "")):
                    term_id = add_presentation(
                        term,
                        "bridge side",
                        math_label=self._math_from_display_label(term),
                    )
                    add_edge(node_id, term_id, "bridge-leg", "bridge", dashed=True)

                continue

            presentation = (
                row.get("differentialPresentation")
                or row.get("expressionDisplay")
                or row.get("differentialDisplay")
                or row.get("expression")
                or row.get("differential")
                or cell_label
            )
            presentation_math = (
                self._math_mp_expression_display(expression)
                or self._math_mp_expression_display(differential)
                or self._math_from_display_label(presentation)
            )
            presentation_node = add_presentation(
                presentation,
                row.get("kind", "attached cell"),
                math_label=presentation_math,
            )
            add_edge(node_id, presentation_node, "resolves", "d")

        self._primitive_graph_add_replacement_edges(
            add_node,
            add_edge,
            add_presentation,
            cell_label_to_id,
        )
        self._primitive_graph_add_generated_chains(
            add_node,
            add_edge,
            add_presentation,
            cell_id_by_mp_key,
            cell_id_by_block_key,
        )
        loop_nodes, loop_edges = self._primitive_graph_closed_loop_subgraph(
            nodes,
            edges,
        )

        return {
            "quiver": self._serialize_quiver_metadata(),
            "nodes": list(loop_nodes.values()),
            "edges": loop_edges,
            "summary": {
                "nodeCount": len(loop_nodes),
                "edgeCount": len(loop_edges),
                "attachmentCount": len(attachment_rows),
                "rawNodeCount": len(nodes),
                "rawEdgeCount": len(edges),
            },
        }

    def _serialize_cyclic_class_graph(self) -> dict[str, Any]:
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []
        circles: list[dict[str, Any]] = []
        seen_edges: set[tuple[str, str, str, str, str]] = set()
        cell_label_to_id: dict[str, str] = {}
        cell_id_by_mp_key: dict[str, str] = {}
        cell_id_by_block_key: dict[str, str] = {}
        product_circle_keys: set[str] = set()
        product_circle_id_by_key: dict[str, str] = {}
        pure_circle_keys: set[str] = set()
        product_circle_limit = 180

        def css_token(value: Any) -> str:
            return re.sub(r"[^a-z0-9_-]+", "-", str(value or "").lower()).strip("-")

        def add_node(
            node_id: str,
            kind: str,
            label: str,
            detail: str = "",
            **extra: Any,
        ) -> str:
            if not node_id:
                node_id = f"{kind}:{len(nodes) + 1}"

            clean_extra = {
                key: value
                for key, value in extra.items()
                if value not in (None, "", [])
            }

            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "kind": kind,
                    "label": label or node_id,
                    "mathLabel": clean_extra.pop("mathLabel", None) or self._math_from_display_label(label),
                    "detail": detail,
                    **clean_extra,
                }
            else:
                node = nodes[node_id]

                if not node.get("detail") and detail:
                    node["detail"] = detail

                for key, value in clean_extra.items():
                    if key == "status" and node.get("status") == "unresolved":
                        continue

                    node[key] = value

            return node_id

        def add_edge(
            source: str,
            target: str,
            kind: str,
            label: str = "",
            **extra: Any,
        ) -> None:
            if not source or not target or source == target:
                return

            status = str(extra.get("status") or "")
            key = (source, target, kind, label, status)

            if key in seen_edges:
                return

            seen_edges.add(key)
            edges.append({
                "source": source,
                "target": target,
                "kind": kind,
                "label": label,
                **{
                    k: v
                    for k, v in extra.items()
                    if v not in (None, "", [])
                },
            })

        def add_presentation(
            label: str,
            detail: str = "",
            math_label: str | None = None,
            **extra: Any,
        ) -> str:
            return add_node(
                "presentation:" + label,
                "presentation",
                label,
                detail,
                mathLabel=math_label,
                **extra,
            )

        def factor_key_tuple(items: Any) -> tuple[str, ...]:
            out = []

            for item in tuple(items or ()):
                try:
                    out.append(repr(self.Q.mp_factor_key(item)))
                except Exception:
                    out.append(repr(item))

            return tuple(out)

        def product_node_id(factors: Any) -> str:
            return "product:" + repr(factor_key_tuple(factors))

        def pure_node_id(inputs: Any) -> str:
            return "pure:" + repr(factor_key_tuple(inputs))

        def product_circle_key(factors: Any) -> str:
            try:
                return repr(self.Q.canonical_cyclic_factor_key(tuple(factors or ())))
            except Exception:
                return repr(factor_key_tuple(factors))

        def pure_circle_key(inputs: Any) -> str:
            try:
                return repr(self.Q.canonical_pure_massey_input_key(tuple(inputs or ())))
            except Exception:
                return repr(factor_key_tuple(inputs))

        def product_is_oriented_cycle(factors: Any) -> bool:
            try:
                factors = self.Q.canonical_mp_factors(tuple(factors or ()))
            except Exception:
                factors = tuple(factors or ())

            if not factors:
                return False

            try:
                return bool(self.Q.mp_factors_composable(factors, cyclic=True))
            except Exception:
                return False

        def product_report_is_compatibly_resolved(report: dict[str, Any] | None) -> bool:
            if not isinstance(report, dict):
                return False

            if not report.get("resolved") or report.get("likely_over"):
                return False

            try:
                resolution_count = int(report.get("minimal_resolution_count") or 0)
            except Exception:
                resolution_count = 0

            return bool(report.get("compatible_resolutions")) and resolution_count >= 2

        def product_report_is_graph_redundant(report: dict[str, Any] | None) -> bool:
            if product_report_is_compatibly_resolved(report):
                return True

            if not isinstance(report, dict) or not report.get("resolved"):
                return False

            sources = [
                source
                for source in tuple(report.get("minimal_resolution_sources", ()) or ())
                if isinstance(source, dict)
            ]

            if not sources:
                return False

            inherited_sources = {
                "bridge_replacement",
                "completed_massey_tower",
                "resolved_massey_factor",
                "stasheff_zero",
            }

            return all(
                (source.get("source") or source.get("kind") or "") in inherited_sources
                for source in sources
            )

        def inputs_are_oriented_cycle(inputs: Any) -> bool:
            inputs = tuple(inputs or ())

            if not inputs:
                return False

            try:
                inputs = self.Q.normalize_mp_inputs(inputs)
            except Exception:
                pass

            try:
                return bool(self.Q.mp_factors_composable(inputs, cyclic=True))
            except Exception:
                pass

            try:
                for left, right in zip(inputs, inputs[1:]):
                    if left.target != right.source:
                        return False

                return inputs[-1].target == inputs[0].source
            except Exception:
                return False

        def add_product_presentation(
            factors: Any,
            detail: str = "",
            status: str = "",
            note: str = "",
        ) -> str:
            factors = tuple(factors or ())
            label = self._format_product(factors)
            return add_node(
                product_node_id(factors),
                "presentation",
                label,
                detail,
                mathLabel=self._math_product(factors),
                expressionKind="product",
                factorCount=len(factors),
                status=css_token(status),
                note=note,
            )

        def add_pure_presentation(
            inputs: Any,
            detail: str = "",
            status: str = "",
            note: str = "",
        ) -> str:
            inputs = tuple(inputs or ())
            return add_node(
                pure_node_id(inputs),
                "massey",
                self._plain_massey_label(inputs),
                detail,
                mathLabel=self._math_massey_label(inputs),
                expressionKind="pure_massey",
                arity=len(inputs),
                status=css_token(status),
                note=note,
            )

        def circle_center(index: int) -> tuple[float, float]:
            columns = 3
            spacing_x = 380
            spacing_y = 330
            column = index % columns
            row = index // columns
            return (
                (column - ((columns - 1) / 2)) * spacing_x,
                row * spacing_y,
            )

        def place_circle(
            kind: str,
            label: str,
            node_ids: list[str],
            status: str = "resolved",
            note: str = "",
        ) -> str | None:
            unique_ids = list(dict.fromkeys(node_ids))

            if len(unique_ids) < 2:
                return None

            circle_id = f"{kind}-circle:{len(circles) + 1}"
            x, y = circle_center(len(circles))
            radius = max(78, min(190, 42 + len(unique_ids) * 18))
            status_token = css_token(status or "resolved")
            circles.append({
                "id": circle_id,
                "kind": kind,
                "label": label,
                "nodeIds": unique_ids,
                "status": status_token,
                "note": note,
                "x": x,
                "y": y,
                "r": radius,
            })

            for index, node_id in enumerate(unique_ids):
                angle = (math.tau * index) / len(unique_ids) - (math.pi / 2)
                node = nodes.get(node_id)

                if node is None:
                    continue

                node["circleId"] = circle_id
                node["circleLabel"] = label
                node["x"] = x + math.cos(angle) * radius
                node["y"] = y + math.sin(angle) * radius
                node["fixed"] = True

            return circle_id

        attachment_rows = self._serialize_attachments()
        attachment_entries = list(getattr(self.Q, "attachment_history", []))

        for row, entry in zip(attachment_rows, attachment_entries):
            expression = entry.get("expression") if isinstance(entry, dict) else None
            cell_label = row.get("cell") or f"cell {row['index']}"
            kind = "bridge" if row.get("kind") == "bridge" else "cell"
            node_id = f"{kind}:{row['index']}"
            add_node(
                node_id,
                kind,
                self._attachment_graph_label(row, expression),
                detail=cell_label,
                mathLabel=self._attachment_graph_math_label(row, expression),
                attachmentIndex=row["index"],
                cell=row.get("cell", ""),
                attachmentKind=row.get("kind", ""),
            )
            cell_label_to_id[cell_label] = node_id
            self._primitive_graph_index_cell(
                expression,
                node_id,
                cell_id_by_mp_key,
                cell_id_by_block_key,
            )

        def cell_or_virtual_for_block(block: Any, face_id: str | None = None) -> str | None:
            return self._primitive_graph_cell_or_virtual_for_face(
                tuple(block or ()),
                cell_id_by_mp_key,
                cell_id_by_block_key,
                add_node,
                add_edge,
                add_presentation,
                face_id=face_id,
                connect_virtual_face=face_id is None,
            )

        def bridge_node_for_record(record: dict[str, Any], index: int) -> str:
            bridge_cell = self._safe_str(record.get("bridge_cell"))
            bridge_id = cell_label_to_id.get(bridge_cell)

            if bridge_id is not None:
                return bridge_id

            return add_node(
                "bridge-replacement:" + repr((
                    index,
                    bridge_cell,
                    self._safe_str(record.get("bridge_expression")),
                )),
                "bridge",
                "w?",
                detail=bridge_cell or self._safe_str(record.get("bridge_expression")),
                mathLabel="w[?]",
            )

        def add_product_candidate_chain(
            alpha_id: str,
            candidate: dict[str, Any],
            chain_index: int,
        ) -> None:
            current_id = alpha_id
            path = tuple(candidate.get("bridge_path", ()) or ())

            for path_index, record in enumerate(path, start=1):
                if not isinstance(record, dict):
                    continue

                after_factors = (
                    record.get("source_product_after")
                    or record.get("replacement_factors")
                    or record.get("to")
                )

                if not after_factors:
                    continue

                after_id = add_product_presentation(
                    tuple(after_factors),
                    "replacement presentation",
                )
                replacement_type = record.get("replacement_type", "bridge")

                if replacement_type == "bridge":
                    bridge_id = bridge_node_for_record(record, path_index)
                    add_edge(
                        current_id,
                        bridge_id,
                        "bridge-leg",
                        "bridge",
                        dashed=True,
                        detail=self._safe_str(record.get("bridge_expression")),
                    )
                    add_edge(
                        bridge_id,
                        after_id,
                        "bridge-leg",
                        "bridge",
                        dashed=True,
                        detail=self._safe_str(record.get("bridge_expression")),
                    )
                    add_edge(
                        current_id,
                        after_id,
                        "bridge-replacement",
                        "bridge",
                        detail=self._safe_str(record.get("bridge_expression")),
                    )
                else:
                    add_edge(
                        current_id,
                        after_id,
                        "ainf-replacement",
                        "A-inf",
                        detail=replacement_type,
                    )

                if len(product_circle_keys) < product_circle_limit:
                    add_product_circle_from_report(
                        tuple(after_factors),
                        source="replacement target",
                    )

                current_id = after_id

            block = tuple(candidate.get("block", ()) or ())

            if not block:
                block = tuple(candidate.get("replacement_factors", ()) or ())

            if not block:
                return

            block_id = add_product_presentation(
                block,
                "resolved block in this presentation",
            )
            add_edge(current_id, block_id, "chain-term", "block")
            cell_id = cell_or_virtual_for_block(block, face_id=block_id)

            if cell_id is not None:
                source = candidate.get("source") or candidate.get("kind") or "primitive"
                add_edge(
                    block_id,
                    cell_id,
                    "resolves",
                    "cell",
                    detail=source,
                    chainIndex=chain_index,
                )

        def product_relation_detail(relation: dict[str, Any]) -> str:
            expression = relation.get("expression")

            if expression is None and isinstance(relation.get("source_relation"), dict):
                expression = relation["source_relation"].get("expression")

            if expression is None and isinstance(relation.get("edge"), dict):
                expression = relation["edge"].get("bridge_expression")

            return self._safe_str(expression)

        def add_product_replacement_relation_edge(
            relation: dict[str, Any],
            relation_index: int,
        ) -> None:
            left = tuple(relation.get("left", ()) or ())
            right = tuple(relation.get("right", ()) or ())

            if not left or not right:
                return

            if not (
                product_is_oriented_cycle(left)
                and product_is_oriented_cycle(right)
            ):
                return

            replacement_type = relation.get("replacement_type", "bridge")
            detail = product_relation_detail(relation)
            left_id = add_product_circle_from_report(
                left,
                source=f"{replacement_type} replacement source",
            )
            right_id = add_product_circle_from_report(
                right,
                source=f"{replacement_type} replacement target",
            )

            if not left_id or not right_id:
                return

            if replacement_type == "bridge":
                bridge_id = bridge_node_for_record(
                    {
                        "bridge_cell": relation.get("cell"),
                        "bridge_expression": detail,
                    },
                    relation_index,
                )
                add_edge(
                    left_id,
                    bridge_id,
                    "bridge-leg",
                    "bridge",
                    dashed=True,
                    detail=detail,
                )
                add_edge(
                    bridge_id,
                    right_id,
                    "bridge-leg",
                    "bridge",
                    dashed=True,
                    detail=detail,
                )
                add_edge(
                    left_id,
                    right_id,
                    "bridge-replacement",
                    "bridge",
                    detail=detail,
                )
                return

            add_edge(
                left_id,
                right_id,
                "ainf-replacement",
                "A-inf",
                detail=replacement_type,
            )

        def add_product_circle_from_report(
            factors: Any,
            report: dict[str, Any] | None = None,
            source: str = "",
            status_hint: str = "",
            note: str = "",
        ) -> str:
            factors = tuple(factors or ())

            if not product_is_oriented_cycle(factors):
                return ""

            if report is None:
                try:
                    report = self.Q.cyclic_product_class_report(factors, verify=False)
                except Exception:
                    report = {}

            if (
                not status_hint
                and product_report_is_graph_redundant(report)
            ):
                return ""

            alpha_id = add_product_presentation(
                factors,
                source or "cyclic product member",
                status=status_hint,
                note=note,
            )
            key = product_circle_key(factors)

            if key in product_circle_keys:
                if status_hint:
                    status_token = css_token(status_hint)
                    nodes[alpha_id]["status"] = status_token
                    circle_id = product_circle_id_by_key.get(key)

                    for circle in circles:
                        if circle.get("id") != circle_id:
                            continue

                        if (
                            circle.get("status") != "over-resolved"
                            or status_token == "over-resolved"
                        ):
                            circle["status"] = status_token

                if note:
                    nodes[alpha_id]["note"] = note
                    circle_id = product_circle_id_by_key.get(key)

                    for circle in circles:
                        if circle.get("id") == circle_id:
                            circle["note"] = note
                            break

                return alpha_id

            if len(product_circle_keys) >= product_circle_limit:
                nodes[alpha_id]["status"] = "unresolved"
                nodes[alpha_id]["note"] = "Graph expansion stopped at the finite display limit."
                return alpha_id

            product_circle_keys.add(key)
            bridge_resolved = False

            if not report.get("resolved") and status_hint != "unresolved":
                try:
                    bridge_resolved = bool(
                        self.Q.product_cyclic_class_is_bridge_resolved(
                            factors,
                        ).get("resolved")
                    )
                except Exception:
                    bridge_resolved = False

            rotations = list(report.get("rotations", []))
            member_ids = []
            rotation_ids: dict[int, str] = {}

            for rotation in rotations:
                rotation_factors = tuple(rotation.get("factors", ()) or ())

                if not rotation_factors:
                    continue

                rotation_id = add_product_presentation(
                    rotation_factors,
                    "cyclic product rotation",
                )
                rotation_ids[int(rotation.get("index", len(rotation_ids)))] = rotation_id

                if rotation_id not in member_ids:
                    member_ids.append(rotation_id)

            if alpha_id not in member_ids:
                member_ids.insert(0, alpha_id)

            likely_over = status_hint == "over-resolved"
            unresolved = status_hint == "unresolved" or (
                not bool(report.get("resolved"))
                and not bridge_resolved
                and source != "known resolved block"
            )
            circle_status = (
                "over-resolved"
                if likely_over
                else "unresolved"
                if unresolved
                else "resolved"
            )
            circle_note = note

            if likely_over:
                circle_note = "This cyclic product class has at least two minimal resolutions."
            elif unresolved:
                circle_note = note or "The automaton found this non-resolvable product cycle."

            circle_id = place_circle(
                "product",
                self._format_product(factors),
                member_ids,
                circle_status,
                circle_note,
            )
            if circle_id is not None:
                product_circle_id_by_key[key] = circle_id

            if unresolved:
                nodes[alpha_id]["status"] = "unresolved"
                nodes[alpha_id]["note"] = circle_note

            for rotation in rotations:
                rotation_id = rotation_ids.get(int(rotation.get("index", -1)))

                if not rotation_id:
                    continue

                candidates = [
                    candidate
                    for candidate in tuple(rotation.get("candidates", ()) or ())
                    if isinstance(candidate, dict)
                ]

                if not candidates:
                    continue

                minimal = [
                    candidate
                    for candidate in candidates
                    if candidate.get("minimal")
                ]
                chosen = minimal if likely_over and minimal else (minimal[:1] or candidates[:1])

                for index, candidate in enumerate(chosen, start=1):
                    add_product_candidate_chain(rotation_id, candidate, index)

            return alpha_id

        def add_pure_circle_from_report(
            inputs: Any,
            report: dict[str, Any] | None = None,
            status_hint: str = "",
            note: str = "",
        ) -> str:
            inputs = tuple(inputs or ())

            if not inputs_are_oriented_cycle(inputs):
                return ""

            alpha_id = add_pure_presentation(
                inputs,
                "pure Massey cyclic member",
                status=status_hint,
                note=note,
            )
            key = pure_circle_key(inputs)

            if key in pure_circle_keys:
                if status_hint:
                    nodes[alpha_id]["status"] = css_token(status_hint)

                if note:
                    nodes[alpha_id]["note"] = note

                return alpha_id

            if report is None:
                try:
                    report = self.Q.pure_massey_cyclic_class_report(
                        inputs,
                        record=True,
                    )
                except Exception:
                    report = {}

            if not report.get("is_genuine", True):
                return alpha_id

            pure_circle_keys.add(key)
            rotations = list(report.get("rotations", []))
            complete_orbit = bool(report.get("complete_compatible_orbit"))
            member_ids = []

            for rotation in rotations:
                rotation_inputs = tuple(rotation.get("inputs", ()) or ())

                if not rotation_inputs:
                    continue

                if complete_orbit and rotation.get("defined"):
                    rotation_id = add_pure_presentation(
                        rotation_inputs,
                        "pure Massey rotation",
                    )

                    if rotation_id not in member_ids:
                        member_ids.append(rotation_id)

                if rotation.get("resolved"):
                    cell_id = self._primitive_graph_cell_for_face(
                        rotation_inputs,
                        cell_id_by_mp_key,
                        cell_id_by_block_key,
                    )

                    if cell_id is not None:
                        resolved_id = add_pure_presentation(
                            rotation_inputs,
                            "resolved pure Massey rotation",
                        )
                        add_edge(resolved_id, cell_id, "resolves", "cell")

            if alpha_id not in member_ids and complete_orbit:
                member_ids.insert(0, alpha_id)

            likely_over = status_hint == "over-resolved"
            unresolved = status_hint == "unresolved" or not bool(report.get("resolved"))
            circle_status = (
                "over-resolved"
                if likely_over
                else "unresolved"
                if unresolved
                else "resolved"
            )
            circle_note = note

            if likely_over:
                circle_note = "This pure Massey cyclic class is resolved by both the chosen member and the other rotations."
            elif unresolved:
                circle_note = note or "This pure Massey cyclic class is not resolved yet."

            if complete_orbit and len(member_ids) >= 2:
                place_circle(
                    "pure-massey",
                    self._plain_massey_label(inputs),
                    member_ids,
                    circle_status,
                    circle_note,
                )

            if unresolved:
                nodes[alpha_id]["status"] = "unresolved"
                nodes[alpha_id]["note"] = circle_note

            if likely_over:
                nodes[alpha_id]["status"] = "over-resolved"
                nodes[alpha_id]["note"] = circle_note

            return alpha_id

        try:
            max_pure_arity = int(
                self.computation_settings.get(
                    "maxPureArity",
                    DEFAULT_COMPUTATION_SETTINGS["maxPureArity"],
                )
            )

            with self._computation_context(include_primitive_details=False):
                report, _ = capture_output(
                    self.Q.cyclic_search_stage_report,
                    max_pure_arity=max_pure_arity,
                    record=True,
                )

                product_entries: list[tuple[tuple[Any, ...], dict[str, Any], str, str]] = []
                seen_product_entries: set[str] = set()
                product_relations_to_draw: list[dict[str, Any]] = []

                def remember_product_entry(
                    factors: Any,
                    item_report: dict[str, Any] | None = None,
                    status: str = "",
                    note_text: str = "",
                ) -> None:
                    factors_tuple = tuple(factors or ())

                    if (
                        not factors_tuple
                        or not product_is_oriented_cycle(factors_tuple)
                    ):
                        return

                    key = product_circle_key(factors_tuple) + ":" + status

                    if key in seen_product_entries:
                        return

                    seen_product_entries.add(key)
                    product_entries.append((
                        factors_tuple,
                        item_report or {},
                        status,
                        note_text,
                    ))

                try:
                    relation_seen = set()

                    for relation in tuple(self.Q.product_replacement_relations() or ()):
                        if not isinstance(relation, dict):
                            continue

                        left = tuple(relation.get("left", ()) or ())
                        right = tuple(relation.get("right", ()) or ())

                        if not left or not right:
                            continue

                        if not (
                            product_is_oriented_cycle(left)
                            and product_is_oriented_cycle(right)
                        ):
                            continue

                        replacement_type = relation.get("replacement_type", "bridge")
                        left_key = factor_key_tuple(left)
                        right_key = factor_key_tuple(right)
                        relation_detail = product_relation_detail(relation)
                        relation_key_factors = (
                            tuple(sorted((left_key, right_key)))
                            if replacement_type == "bridge"
                            else (left_key, right_key)
                        )
                        relation_key = (
                            relation_key_factors,
                            replacement_type,
                            self._safe_str(relation.get("cell")),
                            relation_detail,
                        )

                        if relation_key in relation_seen:
                            continue

                        relation_seen.add(relation_key)
                        product_relations_to_draw.append(relation)
                        remember_product_entry(
                            left,
                            None,
                            "",
                            f"{replacement_type} replacement source",
                        )
                        remember_product_entry(
                            right,
                            None,
                            "",
                            f"{replacement_type} replacement target",
                        )
                except Exception:
                    product_relations_to_draw = []

                product_result = report.get("product_result", {}) if isinstance(report, dict) else {}
                buckets = [
                    ("unresolved_classes", "unresolved"),
                    ("terminating_unresolved_classes", "unresolved"),
                    ("deferred_unresolved_classes", "unresolved"),
                    ("likely_over_classes", "over-resolved"),
                ]

                for bucket, status in buckets:
                    for entry in tuple(product_result.get(bucket, ()) or ()):
                        if not isinstance(entry, dict):
                            continue

                        entry_status = "over-resolved" if entry.get("likely_over") else status
                        remember_product_entry(
                            entry.get("factors", ()),
                            entry.get("report"),
                            entry_status,
                            (
                                "The automaton found this non-resolvable product cycle."
                                if entry_status == "unresolved"
                                else "This product cyclic class has at least two minimal resolutions."
                            ),
                        )

                next_result = product_result.get("next_result", {})

                if isinstance(next_result, dict) and next_result.get("cycle"):
                    next_status = (
                        "over-resolved"
                        if next_result.get("kind") == "likely_over"
                        else "unresolved"
                        if not next_result.get("won")
                        else ""
                    )
                    remember_product_entry(
                        next_result.get("cycle", ()),
                        next_result.get("report"),
                        next_status,
                        (
                            "This product cyclic class has at least two minimal resolutions."
                            if next_status == "over-resolved"
                            else "The product automaton stopped on this cycle."
                        ),
                    )

                try:
                    for block in tuple(self.Q.known_resolved_product_blocks() or ()):
                        if not isinstance(block, dict):
                            continue

                        block_factors = tuple(block.get("factors", ()) or ())

                        if not block_factors:
                            continue

                        remember_product_entry(
                            block_factors,
                            self.Q.cyclic_product_class_report(block_factors, verify=False),
                            "",
                            "known resolved product block",
                        )
                except Exception:
                    pass

                for factors, item_report, status, note_text in product_entries:
                    source_text = ""

                    if not status:
                        source_text = (
                            "known resolved block"
                            if note_text == "known resolved product block"
                            else note_text
                        )

                    add_product_circle_from_report(
                        factors,
                        item_report or None,
                        source=source_text,
                        status_hint=status,
                        note=note_text,
                    )

                for index, relation in enumerate(product_relations_to_draw, start=1):
                    add_product_replacement_relation_edge(relation, index)

                pure_generated = (
                    report.get("pure_generated_result", {})
                    if isinstance(report, dict)
                    else {}
                )

                for entry in tuple(pure_generated.get("classes", ()) or ()):
                    if not isinstance(entry, dict):
                        continue

                    if entry.get("cyclically_zero"):
                        continue

                    entry_status = (
                        "over-resolved"
                        if entry.get("likely_over")
                        else "unresolved"
                        if not entry.get("resolved")
                        else ""
                    )
                    add_pure_circle_from_report(
                        entry.get("inputs", ()),
                        entry.get("report"),
                        entry_status,
                    )

                pure_search = (
                    report.get("pure_search_result")
                    if isinstance(report, dict)
                    else None
                )

                if isinstance(pure_search, dict) and pure_search.get("found"):
                    status = (
                        "over-resolved"
                        if pure_search.get("status") == "likely_over"
                        else "unresolved"
                    )
                    add_pure_circle_from_report(
                        pure_search.get("inputs", ()),
                        pure_search.get("report"),
                        status,
                        (
                            "Pure Massey search found this over-resolved class."
                            if status == "over-resolved"
                            else "Pure Massey search found this unresolved class."
                        ),
                    )

        except Exception as error:
            add_node(
                "cyclic-error",
                "presentation",
                "Cyclic graph error",
                detail=self._safe_str(error),
                status="unresolved",
                note="The cyclic graph serializer could not finish.",
            )

        circle_node_ids = {
            node_id
            for circle in circles
            for node_id in circle.get("nodeIds", [])
        }
        connected_node_ids = set(circle_node_ids)

        for edge in edges:
            connected_node_ids.add(edge.get("source"))
            connected_node_ids.add(edge.get("target"))

        visible_nodes = {
            node_id: node
            for node_id, node in nodes.items()
            if node_id in connected_node_ids
            or node.get("status") in {"unresolved", "over-resolved"}
        }
        visible_edges = [
            edge
            for edge in edges
            if edge.get("source") in visible_nodes
            and edge.get("target") in visible_nodes
        ]

        status_counts: dict[str, int] = {}

        for circle in circles:
            status = circle.get("status") or "resolved"
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "quiver": self._serialize_quiver_metadata(),
            "nodes": list(visible_nodes.values()),
            "edges": visible_edges,
            "circles": circles,
            "summary": {
                "nodeCount": len(visible_nodes),
                "edgeCount": len(visible_edges),
                "circleCount": len(circles),
                "productCircleCount": sum(1 for circle in circles if circle.get("kind") == "product"),
                "pureCircleCount": sum(1 for circle in circles if circle.get("kind") == "pure-massey"),
                "statusCounts": status_counts,
            },
        }

    def _primitive_graph_closed_loop_subgraph(
        self,
        nodes: dict[str, dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
        kept = set(nodes.keys())
        adjacency: dict[str, set[str]] = {
            node_id: set()
            for node_id in kept
        }

        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")

            if source not in kept or target not in kept or source == target:
                continue

            adjacency[source].add(target)
            adjacency[target].add(source)

        queue = [
            node_id
            for node_id, neighbors in adjacency.items()
            if len(neighbors) < 2
        ]

        while queue:
            node_id = queue.pop()

            if node_id not in kept:
                continue

            kept.remove(node_id)

            for neighbor in tuple(adjacency.get(node_id, ())):
                adjacency[neighbor].discard(node_id)

                if neighbor in kept and len(adjacency[neighbor]) < 2:
                    queue.append(neighbor)

            adjacency[node_id].clear()

        loop_edges = [
            edge
            for edge in edges
            if edge.get("source") in kept and edge.get("target") in kept
        ]
        loop_nodes = {
            node_id: node
            for node_id, node in nodes.items()
            if node_id in kept
        }
        return loop_nodes, loop_edges

    def _attachment_graph_label(
        self,
        row: dict[str, Any],
        expression: Any = None,
    ) -> str:
        prefix = self._attachment_graph_prefix(row)
        presentation = (
            self._format_mp_expression_display(expression)
            or row.get("expressionDisplay")
            or row.get("differentialPresentation")
            or row.get("cell")
            or ""
        )

        if presentation:
            return f"{prefix}[{presentation}]"

        return f"{prefix}{row.get('index')}"

    def _attachment_graph_math_label(
        self,
        row: dict[str, Any],
        expression: Any = None,
    ) -> str:
        prefix = self._attachment_graph_prefix(row)
        presentation = (
            self._math_mp_expression_display(expression)
            or self._math_from_display_label(row.get("expressionDisplay", ""))
            or self._math_from_display_label(row.get("differentialPresentation", ""))
        )

        if presentation:
            return f"{prefix}[{presentation}]"

        return f"{prefix}_{{{row.get('index')}}}"

    def _attachment_graph_prefix(self, row: dict[str, Any]) -> str:
        if row.get("kind") == "bridge":
            return "w"

        if row.get("kind") == "ordinary_cell":
            return "u"

        return "v"

    def _primitive_graph_key_token(self, value: Any) -> str:
        return repr(value)

    def _primitive_graph_index_cell(
        self,
        expression: Any,
        node_id: str,
        cell_id_by_mp_key: dict[str, str],
        cell_id_by_block_key: dict[str, str],
    ) -> None:
        if isinstance(expression, self.MasseyProduct):
            try:
                key = self.Q.mp_key(*expression.inputs)
                cell_id_by_mp_key[self._primitive_graph_key_token(key)] = node_id
                cell_id_by_block_key[self._primitive_graph_key_token(key)] = node_id
            except Exception:
                pass

            return

        if isinstance(expression, self.MPProduct):
            try:
                key = self.Q.mp_product_block_key(expression.factors)
                cell_id_by_block_key[self._primitive_graph_key_token(key)] = node_id
            except Exception:
                pass

            return

        if isinstance(expression, self.MPElement) and len(expression.terms) == 1:
            try:
                product, coeff = next(iter(expression.terms.items()))
            except Exception:
                return

            if str(coeff) not in {"1", "-1"} or not isinstance(product, self.MPProduct):
                return

            try:
                key = self.Q.mp_product_block_key(product.factors)
                cell_id_by_block_key[self._primitive_graph_key_token(key)] = node_id
            except Exception:
                pass

    def _primitive_graph_cell_for_face(
        self,
        inputs: tuple[Any, ...],
        cell_id_by_mp_key: dict[str, str],
        cell_id_by_block_key: dict[str, str],
    ) -> str | None:
        try:
            factors = self.Q.canonical_mp_factors(tuple(inputs or ()))
        except Exception:
            factors = tuple(inputs or ())

        if factors:
            try:
                block_key = self.Q.mp_product_block_key(factors)
                token = self._primitive_graph_key_token(block_key)
                if token in cell_id_by_block_key:
                    return cell_id_by_block_key[token]
            except Exception:
                pass

            if len(factors) == 1 and isinstance(factors[0], self.MasseyProduct):
                try:
                    key = self.Q.mp_key(*factors[0].inputs)
                    token = self._primitive_graph_key_token(key)
                    if token in cell_id_by_mp_key:
                        return cell_id_by_mp_key[token]
                except Exception:
                    pass

        try:
            key = self.Q.mp_key(*inputs)
        except Exception:
            return None

        token = self._primitive_graph_key_token(key)
        return cell_id_by_mp_key.get(token) or cell_id_by_block_key.get(token)

    def _primitive_graph_virtual_cell_for_face(
        self,
        inputs: tuple[Any, ...],
        add_node,
        add_edge,
        add_presentation,
        face_id: str | None = None,
        connect_virtual_face: bool = True,
    ) -> str | None:
        factors = []

        for item in tuple(inputs or ()):
            if isinstance(item, self.MasseyProduct):
                factors.append(item)
            else:
                mp_item = self.Q.mp(item)

                if mp_item is None:
                    return None

                factors.append(mp_item)

        if not factors:
            return None

        try:
            candidates = self.Q.product_word_resolution_candidates(
                tuple(factors),
                verify=False,
            )
        except Exception:
            candidates = []

        if not candidates:
            return None

        candidate = next(
            (
                item
                for item in candidates
                if item.get("source") == "bridge_replacement"
                or item.get("kind") in {"bridge_replacement", "completed_massey_tower"}
            ),
            candidates[0],
        )
        face_label = self._format_product(tuple(factors))
        face_math = self._math_product(tuple(factors))
        source = candidate.get("source") or candidate.get("kind") or "primitive"
        witness_prefix = "w" if source == "bridge_replacement" else "v"
        witness_detail = {
            "bridge_replacement": "virtual bridge-replacement witness",
            "completed_massey_tower": "virtual tower witness",
        }.get(source, f"{source} witness")
        node_id = "virtual-face:" + self._primitive_graph_key_token((
            source,
            tuple(self.Q.mp_factor_key(factor) for factor in factors),
        ))
        witness_id = add_node(
            node_id,
            "bridge" if source == "bridge_replacement" else "cell",
            f"{witness_prefix}[{face_label}]",
            detail=witness_detail,
            mathLabel=f"{witness_prefix}[{face_math}]",
        )

        if connect_virtual_face:
            if face_id is None:
                face_id = add_presentation(
                    face_label,
                    "virtual primitive face",
                    math_label=face_math,
                )

            add_edge(witness_id, face_id, "resolves", "v", dashed=True)

        return witness_id

    def _primitive_graph_cell_or_virtual_for_face(
        self,
        inputs: tuple[Any, ...],
        cell_id_by_mp_key: dict[str, str],
        cell_id_by_block_key: dict[str, str],
        add_node,
        add_edge,
        add_presentation,
        face_id: str | None = None,
        connect_virtual_face: bool = True,
    ) -> str | None:
        cell_id = self._primitive_graph_cell_for_face(
            inputs,
            cell_id_by_mp_key,
            cell_id_by_block_key,
        )

        if cell_id is not None:
            return cell_id

        return self._primitive_graph_virtual_cell_for_face(
            inputs,
            add_node,
            add_edge,
            add_presentation,
            face_id=face_id,
            connect_virtual_face=connect_virtual_face,
        )

    def _math_symbol(self, value: Any) -> str:
        text = str(value or "").strip()

        if not text:
            return ""

        if text == "0":
            return "0"

        match = re.fullmatch(r"([A-Za-z]+)_?(\d+)", text)

        if match:
            return f"{match.group(1)}_{{{match.group(2)}}}"

        return text.replace("*", "").replace(" ", "")

    def _math_from_display_label(self, value: Any) -> str:
        text = str(value or "").strip()

        if not text:
            return ""

        def replace_mp(match: re.Match[str]) -> str:
            items = [
                item.strip()
                for item in match.group(1).split(",")
                if item.strip()
            ]
            return f"m_{{{len(items)}}}(" + ",".join(
                self._math_symbol(item)
                for item in items
            ) + ")"

        text = re.sub(r"Q\.mp\(([^()]*)\)", replace_mp, text)
        text = text.replace("*", " ")
        return re.sub(
            r"\b([A-Za-z]+)_?(\d+)\b",
            lambda match: f"{match.group(1)}_{{{match.group(2)}}}",
            text,
        )

    def _math_inputs(self, inputs: Any) -> str:
        return ",".join(
            self._math_mp_input_atom(item)
            for item in tuple(inputs or ())
        )

    def _math_massey_label(self, inputs: Any) -> str:
        inputs = tuple(inputs or ())
        return f"m_{{{len(inputs)}}}({self._math_inputs(inputs)})"

    def _plain_massey_label(self, inputs: Any) -> str:
        inputs = tuple(inputs or ())
        return "m" + str(len(inputs)) + "(" + ",".join(
            self._format_mp_input_atom(item)
            for item in inputs
        ) + ")"

    def _math_product(self, factors: Any) -> str:
        return " ".join(
            self._math_mp_factor(factor)
            for factor in tuple(factors or ())
        )

    def _math_mp_factor(self, factor: Any) -> str:
        if isinstance(factor, self.MasseyProduct):
            if len(factor.inputs) == 1:
                return self._math_mp_input_atom(factor.inputs[0])

            return self._math_massey_label(factor.inputs)

        return self._math_mp_input_atom(factor)

    def _math_mp_input_atom(self, item: Any) -> str:
        if isinstance(item, self.MasseyProduct):
            return self._math_mp_factor(item)

        if isinstance(item, self.Path):
            return "".join(
                self._math_symbol(arrow.name if hasattr(arrow, "name") else arrow)
                for arrow in item.arrows
            )

        if isinstance(item, self.Arrow):
            return self._math_symbol(item.name)

        return self._math_symbol(item)

    def _math_mp_expression_display(self, expr: Any) -> str:
        if expr is None:
            return ""

        if isinstance(expr, self.MPProduct):
            return self._math_product(expr.factors)

        if isinstance(expr, self.MasseyProduct):
            return self._math_mp_factor(expr)

        if isinstance(expr, self.Element):
            return self._math_element_display(expr)

        if isinstance(expr, self.MPElement):
            pieces = []

            for product, coeff in expr.terms.items():
                product_label = self._math_product(product.factors)
                coeff_label = str(coeff)

                if coeff_label == "1":
                    pieces.append((1, product_label))
                elif coeff_label == "-1":
                    pieces.append((-1, product_label))
                elif coeff_label.startswith("-"):
                    pieces.append((-1, f"{coeff_label[1:]}{product_label}"))
                else:
                    pieces.append((1, f"{coeff_label}{product_label}"))

            if not pieces:
                return "0"

            text = ""

            for index, (sign, piece) in enumerate(pieces):
                if index == 0:
                    text += f"-{piece}" if sign < 0 else piece
                else:
                    text += f" {'-' if sign < 0 else '+'} {piece}"

            return text

        return self._math_from_display_label(expr)

    def _math_element_display(self, expr: Any) -> str:
        pieces = []

        for path, coeff in expr.terms.items():
            path_label = self._math_mp_input_atom(path)
            coeff_label = str(coeff)

            if coeff_label == "1":
                pieces.append((1, path_label))
            elif coeff_label == "-1":
                pieces.append((-1, path_label))
            elif coeff_label.startswith("-"):
                pieces.append((-1, f"{coeff_label[1:]}{path_label}"))
            else:
                pieces.append((1, f"{coeff_label}{path_label}"))

        if not pieces:
            return "0"

        text = ""

        for index, (sign, piece) in enumerate(pieces):
            if index == 0:
                text += f"-{piece}" if sign < 0 else piece
            else:
                text += f" {'-' if sign < 0 else '+'} {piece}"

        return text

    def _primitive_graph_product_has_higher_massey_factor(self, factors: Any) -> bool:
        return any(
            isinstance(factor, self.MasseyProduct)
            and len(tuple(factor.inputs)) >= 3
            for factor in tuple(factors or ())
        )

    def _primitive_graph_bridge_terms(self, expression_text: str) -> list[str]:
        expression_text = str(expression_text or "").strip()

        if not expression_text:
            return []

        try:
            expression = self._expression_from_display_text(expression_text)
        except Exception:
            expression = None

        if isinstance(expression, self.MPElement):
            terms = []

            for product, coeff in expression.terms.items():
                if not isinstance(product, self.MPProduct):
                    continue

                label = self._format_product(product.factors)
                coeff_label = str(coeff)

                if coeff_label == "1":
                    terms.append(label)
                elif coeff_label == "-1":
                    terms.append(label)
                else:
                    terms.append(f"{coeff_label}*{label}")

            if terms:
                return terms

        pieces = [
            piece.strip().removeprefix("-").strip()
            for piece in expression_text.replace(" - ", " + -").split(" + ")
            if piece.strip()
        ]
        return pieces[:2] if len(pieces) >= 2 else pieces

    def _expression_from_display_text(self, text: str) -> Any:
        for entry in getattr(self.Q, "attachment_history", []):
            expression = entry.get("expression")

            if self._safe_str(expression) == text:
                return expression

        return None

    def _primitive_graph_add_replacement_edges(
        self,
        add_node,
        add_edge,
        add_presentation,
        cell_label_to_id: dict[str, str],
    ) -> None:
        try:
            with self._computation_context(include_primitive_details=False):
                replacement_edges = list(self.Q.replacement_edge_records())
        except Exception:
            replacement_edges = []

        for index, edge in enumerate(replacement_edges, start=1):
            target = edge.get("target_factors")
            replacement = edge.get("replacement_factors")

            if target is None or replacement is None:
                continue

            target_label = self._format_product(target)
            replacement_label = self._format_product(replacement)
            target_math = self._math_product(target)
            replacement_math = self._math_product(replacement)

            if not target_label or not replacement_label:
                continue

            replacement_type = edge.get("replacement_type", "bridge")

            if (
                replacement_type == "ainf"
                and (
                    self._primitive_graph_product_has_higher_massey_factor(target)
                    or self._primitive_graph_product_has_higher_massey_factor(replacement)
                )
            ):
                continue

            target_id = add_presentation(
                target_label,
                "replacement source",
                math_label=target_math,
            )
            replacement_id = add_presentation(
                replacement_label,
                "replacement target",
                math_label=replacement_math,
            )

            if replacement_type == "bridge":
                bridge_cell = self._safe_str(edge.get("bridge_cell"))
                bridge_id = cell_label_to_id.get(bridge_cell)

                if bridge_id is None:
                    bridge_id = add_node(
                        f"bridge-edge:{index}",
                        "bridge",
                        f"w?",
                        detail=bridge_cell or self._safe_str(edge.get("bridge_expression")),
                        mathLabel="w[?]",
                    )

                add_edge(target_id, bridge_id, "bridge-leg", "bridge", dashed=True)
                add_edge(bridge_id, replacement_id, "bridge-leg", "bridge", dashed=True)
                continue

            add_edge(
                target_id,
                replacement_id,
                "ainf-replacement",
                "A-inf",
                directed=True,
            )

    def _primitive_graph_add_generated_chains(
        self,
        add_node,
        add_edge,
        add_presentation,
        cell_id_by_mp_key: dict[str, str],
        cell_id_by_block_key: dict[str, str],
    ) -> None:
        for item in getattr(self.Q, "generated_massey_products", []):
            if not isinstance(item, self.MasseyProduct):
                continue

            inputs = tuple(item.inputs)

            if len(inputs) < 3:
                continue

            first_face = inputs[:-1]
            second_face = inputs[1:]
            first_cell_id = self._primitive_graph_cell_or_virtual_for_face(
                first_face,
                cell_id_by_mp_key,
                cell_id_by_block_key,
                add_node,
                add_edge,
                add_presentation,
            )
            second_cell_id = self._primitive_graph_cell_or_virtual_for_face(
                second_face,
                cell_id_by_mp_key,
                cell_id_by_block_key,
                add_node,
                add_edge,
                add_presentation,
            )

            if first_cell_id is None or second_cell_id is None:
                continue

            generation_key = self._generation_item_key(item)
            mp_id = add_node(
                "massey-chain:" + generation_key,
                "massey",
                self._plain_massey_label(inputs),
                detail=f"{item.source} -> {item.target}",
                mathLabel=self._math_massey_label(inputs),
            )
            first_label, first_math = self._primitive_graph_chain_term_labels(
                inputs,
                0,
                len(inputs) - 1,
            )
            second_label, second_math = self._primitive_graph_chain_term_labels(
                inputs,
                1,
                len(inputs),
            )
            first_term_id = add_presentation(
                first_label,
                "Massey chain term",
                math_label=first_math,
            )
            second_term_id = add_presentation(
                second_label,
                "Massey chain term",
                math_label=second_math,
            )

            add_edge(first_term_id, second_term_id, "chain-term", "chain")
            add_edge(first_term_id, first_cell_id, "massey-chain", "chain")
            add_edge(second_term_id, second_cell_id, "massey-chain", "chain")
            add_edge(first_cell_id, second_cell_id, "cell-pair", "pair")

            for vertex_id in {
                first_term_id,
                second_term_id,
                first_cell_id,
                second_cell_id,
            }:
                add_edge(mp_id, vertex_id, "massey-center", "m")

    def _primitive_graph_chain_term_labels(
        self,
        inputs: tuple[Any, ...],
        start: int,
        stop: int,
    ) -> tuple[str, str]:
        plain_parts = []
        math_parts = []

        for item in inputs[:start]:
            plain_parts.append(self._format_mp_input_atom(item))
            math_parts.append(self._math_mp_input_atom(item))

        block = inputs[start:stop]

        if len(block) >= 3:
            block_massey = None

            try:
                block_massey = getattr(self.Q, "massey_products", {}).get(
                    self.Q.mp_key(*block),
                    None,
                )
            except Exception:
                block_massey = None

            if isinstance(block_massey, self.MasseyProduct):
                plain_parts.append(self._format_mp_factor(block_massey))
            else:
                plain_parts.append(self._plain_massey_label(block))

            math_parts.append(self._math_massey_label(block))
        else:
            for item in block:
                plain_parts.append(self._format_mp_input_atom(item))
                math_parts.append(self._math_mp_input_atom(item))

        for item in inputs[stop:]:
            plain_parts.append(self._format_mp_input_atom(item))
            math_parts.append(self._math_mp_input_atom(item))

        return "*".join(plain_parts), " ".join(math_parts)

    def _primitive_graph_add_generated_pairs(
        self,
        add_node,
        add_edge,
        cell_label_to_id: dict[str, str],
    ) -> None:
        for item in getattr(self.Q, "generated_massey_products", []):
            if not isinstance(item, self.MasseyProduct):
                continue

            key = self.Q.mp_key(*item.inputs)
            generation_key = self._generation_item_key(item)
            record = self._primitive_record_for_generated_item(
                item,
                key,
                generation_key,
            )

            if not isinstance(record, dict):
                continue

            pairs = record.get("unsettled_termination_pairs", []) or []

            if not pairs:
                continue

            mp_id = add_node(
                "massey:" + generation_key,
                "massey",
                self._format_inputs(item.inputs),
                detail=f"{item.source} -> {item.target}",
            )

            for pair in pairs:
                first_cell = self._pair_cell_label(pair.get("first_termination"))
                second_cell = self._pair_cell_label(pair.get("second_termination"))
                first_id = cell_label_to_id.get(first_cell)
                second_id = cell_label_to_id.get(second_cell)

                if first_id is None or second_id is None:
                    continue

                add_edge(first_id, second_id, "cell-pair", "pair")
                add_edge(mp_id, first_id, "massey-witness", "m")
                add_edge(mp_id, second_id, "massey-witness", "m")

    def _pair_cell_label(self, item: Any) -> str:
        if not isinstance(item, dict):
            return ""

        return str(item.get("cell") or "").strip()

    def _serialize_last_run(self) -> dict[str, Any] | None:
        if not self.last_run:
            return None

        report = self.last_run["report"]
        summary = self.last_run["summary"]
        product_result = report.get("product_result", {})
        pure_generated = report.get("pure_generated_result", {})
        product_cycles = report.get("generated_product_cycle_result", {})
        redundancy = report.get("generator_redundancy_result", {})
        pure_search = report.get("pure_search_result")
        product_classes = [
            self._serialize_product_entry(entry)
            for entry in product_result.get("terminating_unresolved_classes", [])
        ]
        deferred_product_classes = [
            self._serialize_product_entry(entry)
            for entry in product_result.get("deferred_unresolved_classes", [])
        ]
        likely_over_product_classes = [
            self._serialize_product_entry(entry)
            for entry in product_result.get("likely_over_classes", [])
        ]

        return {
            "summary": summary,
            "product": {
                "won": bool(product_result.get("won")),
                "firstUnresolvedLength": product_result.get("first_unresolved_length"),
                "searchedMaxLength": product_result.get("searched_max_length"),
                "searchIncomplete": bool(product_result.get("search_incomplete")),
                "terminating": product_classes,
                "deferred": deferred_product_classes,
                "likelyOver": likely_over_product_classes,
                "generatedCycles": [
                    self._serialize_product_cycle_entry(entry)
                    for entry in product_cycles.get("unresolved_classes", [])
                ],
                "redundantGenerators": [
                    self._serialize_redundant_generator_entry(entry)
                    for entry in redundancy.get("redundant_generators", [])
                ],
            },
            "pureGenerated": {
                "won": bool(pure_generated.get("won")),
                "unresolved": [
                    self._serialize_pure_entry(entry)
                    for entry in pure_generated.get("unresolved_classes", [])
                ],
                "likelyOver": [
                    self._serialize_pure_entry(entry)
                    for entry in pure_generated.get("likely_over_classes", [])
                ],
            },
            "pureSearch": self._serialize_pure_search(pure_search),
        }

    def _serialize_autocomplete_plan(self) -> dict[str, Any] | None:
        plan = self.last_autocomplete_plan

        if not plan:
            return None

        report = plan.get("report") or plan.get("pure_result", {}).get("report")
        choices = []

        if report:
            for rotation in report.get("rotations", []):
                inputs = tuple(rotation.get("inputs", ()))

                if not inputs:
                    continue

                choices.append({
                    "label": self._format_inputs(inputs),
                    "defined": bool(rotation.get("defined")),
                    "resolved": bool(rotation.get("resolved")),
                    "choiceInputs": [self._factor_spec(x) for x in inputs],
                })

        proposed = []

        for item in plan.get("proposed_attachments", []) or plan.get("attachments", []):
            inputs = tuple(item.get("inputs", ()))
            proposed.append({
                "label": self._format_inputs(inputs),
                "choiceInputs": [self._factor_spec(x) for x in inputs],
                "reason": item.get("reason", ""),
            })

        return {
            "status": plan.get("status"),
            "reason": plan.get("reason"),
            "choices": choices,
            "proposed": proposed,
            "leaveInputs": [
                self._factor_spec(x)
                for x in tuple(plan.get("leave_inputs") or ())
            ],
        }

    def _serialize_product_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        factors = tuple(entry.get("factors", ()))
        bridge_resolution = entry.get("bridge_resolution", {})
        report = entry.get("report", {})

        if not isinstance(report, dict):
            report = {}

        source_labels = [
            self._format_product(tuple(source.get("block", ())))
            for source in tuple(entry.get("resolution_sources", ()))
            if source.get("block")
        ]
        return {
            "label": self._format_product(factors),
            "length": entry.get("length", len(factors)),
            "factors": [self._factor_spec(x) for x in factors],
            "expression": {
                "type": "product",
                "factors": [self._factor_spec(x) for x in factors],
            },
            "bridgeResolved": bool(bridge_resolution.get("resolved")),
            "likelyOver": bool(entry.get("likely_over")),
            "resolutionSources": source_labels,
            "likelyOverReason": report.get("likely_over_reason", ""),
            "nonCompatibleChain": self._serialize_product_noncompatible_chain(
                report.get("noncompatible_resolution_chain")
            ),
            "overResolutionWitness": self._serialize_product_over_resolution_witness(
                report.get("over_resolution_witness")
            ),
        }

    def _product_candidate_cell_label(self, part: dict[str, Any]) -> str:
        block = tuple(part.get("block", ()))
        primitive = part.get("raw_primitive") or part.get("primitive")
        primitive_text = self._safe_str(primitive)
        prefix = getattr(primitive, "cell_prefix", None) or "v"

        if "[" in primitive_text:
            candidate = primitive_text.split("[", 1)[0].strip()

            if candidate:
                prefix = candidate

        return f"{prefix}[{self._format_product(block)}]"

    def _product_candidate_term_label(self, part: dict[str, Any]) -> str:
        pieces = []
        left = tuple(part.get("left", ()) or part.get("left_context", ()) or ())
        right = tuple(part.get("right", ()) or part.get("right_context", ()) or ())

        if left:
            pieces.append(self._format_product(left))

        pieces.append(self._product_candidate_cell_label(part))

        if right:
            pieces.append(self._format_product(right))

        return "*".join(piece for piece in pieces if piece)

    def _serialize_product_cycle_candidate(self, candidate: Any) -> dict[str, Any]:
        candidate = candidate if isinstance(candidate, dict) else {}
        span = candidate.get("block_span")

        return {
            "block": self._format_product(tuple(candidate.get("block", ()))),
            "span": list(span) if span is not None else None,
            "source": candidate.get("source", ""),
            "cell": self._product_candidate_cell_label(candidate),
            "primitive": self._product_candidate_term_label(candidate),
        }

    def _serialize_product_cycle_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        factors = tuple(entry.get("factors", ()))
        candidates = [
            candidate if isinstance(candidate, dict) else {}
            for candidate in tuple(entry.get("candidates", ()))
        ]

        def span_width(candidate: dict[str, Any]) -> int:
            span = candidate.get("block_span")

            if not span:
                return 0

            try:
                return int(span[1]) - int(span[0])
            except Exception:
                return 0

        candidates.sort(
            key=lambda candidate: (
                -span_width(candidate),
                tuple(candidate.get("block_span", ()) or ()),
                self._format_product(tuple(candidate.get("block", ()))),
            )
        )
        serialized_candidates = [
            self._serialize_product_cycle_candidate(candidate)
            for candidate in candidates
        ]
        primitive_terms = [
            item["primitive"]
            for item in serialized_candidates
            if item.get("primitive")
        ]
        cycle = " - ".join(primitive_terms[:2])

        return {
            "label": self._format_product(factors),
            "length": entry.get("length", len(factors)),
            "factors": [self._factor_spec(x) for x in factors],
            "expression": {
                "type": "product",
                "factors": [self._factor_spec(x) for x in factors],
            },
            "status": "generated_cycle",
            "cycle": cycle,
            "candidates": serialized_candidates,
            "notMasseyProduct": True,
        }

    def _serialize_redundant_generator_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        factors = tuple(entry.get("factors", ()))
        bridge_resolution = entry.get("bridge_resolution", {})
        resolved_word = tuple(bridge_resolution.get("resolved_word") or ())

        return {
            "name": str(entry.get("name") or ""),
            "label": self._format_product(factors),
            "reason": entry.get("reason", ""),
            "cyclic": bool(entry.get("cyclic")),
            "bridgeResolved": bool(bridge_resolution.get("resolved")),
            "resolvedWord": self._format_product(resolved_word),
            "expression": {
                "type": "product",
                "factors": [self._factor_spec(x) for x in factors],
            },
        }

    def _serialize_product_over_resolution_witness(self, witness: Any) -> dict[str, Any] | None:
        if not isinstance(witness, dict):
            return None

        def cell_label(part: dict[str, Any]) -> str:
            block = tuple(part.get("block", ()))
            primitive = self._safe_str(
                part.get("primitive")
                or part.get("raw_primitive")
            )
            prefix = "v"

            if "[" in primitive:
                candidate = primitive.split("[", 1)[0].strip()

                if candidate:
                    prefix = candidate

            return f"{prefix}[{self._format_product(block)}]"

        def primitive_label(part: dict[str, Any]) -> str:
            pieces = []
            left = tuple(part.get("left_context", ()))
            right = tuple(part.get("right_context", ()))

            if left:
                pieces.append(self._format_product(left))

            pieces.append(cell_label(part))

            if right:
                pieces.append(self._format_product(right))

            return "*".join(pieces)

        def side_payload(part: Any) -> dict[str, Any]:
            part = part if isinstance(part, dict) else {}
            return {
                "word": self._format_product(tuple(part.get("word", ()))),
                "block": self._format_product(tuple(part.get("block", ()))),
                "cell": cell_label(part),
                "primitive": primitive_label(part),
            }

        left = side_payload(witness.get("left"))
        right = side_payload(witness.get("right"))
        return {
            "kind": witness.get("kind", ""),
            "left": left,
            "right": right,
            "cause": f"{left['word']} = {right['word']}",
            "primitiveChain": f"{left['primitive']} and {right['primitive']}",
        }

    def _serialize_product_noncompatible_chain(self, chain: Any) -> dict[str, Any] | None:
        if not isinstance(chain, dict):
            return None

        def op_label(operation: Any) -> str:
            operation = operation if isinstance(operation, dict) else {}
            block = tuple(operation.get("block", ()) or ())
            replacement = tuple(operation.get("replacement", ()) or ())
            rotation = operation.get("rotation_index", 0)
            block_label = self._format_product(block)

            if operation.get("kind") == "cyclic_replacement" and replacement:
                return (
                    f"{block_label} to {self._format_product(replacement)} "
                    f"after rotation {rotation}"
                )

            return f"{block_label} after rotation {rotation}"

        failures = []

        for operation in tuple(chain.get("incompatible_operations", ()) or ()):
            operation = operation if isinstance(operation, dict) else {}
            block = tuple(operation.get("block", ()) or ())
            rotations = tuple(operation.get("failed_rotation_indices", ()) or ())

            if not block:
                continue

            rotation_text = ", ".join(str(item) for item in rotations)
            failures.append(
                f"{self._format_product(block)} is broken by rotation {rotation_text}"
            )

        operations = [
            op_label(operation)
            for operation in tuple(chain.get("operations", ()) or ())
        ]

        return {
            "summary": "non-compatible cyclic replacements",
            "failures": failures,
            "chain": " ; ".join(operations),
        }

    def _serialize_pure_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        inputs = tuple(entry.get("inputs", ()))
        return {
            "label": self._format_inputs(inputs),
            "arity": entry.get("arity", len(inputs)),
            "resolved": bool(entry.get("resolved")),
            "likelyOver": bool(entry.get("likely_over")),
            "isolated": bool(entry.get("isolated")),
            "nonIsolated": bool(entry.get("non_isolated")),
            "choiceInputs": [self._factor_spec(x) for x in inputs],
            "expression": {
                "type": "massey",
                "inputs": [self._factor_spec(x) for x in inputs],
            },
        }

    def _serialize_pure_search(self, result: dict[str, Any] | None) -> dict[str, Any] | None:
        if not result:
            return None

        inputs = tuple(result.get("inputs", ()))
        return {
            "found": bool(result.get("found")),
            "status": result.get("status"),
            "arity": result.get("arity"),
            "label": self._format_inputs(inputs) if inputs else "",
            "choiceInputs": [self._factor_spec(x) for x in inputs],
        }

    def _summarize_run(self, report: dict[str, Any]) -> dict[str, Any]:
        pure_generated = report.get("pure_generated_result", {})
        pure_search = report.get("pure_search_result") or {}
        product_result = report.get("product_result", {})
        product_cycles = report.get("generated_product_cycle_result", {})
        redundancy = report.get("generator_redundancy_result", {})
        product_cycle_count = len(product_cycles.get("unresolved_classes", []))
        redundant_generator_count = len(redundancy.get("redundant_generators", []))
        likely_over_count = len(product_result.get("likely_over_classes", []))
        likely_over_count += len(pure_generated.get("likely_over_classes", []))
        likely_over_count += len(product_cycles.get("likely_over_classes", []))

        if pure_search.get("status") == "likely_over":
            likely_over_count += 1

        not_likely_reason = self._run_not_likely_reason(report)

        if report.get("won"):
            status = "win"
            headline = "Victory! Every current cyclic obstruction is resolved."
        elif redundant_generator_count:
            status = "lose"
            headline = "Not victorious: a generator is redundant."
        elif likely_over_count:
            status = "lose"
            headline = "Not victorious (and unlikely): an over-resolved cyclic class was detected."
        elif product_cycle_count:
            status = "not_yet"
            headline = "Not yet victorious: a generated product cycle was detected."
        elif not_likely_reason:
            status = "not_likely"
            headline = (
                "Not yet victorious (and unlikely): "
                + not_likely_reason
            )
        else:
            status = "not_yet"
            next_kind = report.get("next_kind") or "unknown"
            headline = f"Not yet victorious: next obstruction is {next_kind}."

        return {
            "status": status,
            "headline": headline,
            "nextKind": report.get("next_kind"),
            "productPartWon": bool(report.get("product_part_won")),
            "productFirstLength": product_result.get("first_unresolved_length"),
            "pureUnresolvedCount": len(pure_generated.get("unresolved_classes", [])),
            "productCycleCount": product_cycle_count,
            "redundantGeneratorCount": redundant_generator_count,
            "likelyOverCount": likely_over_count,
            "notLikelyReason": not_likely_reason,
        }

    def _run_not_likely_reason(self, report: dict[str, Any]) -> str | None:
        if report.get("won"):
            return None

        product_cycles = report.get("generated_product_cycle_result", {})

        if product_cycles.get("unresolved_classes"):
            return None

        entry = self._double_minimal_product_class(report.get("product_result", {}))

        if entry is None:
            return None

        label = self._format_product(tuple(entry.get("factors", ())))
        return f"the cyclic class of {label} has at least two minimal resolutions."

    def _double_minimal_product_class(self, product_result: dict[str, Any]) -> dict[str, Any] | None:
        entries = list(product_result.get("unresolved_classes", []))
        entries.extend(product_result.get("terminating_unresolved_classes", []))
        entries.extend(product_result.get("deferred_unresolved_classes", []))

        if not getattr(self.Q, "skip_deep_tower_resolution", False):
            try:
                for block in self.Q.known_resolved_product_blocks():
                    factors = tuple(block.get("factors", ()))
                    entries.append({
                        "factors": factors,
                        "report": self.Q.cyclic_product_class_report(factors),
                        "source": block.get("source"),
                    })
            except Exception:
                pass

        seen = set()

        for entry in entries:
            factors = tuple(entry.get("factors", ()))
            key = repr(tuple(self._format_mp_factor(factor) for factor in factors))

            if key in seen:
                continue

            seen.add(key)
            report = entry.get("report", {})

            if bool(report.get("likely_over")):
                return entry

        return None

    def _factor_spec(self, item: Any) -> dict[str, Any]:
        if self._is_zero_factor(item):
            return {
                "type": "zero",
                "value": 0,
                "label": "0",
            }

        if isinstance(item, self.MasseyProduct):
            return {
                "type": "mp",
                "inputs": [self._factor_spec(x) for x in item.inputs],
            }

        if isinstance(item, self.MPProduct):
            return {
                "type": "product",
                "coefficient": "1",
                "factors": [self._factor_spec(factor) for factor in item.factors],
            }

        if isinstance(item, self.Arrow):
            return {
                "type": "arrow",
                "name": item.name,
            }

        if isinstance(item, self.Path) and len(item.arrows) == 1:
            name = item.arrows[0]
            return {
                "type": "arrow",
                "name": name.name if hasattr(name, "name") else name,
            }

        if isinstance(item, self.Path):
            names = [
                arrow.name if hasattr(arrow, "name") else arrow
                for arrow in item.arrows
            ]
            return {
                "type": "path",
                "arrows": names,
                "label": self._format_mp_input_atom(item),
            }

        raise GameError(f"Cannot serialize factor {item}.")

    def _is_zero_factor(self, item: Any) -> bool:
        if item == 0:
            return True

        terms = getattr(item, "terms", None)
        return isinstance(terms, dict) and len(terms) == 0

    def _spec_contains_zero(self, spec: Any) -> bool:
        if not isinstance(spec, dict):
            return False

        if spec.get("type") == "zero":
            return True

        for key in ("inputs", "factors"):
            if any(self._spec_contains_zero(item) for item in spec.get(key, []) or []):
                return True

        return False

    def _format_inputs(self, inputs: Any) -> str:
        inputs = tuple(inputs or ())

        if not inputs:
            return ""

        try:
            M = self.Q.mp(*inputs)

            if M is not None:
                return str(M)
        except Exception:
            pass

        return "Q.mp(" + ",".join(str(x) for x in inputs) + ")"

    def _format_product(self, factors: Any) -> str:
        factors = tuple(factors or ())

        if not factors:
            return ""

        return "*".join(self._format_mp_factor(factor) for factor in factors)

    def _format_mp_factor(self, factor: Any) -> str:
        if isinstance(factor, self.MasseyProduct):
            if len(factor.inputs) == 1:
                return self._format_mp_input_atom(factor.inputs[0])

            return "Q.mp(" + ",".join(
                self._format_mp_input_atom(item)
                for item in factor.inputs
            ) + ")"

        return self._format_mp_input_atom(factor)

    def _format_mp_input_atom(self, item: Any) -> str:
        if isinstance(item, self.MasseyProduct):
            return self._format_mp_factor(item)

        if isinstance(item, self.Path):
            return "*".join(
                str(arrow.name if hasattr(arrow, "name") else arrow)
                for arrow in item.arrows
            )

        return str(item)

    def _format_mp_expression_display(self, expr: Any) -> str:
        if expr is None:
            return ""

        if isinstance(expr, self.MPProduct):
            return self._format_product(expr.factors)

        if isinstance(expr, self.MasseyProduct):
            return self._format_mp_factor(expr)

        if isinstance(expr, self.Element):
            return self._format_element_display(expr)

        if isinstance(expr, self.MPElement):
            pieces = []

            for product, coeff in expr.terms.items():
                product_label = self._format_product(product.factors)
                coeff_label = str(coeff)

                if coeff_label == "1":
                    pieces.append((1, product_label))
                elif coeff_label == "-1":
                    pieces.append((-1, product_label))
                elif coeff_label.startswith("-"):
                    pieces.append((-1, f"{coeff_label[1:]}*{product_label}"))
                else:
                    pieces.append((1, f"{coeff_label}*{product_label}"))

            if not pieces:
                return "0"

            text = ""

            for index, (sign, piece) in enumerate(pieces):
                if index == 0:
                    text += f"-{piece}" if sign < 0 else piece
                else:
                    text += f" {'-' if sign < 0 else '+'} {piece}"

            return text

        return self._safe_str(expr)

    def _format_attachment_differential(
        self,
        kind: str,
        expression: Any,
        differential: Any,
    ) -> str:
        if kind in {"mp_cell", "bridge"}:
            presentation = self._format_mp_expression_display(expression)

            if presentation:
                return presentation

        return self._format_mp_expression_display(differential)

    def _format_element_display(self, expr: Any) -> str:
        pieces = []

        for path, coeff in expr.terms.items():
            path_label = self._format_mp_input_atom(path)
            coeff_label = str(coeff)

            if coeff_label == "1":
                pieces.append((1, path_label))
            elif coeff_label == "-1":
                pieces.append((-1, path_label))
            elif coeff_label.startswith("-"):
                pieces.append((-1, f"{coeff_label[1:]}*{path_label}"))
            else:
                pieces.append((1, f"{coeff_label}*{path_label}"))

        if not pieces:
            return "0"

        text = ""

        for index, (sign, piece) in enumerate(pieces):
            if index == 0:
                text += f"-{piece}" if sign < 0 else piece
            else:
                text += f" {'-' if sign < 0 else '+'} {piece}"

        return text

    def _safe_str(self, value: Any) -> str:
        if value is None:
            return ""

        try:
            return str(value)
        except Exception:
            return repr(value)


class DGRightModulePresentation:
    """Finitely generated right module presentation coker(F1 -> F0)."""

    def __init__(
        self,
        generators: list[dict[str, Any]],
        rows: list[dict[str, Any]],
    ) -> None:
        self.generators = generators
        self.rows = rows

    def matrix_shape(self) -> dict[str, int]:
        return {
            "rows": len(self.rows),
            "columns": len(self.generators),
        }

    def row_displays(self, analyzer: "DGQuiverRelationsAnalyzer") -> list[dict[str, Any]]:
        return [
            {
                "name": row["name"],
                "vertex": row["vertex"],
                "entries": [
                    analyzer.expression_display(entry)
                    for entry in row["entries"]
                ],
            }
            for row in self.rows
        ]


class DGRightProjectiveModule:
    """Right projective P(i) = e_i A for the current path-algebra quotient A."""

    def __init__(self, vertex: str) -> None:
        self.vertex = vertex
        self.name = f"P({vertex})"

    def generator(self) -> dict[str, Any]:
        return {
            "name": f"P_{self.vertex}",
            "vertex": self.vertex,
            "degree": 0,
        }

    def report(
        self,
        analyzer: "DGQuiverRelationsAnalyzer",
        basis_groups: list[list[tuple[str, ...]]],
        finite_dimensional: dict[str, Any],
    ) -> dict[str, Any]:
        grouped_basis = []
        flat_basis = []

        for length, paths in enumerate(basis_groups):
            starting_paths = [
                path
                for path in paths
                if analyzer.path_endpoints(path)
                and analyzer.path_endpoints(path)[0] == self.vertex
            ]
            flat_basis.extend(starting_paths)
            grouped_basis.append({
                "length": length,
                "paths": [
                    analyzer._serialize_path(path)
                    for path in starting_paths
                ],
            })

        is_finite = finite_dimensional.get("status") == "finite"
        report: dict[str, Any] = {
            "name": self.name,
            "vertex": self.vertex,
            "description": f"P({self.vertex}) = e_{self.vertex} A",
            "generator": self.generator(),
            "basisByLength": grouped_basis,
            "basis": [
                analyzer._serialize_path(path)
                for path in flat_basis
            ],
            "basisCount": len(flat_basis),
            "basisDisplayComplete": is_finite,
            "dimensionKnown": is_finite,
        }

        if is_finite:
            report["dimension"] = len(flat_basis)
        else:
            report["message"] = "Displayed normal paths up to the current basis length."

        return report


class DGQuiverRelationsAnalyzer:
    """Small path-algebra quotient analyzer for the DG relations page."""

    ID_PREFIX = "e:"
    NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload if isinstance(payload, dict) else {}
        self.vertices: list[str] = []
        self.arrows: dict[str, dict[str, Any]] = {}
        self.arrow_order: list[str] = []
        self.differentials: dict[str, dict[tuple[str, ...], Fraction]] = {}
        self.relations: list[dict[str, Any]] = []
        self.rules: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    def analyze(self) -> dict[str, Any]:
        self._load_vertices()
        self._load_arrows()
        self._load_differentials()
        self._load_relations()
        self._orient_relations()

        max_length = self._max_length()
        sample_text = str(self.payload.get("sample") or "").strip()
        sample = self._parse_expression(sample_text, "sample") if sample_text else {}
        sample_reduction = self.reduce_expression(sample) if sample_text else {}

        finite_dimensional = self._finite_dimensional_report()
        basis_display_length = max_length

        if finite_dimensional.get("status") == "finite":
            basis_display_length = max(
                max_length,
                int(finite_dimensional.get("longestNormalPathLength") or 0),
            )

        basis_by_length = self._basis_by_length(basis_display_length)
        relation_checks = self._relation_differential_checks()
        dg_ideal = self._dg_ideal_report(relation_checks)
        d_squared_checks = self._d_squared_checks()
        module_presentation = self._module_presentation_report(finite_dimensional)
        projective_modules = self._projective_modules_report(
            finite_dimensional,
            basis_display_length,
        )

        return {
            "vertices": self.vertices,
            "arrows": [self.arrows[name] for name in self.arrow_order],
            "relations": [
                {
                    "index": index + 1,
                    "display": self.expression_display(item["expression"]),
                    "source": item["source"],
                    "target": item["target"],
                }
                for index, item in enumerate(self.relations)
            ],
            "rules": [self._serialize_rule(rule) for rule in self.rules],
            "basisByLength": basis_by_length,
            "basisCount": sum(len(group["paths"]) for group in basis_by_length),
            "basisDisplayLength": basis_display_length,
            "basisDisplayComplete": finite_dimensional.get("status") == "finite",
            "finiteDimensional": finite_dimensional,
            "relationChecks": relation_checks,
            "dgIdeal": dg_ideal,
            "dSquaredChecks": d_squared_checks,
            "modulePresentation": module_presentation,
            "projectiveModules": projective_modules,
            "sample": {
                "input": sample_text,
                "normalForm": self.expression_display(sample_reduction),
                "terms": self.serialize_expression(sample_reduction),
                "isZero": not bool(sample_reduction),
                "inIdeal": not bool(sample_reduction),
            } if sample_text else None,
            "warnings": self.warnings,
            "messages": self._summary_messages(
                max_length,
                relation_checks,
                d_squared_checks,
                finite_dimensional,
            ),
        }

    def _load_vertices(self) -> None:
        raw = self.payload.get("vertices", [])

        if isinstance(raw, str):
            vertices = [
                item.strip()
                for item in re.split(r"[\s,]+", raw)
                if item.strip()
            ]
        else:
            vertices = [str(item).strip() for item in raw or [] if str(item).strip()]

        seen = set()
        self.vertices = []

        for vertex in vertices:
            if vertex in seen:
                raise GameError(f"Vertex {vertex} is listed more than once.")

            seen.add(vertex)
            self.vertices.append(vertex)

        if not self.vertices:
            raise GameError("Enter at least one vertex.")

    def _load_arrows(self) -> None:
        arrows = self.payload.get("arrows", [])

        if not isinstance(arrows, list):
            raise GameError("Arrows must be a list.")

        vertex_set = set(self.vertices)

        for item in arrows:
            if not isinstance(item, dict):
                raise GameError("Each arrow must be an object.")

            name = clean_name(item.get("name"), "Arrow name")

            if not self.NAME_RE.match(name):
                raise GameError(
                    "Arrow names must start with a letter and contain only letters, digits, or underscores."
                )

            if name in self.arrows:
                raise GameError(f"Arrow {name} is listed more than once.")

            if name.startswith("e_"):
                raise GameError("Arrow names may not start with e_; that prefix is reserved for idempotents.")

            source = clean_name(item.get("source"), f"Source of {name}")
            target = clean_name(item.get("target"), f"Target of {name}")

            if source not in vertex_set:
                raise GameError(f"Source {source} of {name} is not a vertex.")

            if target not in vertex_set:
                raise GameError(f"Target {target} of {name} is not a vertex.")

            degree = self._parse_degree(item.get("degree"))

            self.arrows[name] = {
                "name": name,
                "source": source,
                "target": target,
                "degree": degree,
                "differential": str(item.get("differential") or "").strip(),
            }
            self.arrow_order.append(name)

    def _parse_degree(self, value: Any) -> int | None:
        text = str(value or "").strip().lower()

        if text in {"", "?", "unknown", "undetermined", "none"}:
            return None

        return parse_optional_int(value)

    def _load_differentials(self) -> None:
        for name in self.arrow_order:
            arrow = self.arrows[name]
            text = arrow.get("differential") or ""
            expression = self._parse_expression(text, f"d({name})") if text else {}

            if expression and not self._expression_has_endpoints(
                expression,
                arrow["source"],
                arrow["target"],
            ):
                raise GameError(
                    f"d({name}) must be a linear combination of paths from "
                    f"{arrow['source']} to {arrow['target']}."
                )

            self.differentials[name] = expression

    def _load_relations(self) -> None:
        raw = self.payload.get("relations", [])

        if isinstance(raw, str):
            lines = raw.splitlines()
        elif isinstance(raw, list):
            lines = [str(item) for item in raw]
        else:
            raise GameError("Relations must be text or a list.")

        for line_number, line in enumerate(lines, start=1):
            text = line.split("#", 1)[0].strip()

            if not text:
                continue

            if "=" in text:
                left, right = text.split("=", 1)
                left_expression = self._parse_expression(left, f"relation {line_number} left side")
                right_expression = self._parse_expression(right, f"relation {line_number} right side")
                expression = self._clean_expression({
                    path: (
                        left_expression.get(path, Fraction(0))
                        - right_expression.get(path, Fraction(0))
                    )
                    for path in set(left_expression) | set(right_expression)
                })
            else:
                expression = self._parse_expression(text, f"relation {line_number}")

            if not expression:
                continue

            endpoints = self._expression_endpoints(expression)

            if endpoints is None:
                raise GameError(
                    f"Relation {line_number} is not uniform: every term must have the same source and target."
                )

            self.relations.append({
                "line": line_number,
                "text": line.strip(),
                "expression": expression,
                "source": endpoints[0],
                "target": endpoints[1],
            })

    def _orient_relations(self) -> None:
        for relation in self.relations:
            expression = relation["expression"]
            leading = max(expression, key=self._path_order_key)
            leading_coeff = expression[leading]

            if self._path_length(leading) == 0:
                raise GameError(
                    f"Relation {relation['line']} has an idempotent leading term; this reducer only orients relations with arrow paths."
                )

            rest = dict(expression)
            del rest[leading]
            replacement = {
                path: -coeff / leading_coeff
                for path, coeff in rest.items()
            }
            replacement = self._clean_expression(replacement)
            self.rules.append({
                "relation": relation,
                "leading": leading,
                "leadingCoeff": leading_coeff,
                "replacement": replacement,
            })

        self.rules.sort(
            key=lambda rule: self._path_order_key(rule["leading"]),
            reverse=True,
        )

    def _parse_expression(self, text: str, label: str) -> dict[tuple[str, ...], Fraction]:
        text = str(text or "").replace("−", "-").strip()

        if not text or text == "0":
            return {}

        tokens = self._tokenize_expression(text, label)
        index = 0

        def peek() -> tuple[str, str]:
            return tokens[index]

        def take(expected: str | None = None) -> tuple[str, str]:
            nonlocal index
            token = tokens[index]

            if expected is not None and token[0] != expected:
                found = "end of expression" if token[0] == "EOF" else token[1]
                raise GameError(f"Expected {expected} in {label}, found {found}.")

            index += 1
            return token

        def parse_sum() -> dict[Any, Fraction]:
            value = parse_product()

            while peek()[0] in {"+", "-"}:
                operator = take()[0]
                right = parse_product()

                if operator == "-":
                    right = self._scale_parser_expression(right, Fraction(-1))

                value = self._add_parser_expressions(value, right)

            return value

        def parse_product() -> dict[Any, Fraction]:
            value = parse_unary()

            while peek()[0] == "*":
                take("*")
                value = self._multiply_parser_expressions(value, parse_unary())

            return value

        def parse_unary() -> dict[Any, Fraction]:
            token_type = peek()[0]

            if token_type == "+":
                take("+")
                return parse_unary()

            if token_type == "-":
                take("-")
                return self._scale_parser_expression(parse_unary(), Fraction(-1))

            return parse_atom()

        def parse_atom() -> dict[Any, Fraction]:
            token_type, token_value = peek()

            if token_type == "NUMBER":
                take("NUMBER")
                return {None: self._parse_fraction(token_value, label)}

            if token_type == "NAME":
                take("NAME")
                return {self._parse_path_factor(token_value, label): Fraction(1)}

            if token_type == "(":
                take("(")
                value = parse_sum()
                take(")")
                return value

            found = "end of expression" if token_type == "EOF" else token_value
            raise GameError(f"Expected a coefficient, path, or parenthesized polynomial in {label}, found {found}.")

        expression = self._clean_parser_expression(parse_sum())

        if peek()[0] != "EOF":
            found = peek()[1]
            raise GameError(f"Unexpected token {found} in {label}.")

        scalar = expression.pop(None, Fraction(0))

        if scalar:
            raise GameError(
                f"Scalar term {self._format_fraction(scalar)} in {label} is not attached to a vertex/path."
            )

        return self._clean_expression(expression)

    def _tokenize_expression(self, text: str, label: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        index = 0

        while index < len(text):
            char = text[index]

            if char.isspace():
                index += 1
                continue

            if char in "+-*()":
                tokens.append((char, char))
                index += 1
                continue

            if char.isdigit():
                start = index

                while index < len(text) and text[index].isdigit():
                    index += 1

                if index < len(text) and text[index] == "/":
                    index += 1
                    denominator_start = index

                    while index < len(text) and text[index].isdigit():
                        index += 1

                    if denominator_start == index:
                        raise GameError(f"Coefficient {text[start:index]} in {label} is not rational.")

                tokens.append(("NUMBER", text[start:index]))
                continue

            if char.isalpha():
                start = index

                while index < len(text) and (text[index].isalnum() or text[index] == "_"):
                    index += 1

                tokens.append(("NAME", text[start:index]))
                continue

            raise GameError(f"Unexpected character {char!r} in {label}.")

        tokens.append(("EOF", ""))
        return tokens

    def _parse_fraction(self, text: str, label: str) -> Fraction:
        try:
            return Fraction(text)
        except Exception as exc:
            raise GameError(f"Coefficient {text} in {label} is not rational.") from exc

    def _add_parser_expressions(
        self,
        left: dict[Any, Fraction],
        right: dict[Any, Fraction],
    ) -> dict[Any, Fraction]:
        result = dict(left)

        for path, coeff in right.items():
            result[path] = result.get(path, Fraction(0)) + coeff

        return self._clean_parser_expression(result)

    def _scale_parser_expression(
        self,
        expression: dict[Any, Fraction],
        scalar: Fraction,
    ) -> dict[Any, Fraction]:
        return self._clean_parser_expression({
            path: scalar * coeff
            for path, coeff in expression.items()
        })

    def _multiply_parser_expressions(
        self,
        left: dict[Any, Fraction],
        right: dict[Any, Fraction],
    ) -> dict[Any, Fraction]:
        result: dict[Any, Fraction] = {}

        for left_path, left_coeff in left.items():
            for right_path, right_coeff in right.items():
                if left_path is None and right_path is None:
                    product = None
                elif left_path is None:
                    product = right_path
                elif right_path is None:
                    product = left_path
                else:
                    product = self.compose_paths(left_path, right_path)

                    if product is None:
                        continue

                result[product] = result.get(product, Fraction(0)) + left_coeff * right_coeff

        return self._clean_parser_expression(result)

    def _clean_parser_expression(
        self,
        expression: dict[Any, Fraction],
    ) -> dict[Any, Fraction]:
        return {
            path: coeff
            for path, coeff in expression.items()
            if coeff != 0
        }

    def _parse_path_factor(self, text: str, label: str) -> tuple[str, ...]:
        if text in self.arrows:
            return (text,)

        if text.startswith("e_"):
            vertex = text[2:]

            if vertex in self.vertices:
                return (self._id_token(vertex),)

        if all(
            len(char) == 1 and char in self.arrows
            for char in text
        ):
            path: tuple[str, ...] | None = None

            for char in text:
                factor = (char,)
                path = factor if path is None else self.compose_paths(path, factor)

                if path is None:
                    raise GameError(f"Factor {text} in {label} is not composable.")

            if path is not None:
                return path

        raise GameError(f"Unknown arrow/path factor {text} in {label}.")

    def _expression_has_endpoints(
        self,
        expression: dict[tuple[str, ...], Fraction],
        source: str,
        target: str,
    ) -> bool:
        return all(self.path_endpoints(path) == (source, target) for path in expression)

    def _expression_endpoints(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> tuple[str, str] | None:
        endpoints = None

        for path in expression:
            path_endpoints = self.path_endpoints(path)

            if path_endpoints is None:
                return None

            if endpoints is None:
                endpoints = path_endpoints
            elif endpoints != path_endpoints:
                return None

        return endpoints

    def path_endpoints(self, path: tuple[str, ...]) -> tuple[str, str] | None:
        if self._is_id_path(path):
            vertex = self._id_vertex(path)
            return (vertex, vertex)

        if not path:
            return None

        first = self.arrows[path[0]]
        last = self.arrows[path[-1]]
        return (first["source"], last["target"])

    def compose_paths(
        self,
        left: tuple[str, ...],
        right: tuple[str, ...],
    ) -> tuple[str, ...] | None:
        if self._is_id_path(left):
            vertex = self._id_vertex(left)
            right_endpoints = self.path_endpoints(right)
            return right if right_endpoints and right_endpoints[0] == vertex else None

        if self._is_id_path(right):
            vertex = self._id_vertex(right)
            left_endpoints = self.path_endpoints(left)
            return left if left_endpoints and left_endpoints[1] == vertex else None

        left_endpoints = self.path_endpoints(left)
        right_endpoints = self.path_endpoints(right)

        if left_endpoints is None or right_endpoints is None:
            return None

        if left_endpoints[1] != right_endpoints[0]:
            return None

        return left + right

    def multiply_expressions(
        self,
        left: dict[tuple[str, ...], Fraction],
        right: dict[tuple[str, ...], Fraction],
    ) -> dict[tuple[str, ...], Fraction]:
        result: dict[tuple[str, ...], Fraction] = {}

        for left_path, left_coeff in left.items():
            for right_path, right_coeff in right.items():
                product = self.compose_paths(left_path, right_path)

                if product is None:
                    continue

                result[product] = result.get(product, Fraction(0)) + left_coeff * right_coeff

        return self._clean_expression(result)

    def reduce_expression(
        self,
        expression: dict[tuple[str, ...], Fraction],
        max_steps: int = 2000,
    ) -> dict[tuple[str, ...], Fraction]:
        expression = self._clean_expression(expression)
        steps = 0

        while steps < max_steps:
            reduction = self._first_reduction(expression)

            if reduction is None:
                break

            path, coeff, rule, start = reduction
            steps += 1
            expression[path] = expression.get(path, Fraction(0)) - coeff

            if expression.get(path) == 0:
                expression.pop(path, None)

            prefix = path[:start]
            suffix = path[start + len(rule["leading"]):]

            for replacement_path, replacement_coeff in rule["replacement"].items():
                replaced = replacement_path

                if prefix:
                    replaced = self.compose_paths(prefix, replaced)

                if replaced is None:
                    continue

                if suffix:
                    replaced = self.compose_paths(replaced, suffix)

                if replaced is None:
                    continue

                expression[replaced] = (
                    expression.get(replaced, Fraction(0))
                    + coeff * replacement_coeff
                )

            expression = self._clean_expression(expression)
        else:
            self.warnings.append("Reduction stopped at the step limit; the oriented rules may not terminate.")

        return expression

    def _first_reduction(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> tuple[tuple[str, ...], Fraction, dict[str, Any], int] | None:
        for path in sorted(expression, key=self._path_order_key, reverse=True):
            if self._is_id_path(path):
                continue

            for rule in self.rules:
                start = self._find_subpath(path, rule["leading"])

                if start is not None:
                    return (path, expression[path], rule, start)

        return None

    def _find_subpath(
        self,
        path: tuple[str, ...],
        subpath: tuple[str, ...],
    ) -> int | None:
        if self._is_id_path(path) or self._is_id_path(subpath):
            return None

        width = len(subpath)

        if width == 0 or width > len(path):
            return None

        for start in range(0, len(path) - width + 1):
            if path[start:start + width] == subpath:
                return start

        return None

    def differential_expression(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> dict[tuple[str, ...], Fraction]:
        result: dict[tuple[str, ...], Fraction] = {}

        for path, coeff in expression.items():
            d_path = self.differential_path(path)

            for d_term, d_coeff in d_path.items():
                result[d_term] = result.get(d_term, Fraction(0)) + coeff * d_coeff

        return self._clean_expression(result)

    def differential_path(
        self,
        path: tuple[str, ...],
    ) -> dict[tuple[str, ...], Fraction]:
        if self._is_id_path(path):
            return {}

        result: dict[tuple[str, ...], Fraction] = {}
        prefix_degree: int | None = 0

        for index, arrow_name in enumerate(path):
            d_arrow = self.differentials.get(arrow_name, {})
            arrow_degree = self.arrows[arrow_name].get("degree")

            if not d_arrow:
                prefix_degree = self._add_prefix_degree(prefix_degree, arrow_degree)
                continue

            if prefix_degree is None:
                raise GameError(
                    f"Cannot determine the Leibniz sign in d({self.path_label(path)}) "
                    "because a preceding arrow has undetermined degree."
                )

            left = path[:index]
            right = path[index + 1:]
            term = d_arrow

            if left:
                term = self.multiply_expressions({left: Fraction(1)}, term)

            if right:
                term = self.multiply_expressions(term, {right: Fraction(1)})

            sign = Fraction(-1 if prefix_degree % 2 else 1)

            for term_path, term_coeff in term.items():
                result[term_path] = result.get(term_path, Fraction(0)) + sign * term_coeff

            prefix_degree = self._add_prefix_degree(prefix_degree, arrow_degree)

        return self._clean_expression(result)

    def _add_prefix_degree(self, prefix_degree: int | None, arrow_degree: int | None) -> int | None:
        if prefix_degree is None or arrow_degree is None:
            return None

        return prefix_degree + int(arrow_degree)

    def _basis_by_length(self, max_length: int) -> list[dict[str, Any]]:
        groups = [{
            "length": 0,
            "paths": [self._serialize_path((self._id_token(vertex),)) for vertex in self.vertices],
        }]
        current = [(name,) for name in self.arrow_order]

        for length in range(1, max_length + 1):
            normal_paths = []
            next_paths = []

            for path in current:
                reduced = self.reduce_expression({path: Fraction(1)})

                if len(reduced) == 1 and reduced.get(path) == 1:
                    normal_paths.append(path)

                for arrow_name in self.arrow_order:
                    product = self.compose_paths(path, (arrow_name,))

                    if product is not None:
                        next_paths.append(product)

            groups.append({
                "length": length,
                "paths": [self._serialize_path(path) for path in normal_paths],
            })
            current = next_paths

        return groups

    def _finite_dimensional_report(self) -> dict[str, Any]:
        forbidden = [
            rule["leading"]
            for rule in self.rules
            if not self._is_id_path(rule["leading"])
        ]
        max_forbidden = max((len(path) for path in forbidden), default=0)
        max_suffix = max(0, max_forbidden - 1)
        state_limit = 5000
        start_states = [(vertex, ()) for vertex in self.vertices]
        adjacency: dict[tuple[str, tuple[str, ...]], list[tuple[tuple[str, tuple[str, ...]], str]]] = {}
        seen = set(start_states)
        queue = list(start_states)

        while queue:
            if len(seen) > state_limit:
                return {
                    "status": "unknown",
                    "isFinite": None,
                    "method": self._finite_dimensional_method(),
                    "stateCount": len(seen),
                    "transitionCount": sum(len(edges) for edges in adjacency.values()),
                    "reason": "state limit reached while building the normal-path automaton",
                }

            state = queue.pop(0)
            vertex, suffix = state
            edges = []

            for arrow_name in self.arrow_order:
                arrow = self.arrows[arrow_name]

                if arrow["source"] != vertex:
                    continue

                candidate_suffix = suffix + (arrow_name,)

                if self._ends_with_forbidden_leading_path(candidate_suffix, forbidden):
                    continue

                next_suffix = candidate_suffix[-max_suffix:] if max_suffix else ()
                next_state = (arrow["target"], next_suffix)
                edges.append((next_state, arrow_name))

                if next_state not in seen:
                    seen.add(next_state)
                    queue.append(next_state)

            adjacency[state] = edges

        cycle_state = self._reachable_cycle_state(adjacency, start_states)

        if cycle_state is not None:
            return {
                "status": "infinite",
                "isFinite": False,
                "method": self._finite_dimensional_method(),
                "stateCount": len(seen),
                "transitionCount": sum(len(edges) for edges in adjacency.values()),
                "cycleState": self._automaton_state_label(cycle_state),
                "caveat": self._finite_dimensional_caveat(),
            }

        normal_path_count, longest_length = self._count_acyclic_normal_paths(adjacency, start_states)
        return {
            "status": "finite",
            "isFinite": True,
            "method": self._finite_dimensional_method(),
            "normalPathCount": normal_path_count,
            "longestNormalPathLength": longest_length,
            "stateCount": len(seen),
            "transitionCount": sum(len(edges) for edges in adjacency.values()),
            "caveat": self._finite_dimensional_caveat(),
        }

    def _ends_with_forbidden_leading_path(
        self,
        suffix: tuple[str, ...],
        forbidden: list[tuple[str, ...]],
    ) -> bool:
        return any(
            len(path) <= len(suffix) and suffix[-len(path):] == path
            for path in forbidden
        )

    def _reachable_cycle_state(
        self,
        adjacency: dict[tuple[str, tuple[str, ...]], list[tuple[tuple[str, tuple[str, ...]], str]]],
        start_states: list[tuple[str, tuple[str, ...]]],
    ) -> tuple[str, tuple[str, ...]] | None:
        color: dict[tuple[str, tuple[str, ...]], int] = {}

        def visit(state: tuple[str, tuple[str, ...]]) -> tuple[str, tuple[str, ...]] | None:
            color[state] = 1

            for next_state, _arrow_name in adjacency.get(state, []):
                if color.get(next_state) == 1:
                    return next_state

                if color.get(next_state) == 2:
                    continue

                cycle = visit(next_state)

                if cycle is not None:
                    return cycle

            color[state] = 2
            return None

        for state in start_states:
            if color.get(state):
                continue

            cycle = visit(state)

            if cycle is not None:
                return cycle

        return None

    def _count_acyclic_normal_paths(
        self,
        adjacency: dict[tuple[str, tuple[str, ...]], list[tuple[tuple[str, tuple[str, ...]], str]]],
        start_states: list[tuple[str, tuple[str, ...]]],
    ) -> tuple[int, int]:
        visited = set()
        order = []

        def visit(state: tuple[str, tuple[str, ...]]) -> None:
            if state in visited:
                return

            visited.add(state)

            for next_state, _arrow_name in adjacency.get(state, []):
                visit(next_state)

            order.append(state)

        for state in start_states:
            visit(state)

        counts = {state: 1 for state in start_states}
        lengths = {state: 0 for state in start_states}
        total = len(start_states)
        longest = 0

        for state in reversed(order):
            state_count = counts.get(state, 0)
            state_length = lengths.get(state, 0)

            for next_state, _arrow_name in adjacency.get(state, []):
                counts[next_state] = counts.get(next_state, 0) + state_count
                next_length = state_length + 1
                lengths[next_state] = max(lengths.get(next_state, 0), next_length)
                total += state_count
                longest = max(longest, next_length)

        return total, longest

    def _automaton_state_label(self, state: tuple[str, tuple[str, ...]]) -> str:
        vertex, suffix = state
        suffix_label = "*".join(suffix) if suffix else "empty"
        return f"{vertex}; suffix {suffix_label}"

    def _finite_dimensional_method(self) -> str:
        return "reachable-cycle test in the automaton of composable normal paths avoiding oriented leading relation paths"

    def _finite_dimensional_caveat(self) -> str:
        return (
            "This is exact for the currently oriented leading-path normal basis; "
            "for noncommutative nonmonomial systems it depends on the oriented rules behaving as a complete reduction system."
        )

    def _projective_modules_report(
        self,
        finite_dimensional: dict[str, Any],
        basis_display_length: int,
    ) -> list[dict[str, Any]]:
        basis_groups = self._normal_paths_by_length(basis_display_length)
        return [
            DGRightProjectiveModule(vertex).report(
                self,
                basis_groups,
                finite_dimensional,
            )
            for vertex in self.vertices
        ]

    def _module_presentation_report(self, finite_dimensional: dict[str, Any]) -> dict[str, Any] | None:
        raw = self.payload.get("modulePresentation")

        if not isinstance(raw, dict):
            return None

        generators = self._load_module_generators(raw.get("generators", []))
        rows = self._load_module_rows(raw.get("rows", []), generators)
        presentation = DGRightModulePresentation(generators, rows)
        report: dict[str, Any] = {
            "orientation": "Right module presentation coker(F1 -> F0) with F0 summands e_v A.",
            "entryConvention": "Matrix entry in row r and column c must lie in e_{generator(c)} A e_{relation(r)}.",
            "generators": presentation.generators,
            "rows": presentation.row_displays(self),
            "matrixShape": presentation.matrix_shape(),
            "dimensionKnown": False,
            "basis": [],
            "messages": [],
        }

        if not presentation.generators:
            report["messages"].append("No module generators entered.")
            return report

        if finite_dimensional.get("status") != "finite":
            report["messages"].append("Module vector-space basis is available after the algebra basis is finite.")
            return report

        longest = int(finite_dimensional.get("longestNormalPathLength") or 0)
        algebra_basis = [
            path
            for group in self._normal_paths_by_length(longest)
            for path in group
        ]
        module_basis = [
            (generator_index, path)
            for generator_index, generator in enumerate(presentation.generators)
            for path in algebra_basis
            if self.path_endpoints(path) and self.path_endpoints(path)[0] == generator["vertex"]
        ]
        basis_index = {
            key: index
            for index, key in enumerate(module_basis)
        }
        relation_vectors = []

        for row in presentation.rows:
            multipliers = [
                path
                for path in algebra_basis
                if self.path_endpoints(path) and self.path_endpoints(path)[0] == row["vertex"]
            ]

            for multiplier in multipliers:
                vector: dict[int, Fraction] = {}

                for generator_index, entry in enumerate(row["entries"]):
                    product = self.multiply_expressions(entry, {multiplier: Fraction(1)})
                    reduced = self.reduce_expression(product)

                    for path, coeff in reduced.items():
                        key = (generator_index, path)

                        if key not in basis_index:
                            self.warnings.append(
                                "A module relation reduced to a path outside the displayed finite basis."
                            )
                            continue

                        column = basis_index[key]
                        vector[column] = vector.get(column, Fraction(0)) + coeff

                vector = {
                    column: coeff
                    for column, coeff in vector.items()
                    if coeff != 0
                }

                if vector:
                    relation_vectors.append(vector)

        rank, pivot_columns = self._matrix_rank_and_pivots(relation_vectors, len(module_basis))
        surviving = [
            key
            for index, key in enumerate(module_basis)
            if index not in pivot_columns
        ]
        report.update({
            "dimensionKnown": True,
            "freeBasisCount": len(module_basis),
            "relationVectorCount": len(relation_vectors),
            "relationRank": rank,
            "dimension": len(module_basis) - rank,
            "basis": [
                self._serialize_module_basis_item(presentation.generators, key)
                for key in surviving
            ],
            "messages": [
                (
                    f"Computed coker basis: {len(module_basis)} free basis element(s), "
                    f"rank {rank} relation span, dimension {len(module_basis) - rank}."
                )
            ],
        })
        return report

    def _load_module_generators(self, raw: Any) -> list[dict[str, Any]]:
        if not isinstance(raw, list):
            raise GameError("Module generators must be a list.")

        vertex_set = set(self.vertices)
        seen = set()
        generators = []

        for index, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                raise GameError("Each module generator must be an object.")

            name = clean_name(item.get("name") or f"m{index}", f"Module generator {index}")

            if name in seen:
                raise GameError(f"Module generator {name} is listed more than once.")

            seen.add(name)
            vertex = clean_name(item.get("vertex"), f"Vertex of module generator {name}")

            if vertex not in vertex_set:
                raise GameError(f"Module generator {name} uses unknown vertex {vertex}.")

            generators.append({
                "name": name,
                "vertex": vertex,
                "degree": self._parse_degree(item.get("degree")),
            })

        return generators

    def _load_module_rows(
        self,
        raw: Any,
        generators: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not isinstance(raw, list):
            raise GameError("Module presentation rows must be a list.")

        vertex_set = set(self.vertices)
        rows = []

        for row_index, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                raise GameError("Each module presentation row must be an object.")

            name = str(item.get("name") or f"r{row_index}").strip() or f"r{row_index}"
            vertex = clean_name(item.get("vertex"), f"Vertex of module relation {name}")

            if vertex not in vertex_set:
                raise GameError(f"Module relation {name} uses unknown vertex {vertex}.")

            entries = item.get("entries", [])

            if not isinstance(entries, list):
                raise GameError(f"Entries of module relation {name} must be a list.")

            if len(entries) != len(generators):
                raise GameError(
                    f"Module relation {name} has {len(entries)} entries, "
                    f"but there are {len(generators)} module generators."
                )

            parsed_entries = []

            for column_index, raw_entry in enumerate(entries):
                generator = generators[column_index]
                text = str(raw_entry or "").strip()
                expression = self._parse_expression(text, f"module row {name}, column {generator['name']}") if text else {}

                if expression and not self._expression_has_endpoints(
                    expression,
                    generator["vertex"],
                    vertex,
                ):
                    raise GameError(
                        f"Module matrix entry ({name}, {generator['name']}) must be a linear combination "
                        f"of paths from {generator['vertex']} to {vertex}."
                    )

                parsed_entries.append(expression)

            rows.append({
                "name": name,
                "vertex": vertex,
                "entries": parsed_entries,
            })

        return rows

    def _normal_paths_by_length(self, max_length: int) -> list[list[tuple[str, ...]]]:
        groups: list[list[tuple[str, ...]]] = [
            [(self._id_token(vertex),) for vertex in self.vertices]
        ]
        current = [(name,) for name in self.arrow_order]

        for _length in range(1, max_length + 1):
            normal_paths = []
            next_paths = []

            for path in current:
                reduced = self.reduce_expression({path: Fraction(1)})

                if len(reduced) == 1 and reduced.get(path) == 1:
                    normal_paths.append(path)

                for arrow_name in self.arrow_order:
                    product = self.compose_paths(path, (arrow_name,))

                    if product is not None:
                        next_paths.append(product)

            groups.append(normal_paths)
            current = next_paths

        return groups

    def _matrix_rank_and_pivots(
        self,
        vectors: list[dict[int, Fraction]],
        width: int,
    ) -> tuple[int, set[int]]:
        rows = [
            {
                column: coeff
                for column, coeff in vector.items()
                if coeff != 0
            }
            for vector in vectors
            if any(coeff != 0 for coeff in vector.values())
        ]
        rank = 0
        pivot_columns: set[int] = set()
        row_index = 0

        for column in range(width):
            pivot_index = None

            for candidate in range(row_index, len(rows)):
                if rows[candidate].get(column, Fraction(0)) != 0:
                    pivot_index = candidate
                    break

            if pivot_index is None:
                continue

            rows[row_index], rows[pivot_index] = rows[pivot_index], rows[row_index]
            pivot = rows[row_index][column]
            rows[row_index] = {
                item_column: coeff / pivot
                for item_column, coeff in rows[row_index].items()
                if coeff != 0
            }

            for other_index in range(len(rows)):
                if other_index == row_index:
                    continue

                factor = rows[other_index].get(column, Fraction(0))

                if factor == 0:
                    continue

                for item_column, coeff in rows[row_index].items():
                    rows[other_index][item_column] = rows[other_index].get(item_column, Fraction(0)) - factor * coeff

                    if rows[other_index].get(item_column) == 0:
                        rows[other_index].pop(item_column, None)

            pivot_columns.add(column)
            rank += 1
            row_index += 1

            if row_index >= len(rows):
                break

        return rank, pivot_columns

    def _serialize_module_basis_item(
        self,
        generators: list[dict[str, Any]],
        key: tuple[int, tuple[str, ...]],
    ) -> dict[str, Any]:
        generator_index, path = key
        generator = generators[generator_index]
        path_label = self.path_label(path)
        label = generator["name"] if self._is_id_path(path) else f"{generator['name']}*{path_label}"
        endpoints = self.path_endpoints(path)
        return {
            "label": label,
            "generator": generator["name"],
            "generatorVertex": generator["vertex"],
            "path": path_label,
            "source": endpoints[0] if endpoints else "",
            "target": endpoints[1] if endpoints else "",
        }

    def _relation_differential_checks(self) -> list[dict[str, Any]]:
        checks = []

        for relation in self.relations:
            try:
                differential = self.differential_expression(relation["expression"])
                normal = self.reduce_expression(differential)
                checks.append({
                    "relation": relation["line"],
                    "generator": relation["text"],
                    "differential": self.expression_display(differential),
                    "normalForm": self.expression_display(normal),
                    "isZero": not bool(normal),
                    "isKnown": True,
                })
            except GameError as exc:
                checks.append({
                    "relation": relation["line"],
                    "generator": relation["text"],
                    "differential": "unknown",
                    "normalForm": "unknown",
                    "isZero": False,
                    "isKnown": False,
                    "error": str(exc),
                })

        return checks

    def _dg_ideal_report(self, relation_checks: list[dict[str, Any]]) -> dict[str, Any]:
        failures = [
            check
            for check in relation_checks
            if check.get("isKnown", True) and not check["isZero"]
        ]
        unknown = [
            check
            for check in relation_checks
            if not check.get("isKnown", True)
        ]
        current_lines = [relation["text"] for relation in self.relations]
        seen = {
            self.expression_display(relation["expression"])
            for relation in self.relations
        } | {line.strip() for line in current_lines}
        suggestions = []

        for check in failures:
            normal = check["normalForm"]

            if normal == "0" or normal in seen:
                continue

            seen.add(normal)
            suggestions.append({
                "relation": check["relation"],
                "generator": check["generator"],
                "differential": check["differential"],
                "normalForm": normal,
            })

        status = "closed"

        if failures:
            status = "notClosed"
        elif unknown:
            status = "unknown"

        return {
            "isDG": status == "closed",
            "status": status,
            "membershipTest": "normal-form reduction by the oriented relation rules",
            "failures": failures,
            "unknown": unknown,
            "suggestedGenerators": suggestions,
            "externalRelationsText": "\n".join(current_lines + [
                item["normalForm"]
                for item in suggestions
            ]),
        }

    def _d_squared_checks(self) -> list[dict[str, Any]]:
        checks = []

        for name in self.arrow_order:
            try:
                differential = self.differentials.get(name, {})
                d_squared = self.differential_expression(differential)
                normal = self.reduce_expression(d_squared)
                checks.append({
                    "arrow": name,
                    "differential": self.expression_display(differential),
                    "dSquared": self.expression_display(d_squared),
                    "normalForm": self.expression_display(normal),
                    "isZero": not bool(normal),
                    "isKnown": True,
                })
            except GameError as exc:
                checks.append({
                    "arrow": name,
                    "differential": self.expression_display(self.differentials.get(name, {})),
                    "dSquared": "unknown",
                    "normalForm": "unknown",
                    "isZero": False,
                    "isKnown": False,
                    "error": str(exc),
                })

        return checks

    def _summary_messages(
        self,
        max_length: int,
        relation_checks: list[dict[str, Any]],
        d_squared_checks: list[dict[str, Any]],
        finite_dimensional: dict[str, Any],
    ) -> list[str]:
        relation_unknown = sum(1 for check in relation_checks if not check.get("isKnown", True))
        d_squared_unknown = sum(1 for check in d_squared_checks if not check.get("isKnown", True))
        relation_failures = sum(
            1
            for check in relation_checks
            if check.get("isKnown", True) and not check["isZero"]
        )
        d_squared_failures = sum(
            1
            for check in d_squared_checks
            if check.get("isKnown", True) and not check["isZero"]
        )
        messages = [
            (
                f"Analyzed {len(self.vertices)} vertices, {len(self.arrow_order)} arrows, "
                f"{len(self.relations)} relations through path length {max_length}."
            )
        ]

        if relation_failures:
            messages.append(f"{relation_failures} relation differential(s) are nonzero modulo the oriented rules.")
        elif relation_unknown:
            messages.append(f"{relation_unknown} relation differential(s) need undetermined grading signs.")
        else:
            messages.append("All relation differentials reduce to zero.")

        if d_squared_failures:
            messages.append(f"{d_squared_failures} arrow differential(s) have nonzero d^2 modulo the oriented rules.")
        elif d_squared_unknown:
            messages.append(f"{d_squared_unknown} arrow d^2 check(s) need undetermined grading signs.")
        else:
            messages.append("All arrow d^2 checks reduce to zero.")

        if finite_dimensional.get("status") == "finite":
            messages.append(
                f"The normal-path automaton is finite with {finite_dimensional.get('normalPathCount', 0)} normal path(s)."
            )
        elif finite_dimensional.get("status") == "infinite":
            messages.append("The normal-path automaton has a reachable cycle, so the current normal basis is infinite.")
        else:
            messages.append("Finite-dimensional detection was inconclusive for the current normal-path automaton.")

        return messages

    def _max_length(self) -> int:
        try:
            value = int(self.payload.get("maxLength", 5))
        except (TypeError, ValueError):
            value = 5

        return max(0, min(value, 10))

    def _serialize_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        return {
            "relation": rule["relation"]["line"],
            "leading": self.path_label(rule["leading"]),
            "leadingPath": self._serialize_path(rule["leading"]),
            "replacement": self.expression_display(rule["replacement"]),
            "replacementTerms": self.serialize_expression(rule["replacement"]),
        }

    def serialize_expression(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> list[dict[str, Any]]:
        return [
            {
                "coefficient": self._format_fraction(coeff),
                "path": self.path_label(path),
                "source": endpoints[0] if endpoints else "",
                "target": endpoints[1] if endpoints else "",
                "arrows": list(path),
            }
            for path, coeff in sorted(
                expression.items(),
                key=lambda item: self._path_order_key(item[0]),
                reverse=True,
            )
            for endpoints in (self.path_endpoints(path),)
        ]

    def expression_display(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> str:
        expression = self._clean_expression(expression)

        if not expression:
            return "0"

        pieces = []

        for path, coeff in sorted(
            expression.items(),
            key=lambda item: self._path_order_key(item[0]),
            reverse=True,
        ):
            sign = -1 if coeff < 0 else 1
            abs_coeff = abs(coeff)
            path_label = self.path_label(path)

            if abs_coeff == 1:
                body = path_label
            else:
                body = f"{self._format_fraction(abs_coeff)}*{path_label}"

            pieces.append((sign, body))

        text = ""

        for index, (sign, body) in enumerate(pieces):
            if index == 0:
                text += f"-{body}" if sign < 0 else body
            else:
                text += f" {'-' if sign < 0 else '+'} {body}"

        return text

    def path_label(self, path: tuple[str, ...]) -> str:
        if self._is_id_path(path):
            return "e_" + self._id_vertex(path)

        return "*".join(path) if path else "0"

    def _serialize_path(self, path: tuple[str, ...]) -> dict[str, Any]:
        endpoints = self.path_endpoints(path)
        return {
            "label": self.path_label(path),
            "arrows": [] if self._is_id_path(path) else list(path),
            "source": endpoints[0] if endpoints else "",
            "target": endpoints[1] if endpoints else "",
        }

    def _clean_expression(
        self,
        expression: dict[tuple[str, ...], Fraction],
    ) -> dict[tuple[str, ...], Fraction]:
        return {
            path: coeff
            for path, coeff in expression.items()
            if coeff != 0
        }

    def _path_order_key(self, path: tuple[str, ...]) -> tuple[int, tuple[str, ...]]:
        return (self._path_length(path), tuple(path))

    def _path_length(self, path: tuple[str, ...]) -> int:
        return 0 if self._is_id_path(path) else len(path)

    def _id_token(self, vertex: str) -> str:
        return self.ID_PREFIX + vertex

    def _is_id_path(self, path: tuple[str, ...]) -> bool:
        return len(path) == 1 and path[0].startswith(self.ID_PREFIX)

    def _id_vertex(self, path: tuple[str, ...]) -> str:
        return path[0][len(self.ID_PREFIX):]

    def _format_fraction(self, value: Fraction) -> str:
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def analyze_dg_relations(payload: dict[str, Any]) -> dict[str, Any]:
    return DGQuiverRelationsAnalyzer(payload).analyze()


def preview_dg_polynomial(payload: dict[str, Any]) -> dict[str, Any]:
    analyzer = DGQuiverRelationsAnalyzer(payload)
    analyzer._load_vertices()
    analyzer._load_arrows()
    analyzer._load_differentials()

    text = str(payload.get("polynomial") or "").strip()
    expression = analyzer._parse_expression(text, "polynomial") if text else {}
    endpoints = analyzer._expression_endpoints(expression) if expression else None

    return {
        "input": text,
        "display": analyzer.expression_display(expression),
        "terms": analyzer.serialize_expression(expression),
        "isZero": not bool(expression),
        "isUniform": bool(endpoints) or not bool(expression),
        "source": endpoints[0] if endpoints else "",
        "target": endpoints[1] if endpoints else "",
    }


CANCELLABLE_PATH_LABELS = {
    "/api/import": "load quiver",
    "/api/attach-mp": "resolve cell",
    "/api/attach-bridge": "resolve bridge",
    "/api/generate": "generate Massey products",
    "/api/run": "run search",
    "/api/undo": "undo/replay",
    "/api/autocomplete/plan": "autocomplete plan",
    "/api/autocomplete/plan-selected": "selected autocomplete plan",
    "/api/autocomplete/apply": "autocomplete apply",
    "/api/autocomplete/apply-selected": "selected autocomplete apply",
}

CANCELLER = CancellationManager()
ENGINE = GameEngine()


class UIRequestHandler(BaseHTTPRequestHandler):
    server_version = "AinfGameUI/1.0"

    def log_message(self, format, *args):  # noqa: A003 - inherited name
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return

        if path == "/api/state":
            self._send_json(ENGINE.state())
            return

        if path == "/api/primitive-graph":
            self._send_json(ENGINE.primitive_graph())
            return

        if path == "/api/cyclic-class-graph":
            self._send_json(ENGINE.cyclic_class_graph())
            return

        if path == "/api/export":
            self._send_json(ENGINE.export_save())
            return

        static_path = STATIC_DIR / path.lstrip("/")

        if static_path.is_file() and static_path.resolve().is_relative_to(STATIC_DIR.resolve()):
            self._send_file(static_path, self._content_type(static_path))
            return

        self._send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            payload = self._read_json()

            if path == "/api/stop":
                if payload.get("force"):
                    self._send_json({"stop": CANCELLER.request_force_stop()})
                else:
                    self._send_json({"stop": CANCELLER.request_stop()})
                return

            label = CANCELLABLE_PATH_LABELS.get(path)

            if label:
                with CANCELLER.operation(label):
                    response = self._dispatch_post(path, payload)
            else:
                response = self._dispatch_post(path, payload)

            self._send_json(response)
        except OperationCancelled:
            state = ENGINE.stopped_state()
            state["error"] = "Stopped current computation."
            self._send_json(state, HTTPStatus.CONFLICT)
        except FileNotFoundError as exc:
            self._send_json({"error": str(exc)}, HTTPStatus.NOT_FOUND)
        except GameError as exc:
            state = ENGINE.state()
            state["error"] = str(exc)
            self._send_json(state, HTTPStatus.BAD_REQUEST)
        except Exception as exc:  # pragma: no cover - sent to browser while debugging
            state = ENGINE.state()
            state["error"] = str(exc)
            state["traceback"] = traceback.format_exc()
            self._send_json(state, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _dispatch_post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if path == "/api/reset":
            return ENGINE.reset()

        if path == "/api/import":
            return ENGINE.import_save(payload)

        if path == "/api/save":
            return ENGINE.save_current_quiver(payload)

        if path == "/api/quiver-name":
            return ENGINE.update_quiver_name(payload)

        if path == "/api/vertices":
            return ENGINE.add_vertices(payload.get("vertices", ""))

        if path == "/api/arrows":
            return ENGINE.add_arrow(payload)

        if path == "/api/generators/remove":
            return ENGINE.remove_generator(payload)

        if path == "/api/generators/order":
            return ENGINE.set_generator_order(payload)

        if path == "/api/attach-mp":
            return ENGINE.attach_mp_cell(payload)

        if path == "/api/attach-bridge":
            return ENGINE.attach_bridge(payload)

        if path == "/api/generate":
            return ENGINE.generate(payload)

        if path == "/api/run":
            return ENGINE.run(payload)

        if path == "/api/undo":
            return ENGINE.undo(auto_run=bool(payload.get("autoRun")), data=payload)

        if path == "/api/settings":
            return ENGINE.update_settings(payload)

        if path == "/api/dg-relations/analyze":
            return analyze_dg_relations(payload)

        if path == "/api/dg-relations/polynomial":
            return preview_dg_polynomial(payload)

        if path == "/api/autocomplete/plan":
            return ENGINE.autocomplete_plan(payload)

        if path == "/api/autocomplete/plan-selected":
            return ENGINE.autocomplete_plan_selected(payload)

        if path == "/api/autocomplete/apply":
            return ENGINE.autocomplete_apply(payload)

        if path == "/api/autocomplete/apply-selected":
            return ENGINE.autocomplete_apply_selected(payload)

        raise FileNotFoundError("Not found.")

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")

        if length == 0:
            return {}

        raw = self.rfile.read(length)

        if not raw:
            return {}

        return json.loads(raw.decode("utf-8"))

    def _send_json(self, data: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        payload = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_file(self, path: Path, content_type: str) -> None:
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _content_type(self, path: Path) -> str:
        suffix = path.suffix.lower()

        if suffix == ".css":
            return "text/css; charset=utf-8"

        if suffix == ".html":
            return "text/html; charset=utf-8"

        if suffix == ".js":
            return "text/javascript; charset=utf-8"

        if suffix == ".svg":
            return "image/svg+xml"

        return "application/octet-stream"


def find_port(preferred: int) -> int:
    for port in range(preferred, preferred + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue

            return port

    raise RuntimeError("No free local port found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the A_infinity game UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    port = find_port(args.port)
    server = ThreadingHTTPServer((args.host, port), UIRequestHandler)
    url = f"http://{args.host}:{port}"
    print(f"A_infinity game UI running at {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
