from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


game_root = Path(SPECPATH)
legacy_root = game_root.parent / "program-A-inf"

hidden_imports = [
    "cyclic_extensions",
    "sympy",
    *collect_submodules("WebKit"),
]

a = Analysis(
    [str(game_root / "mac_app.py")],
    pathex=[str(game_root), str(legacy_root)],
    binaries=[],
    datas=[
        (str(game_root / "web"), "web"),
        (str(legacy_root / "A_inf.ipynb"), "."),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PyQt5", "PySide6", "tkinter"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Monomial Finite Cell Game",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=False,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)

collection = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Monomial Finite Cell Game",
)

app = BUNDLE(
    collection,
    name="Monomial Finite Cell Game.app",
    bundle_identifier="org.ukko.monomial-finite-cell-game",
    info_plist={
        "CFBundleDisplayName": "Monomial Finite Cell Game",
        "CFBundleName": "Monomial Finite Cell Game",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "1",
        "NSHighResolutionCapable": True,
        "NSPrincipalClass": "NSApplication",
    },
)
