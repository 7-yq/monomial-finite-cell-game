from pathlib import Path


game_root = Path(SPECPATH)
legacy_root = game_root.parent / "program-A-inf"

a = Analysis(
    [str(game_root / "windows_app.py")],
    pathex=[str(game_root), str(legacy_root)],
    binaries=[],
    datas=[
        (str(game_root / "web"), "web"),
        (str(legacy_root / "A_inf.ipynb"), "."),
    ],
    hiddenimports=[
        "clr",
        "cyclic_extensions",
        "sympy",
        "webview",
        "webview.platforms.edgechromium",
        "webview.platforms.win32",
        "webview.platforms.winforms",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "cefpython3",
        "gi",
        "objc",
        "tkinter",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Monomial Finite Cell Game",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=str(game_root / "windows_version_info.txt"),
)
