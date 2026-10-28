#!/usr/bin/env bash
# Shared SMA/.venv has nbclassic, not jupyter-notebook.exe.
set -euo pipefail
ROOT="/e/IT_SPACES/AI/ZoomCamp/SMA"
HERE="$ROOT/04/trading_strategy_and_simulation"
PY="$ROOT/.venv/Scripts/python.exe"
NB="${1:-[2026]_Module_04_Trading_Simulations.ipynb}"
cd "$HERE"
exec "$PY" "$ROOT/.venv/Scripts/jupyter-nbclassic-script.py" "$NB"
