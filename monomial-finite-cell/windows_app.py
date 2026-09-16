"""Native Windows window for the monomial finite-cell game."""

from __future__ import annotations

import json
import sys
import threading
from urllib.request import urlopen

from monomial_finite_cell_game import create_server


APP_NAME = "Monomial Finite Cell Game"


def start_game_server():
    """Start the private game server and return it with its base URL."""

    server = create_server("127.0.0.1", 0)
    thread = threading.Thread(
        target=server.serve_forever,
        name="monomial-game-server",
        daemon=True,
    )
    thread.start()
    host, port = server.server_address[:2]
    return server, thread, f"http://{host}:{port}"


def smoke_test() -> int:
    """Exercise bundled resources and the HTTP API without opening a window."""

    server, thread, url = start_game_server()

    try:
        with urlopen(f"{url}/api/state", timeout=20) as response:
            state = json.load(response)
        assert state["game"]["mode"] == "monomial-finite-cell"
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def run_native_app() -> int:
    """Run the game in a native Edge WebView2 window."""

    import webview  # type: ignore[import-not-found]

    server, thread, url = start_game_server()

    try:
        webview.create_window(
            APP_NAME,
            url,
            width=1280,
            height=820,
            min_size=(960, 640),
        )
        webview.start(gui="edgechromium", private_mode=True)
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main() -> int:
    if "--smoke-test" in sys.argv:
        return smoke_test()
    return run_native_app()


if __name__ == "__main__":
    raise SystemExit(main())
