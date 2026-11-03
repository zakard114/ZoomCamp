#!/usr/bin/env bash
set -euo pipefail
ROOT="/e/IT_SPACES/AI/ZoomCamp/SMA"
HERE="$ROOT/05/HW_05"
PY="$ROOT/.venv/Scripts/python.exe"
NB="${1:-[2026]_Module_05_Homework.ipynb}"
cd "$HERE"
exec "$PY" "$ROOT/.venv/Scripts/jupyter-nbclassic-script.py" "$NB"
