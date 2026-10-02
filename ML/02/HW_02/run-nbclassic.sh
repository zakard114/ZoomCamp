#!/usr/bin/env bash
# Launch classic Jupyter (nbclassic) with shared ML Zoomcamp venv.
# Do not use `jupyter notebook` — jupyter-notebook.exe is not in this venv.
# Do not pip/uv install the `notebook` package here (nbclassic shims without it).
set -euo pipefail
ROOT="/e/IT_SPACES/AI/ZoomCamp/ML"
HW="$ROOT/02/HW_02"
PY="$ROOT/.venv/Scripts/python.exe"
NB="${1:-[2026]_HW_02.ipynb}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-1}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-1}"
export PYTHONUNBUFFERED=1
cd "$HW"

busy="$("$PY" -c "import socket; s=socket.socket(); s.settimeout(0.5); print('1' if s.connect_ex(('127.0.0.1',8888))==0 else '0')")"
if [ "$busy" = "1" ]; then
  echo "nbclassic already on http://127.0.0.1:8888/"
  echo "Notebook: http://127.0.0.1:8888/notebooks/${NB}"
  echo "Do not start a second server. If a token is asked, use the first launch terminal."
  exit 0
fi

echo "Starting nbclassic. First launch after reboot can take 1-2 minutes."
echo "If you see ModuleNotFoundError: No module named 'notebook' — that is the nbclassic shim, not a crash."
echo "Wait for the http://127.0.0.1:8888 URL. Do not Ctrl+C."

exec "$PY" "$ROOT/.venv/Scripts/jupyter-nbclassic-script.py" \
  --ip=127.0.0.1 --port=8888 \
  --MappingKernelManager.kernel_info_timeout=180 \
  "$NB"
