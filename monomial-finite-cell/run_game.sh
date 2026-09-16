#!/bin/sh
set -eu

if command -v python3 >/dev/null 2>&1 && python3 -c 'import sympy' >/dev/null 2>&1; then
    exec python3 monomial_finite_cell_game.py "$@"
fi

if [ -x /opt/anaconda3/bin/python3 ]; then
    exec /opt/anaconda3/bin/python3 monomial_finite_cell_game.py "$@"
fi

echo "A Python environment containing SymPy is required." >&2
exit 1
