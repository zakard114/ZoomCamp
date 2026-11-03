#!/usr/bin/env bash
set -euo pipefail
ROOT="/e/IT_SPACES/AI/ZoomCamp/SMA"
HERE="$ROOT/05/deployment_and_automation"
PY="$ROOT/.venv/Scripts/python.exe"
NB="${1:-[2025]_Module_05_Advanced_Strategies_And_Simulation.ipynb}"
cd "$HERE"
exec "$PY" "$ROOT/.venv/Scripts/jupyter-nbclassic-script.py" "$NB"
