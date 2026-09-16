#!/bin/sh
set -eu

GAME_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
BUILD_DIR=${BUILD_DIR:-/private/tmp/monomial-finite-cell-build}
DIST_DIR=${DIST_DIR:-/private/tmp/monomial-finite-cell-dist}
RELEASE_DIR=${RELEASE_DIR:-"$GAME_ROOT/dist"}
PYI_CONFIG_DIR=${PYI_CONFIG_DIR:-/private/tmp/monomial-pyinstaller-config}

if [ ! -x "$PYTHON_BIN" ]; then
    echo "Python was not found at $PYTHON_BIN." >&2
    exit 1
fi

if ! "$PYTHON_BIN" -c 'import PyInstaller, sympy, Cocoa, WebKit' >/dev/null 2>&1; then
    echo "The macOS packaging dependencies are not installed for $PYTHON_BIN." >&2
    echo "Install requirements-macos-build.txt in a virtual environment first." >&2
    exit 1
fi

mkdir -p "$BUILD_DIR" "$DIST_DIR" "$RELEASE_DIR" "$PYI_CONFIG_DIR"
export PYINSTALLER_CONFIG_DIR="$PYI_CONFIG_DIR"

"$PYTHON_BIN" -m PyInstaller \
    --noconfirm \
    --clean \
    --workpath "$BUILD_DIR" \
    --distpath "$DIST_DIR" \
    "$GAME_ROOT/MonomialFiniteCellGame.spec"

APP_PATH="$DIST_DIR/Monomial Finite Cell Game.app"
xattr -cr "$APP_PATH"
codesign --force --deep --sign "${CODESIGN_IDENTITY:--}" "$APP_PATH"
codesign --verify --deep --strict "$APP_PATH"

ARCHIVE_NAME="Monomial-Finite-Cell-Game-macOS-arm64-v0.1.0.zip"
(
    cd "$DIST_DIR"
    zip -qry -FS -y "$ARCHIVE_NAME" "Monomial Finite Cell Game.app"
)
unzip -tq "$DIST_DIR/$ARCHIVE_NAME"
cp -f "$DIST_DIR/$ARCHIVE_NAME" "$RELEASE_DIR/$ARCHIVE_NAME"

echo "Built $RELEASE_DIR/$ARCHIVE_NAME"
echo "Smoke test with:"
echo "  $APP_PATH/Contents/MacOS/Monomial Finite Cell Game --smoke-test"
