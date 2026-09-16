"""Native macOS window for the monomial finite-cell game."""

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
        print(json.dumps({"ok": True, "url": url, "game": state["game"]["name"]}))
        return 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def run_native_app() -> int:
    """Run the game in a native WKWebView and stop its server on exit."""

    from Cocoa import (  # type: ignore[import-not-found]
        NSApplication,
        NSApplicationActivationPolicyRegular,
        NSBackingStoreBuffered,
        NSMakeRect,
        NSMenu,
        NSMenuItem,
        NSWindow,
        NSWindowStyleMaskClosable,
        NSWindowStyleMaskMiniaturizable,
        NSWindowStyleMaskResizable,
        NSWindowStyleMaskTitled,
        NSObject,
    )
    from Foundation import NSURL, NSURLRequest  # type: ignore[import-not-found]
    from WebKit import WKWebView, WKWebViewConfiguration  # type: ignore[import-not-found]

    server, thread, url = start_game_server()

    class AppDelegate(NSObject):
        def applicationDidFinishLaunching_(self, notification):
            frame = NSMakeRect(0.0, 0.0, 1280.0, 820.0)
            style = (
                NSWindowStyleMaskTitled
                | NSWindowStyleMaskClosable
                | NSWindowStyleMaskMiniaturizable
                | NSWindowStyleMaskResizable
            )
            self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                frame,
                style,
                NSBackingStoreBuffered,
                False,
            )
            self.window.setTitle_(APP_NAME)
            self.window.setMinSize_((960.0, 640.0))
            self.window.center()

            configuration = WKWebViewConfiguration.alloc().init()
            self.webview = WKWebView.alloc().initWithFrame_configuration_(
                frame,
                configuration,
            )
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(url))
            self.webview.loadRequest_(request)
            self.window.setContentView_(self.webview)
            self.window.makeKeyAndOrderFront_(None)
            NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

        def applicationShouldTerminateAfterLastWindowClosed_(self, application):
            return True

        def applicationWillTerminate_(self, notification):
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

    main_menu = NSMenu.alloc().init()
    application_menu_item = NSMenuItem.alloc().init()
    main_menu.addItem_(application_menu_item)
    application_menu = NSMenu.alloc().init()
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        f"Quit {APP_NAME}",
        "terminate:",
        "q",
    )
    application_menu.addItem_(quit_item)
    application_menu_item.setSubmenu_(application_menu)
    app.setMainMenu_(main_menu)

    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()
    return 0


def main() -> int:
    if "--smoke-test" in sys.argv:
        return smoke_test()
    return run_native_app()


if __name__ == "__main__":
    raise SystemExit(main())
