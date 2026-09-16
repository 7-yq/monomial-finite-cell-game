# Monomial finite-cell game

This is the bridge-free monomial version of the A-infinity game for searching
for proper finite-cell DG algebras.

Rules:

- Every cell differential is one A-infinity monomial, never a difference of
  two monomials.
- Ordinary products of generators are allowed as seed monomials. This is what
  first makes higher Massey products definable.
- Every operation of arity at least three is the canonical Massey product with
  those inputs, taken in one compatible system.
- Explicit cochain formulas for higher products are not constructed.
- Available Massey products are regenerated automatically after every cell
  attachment.
- A-infinity/Stasheff replacements and the Lemma-1 collapsed-product rule are
  enabled.
- Bridge cells and bridge replacement searches are disabled.

## Properness kernel

When the attached cells form a complete pair-poset descent language, **Run**
uses the exact finite support automaton. It reports whether the supported-word
language is finite, its maximum word length, and the resulting cohomology
dimension. Multiple compatible cut resolutions are coherence data and are not
treated as over-resolution.

If a descent system is incomplete, Run lists the missing cells instead of
claiming victory. Presentations outside the pair-poset subclass continue to use
the older search and are explicitly labeled as a heuristic fallback in the run
result.

Start the game with:

```sh
./run_game.sh
```

Then open <http://127.0.0.1:8600>. Saved games go into `saved games/` and use
their own `monomial-finite-cell-game-save` schema. A bridge-free save from the
original A-infinity game can also be imported.

## macOS application

`build_macos_app.sh` creates a distributable ZIP at
`dist/Monomial-Finite-Cell-Game-macOS-arm64-v0.1.0.zip`. Unzip it and
double-click `Monomial Finite Cell Game.app`. The application embeds the Python
engine, opens the game in its own native window, and does not require players to
install Python. Packaged saves are stored in:

```text
~/Library/Application Support/Monomial Finite Cell Game/saved games/
```

Create a clean build environment before the first build:

```sh
python3 -m venv .macos-build-env
.macos-build-env/bin/python -m pip install -r requirements-macos-build.txt
PYTHON_BIN=.macos-build-env/bin/python ./build_macos_app.sh
```

The current build script targets Apple Silicon Macs. It uses an ad-hoc signature
for local testing; public downloads should be signed with an Apple Developer ID
and notarized before release.

## Windows application

The Windows build is a single 64-bit executable with a native Edge WebView2
window. It embeds Python, SymPy, the game server, and all interface resources;
players do not need to install Python. It uses the Microsoft Edge WebView2
Runtime normally included with current Windows 10 and Windows 11 installations.
Saved games are stored in:

```text
%LOCALAPPDATA%\Monomial Finite Cell Game\saved games\
```

On a 64-bit Windows 10 or Windows 11 machine with Python 3.13 installed, run:

```powershell
./build_windows.ps1
```

This creates:

```text
dist\Monomial Finite Cell Game.exe
dist\Monomial-Finite-Cell-Game-Windows-x64-v0.1.0.zip
```

The repository-level `Build Windows game` workflow performs the same build and
smoke test on a Windows runner, then publishes both files as a workflow artifact.
The executable is currently unsigned; a public release should be Authenticode
signed to reduce Microsoft Defender SmartScreen warnings.
