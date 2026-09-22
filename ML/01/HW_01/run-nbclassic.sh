#!/usr/bin/env bash
# Launch classic Jupyter (nbclassic) with shared ML Zoomcamp venv.
# Do not use `jupyter notebook` — jupyter-notebook.exe is not in this venv.
set -euo pipefail
ROOT="/e/IT_SPACES/AI/ZoomCamp/ML"
HW="$ROOT/01/HW_01"
PY="$ROOT/.venv/Scripts/python.exe"
NB="${1:-[2026]_HW_01.ipynb}"
cd "$HW"
exec "$PY" "$ROOT/.venv/Scripts/jupyter-nbclassic-script.py" "$NB"
