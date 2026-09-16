# Monomial Finite Cell Game

This repository contains the bridge-free, formula-free monomial version of the
A-infinity finite-cell game, together with packaging scripts for macOS and
Windows.

The game source and detailed documentation are in
[`monomial-finite-cell/`](monomial-finite-cell/README.md). The small
`program-A-inf/` directory contains the shared algebra kernel files required by
the monomial game.

## Run from source

```sh
cd monomial-finite-cell
./run_game.sh
```

Then open <http://127.0.0.1:8600>.

## Build the Windows game on GitHub

Open the repository's **Actions** tab, select **Build Windows game**, and choose
**Run workflow**. When the run completes, download the Windows artifact from
the workflow run page. It contains the `.exe` and a ZIP archive.

