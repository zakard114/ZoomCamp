#!/usr/bin/env bash
# Classic Jupyter (Esc / a / b) with ML Zoomcamp root .venv — Git Bash
set -euo pipefail

E_CACHE="E:/IT_SPACES/AI/.cache"
mkdir -p "$E_CACHE"/uv "$E_CACHE"/uv-python/bin "$E_CACHE"/uv-tools \
  "$E_CACHE"/pip "$E_CACHE"/hf "$E_CACHE"/tmp "$E_CACHE"/npm \
  "$E_CACHE"/ollama "$E_CACHE"/gradle

export UV_CACHE_DIR="$E_CACHE/uv"
export UV_PYTHON_INSTALL_DIR="$E_CACHE/uv-python"
export UV_PYTHON_BIN_DIR="$E_CACHE/uv-python/bin"
export UV_TOOL_DIR="$E_CACHE/uv-tools"
export PIP_CACHE_DIR="$E_CACHE/pip"
export HF_HOME="$E_CACHE/hf"
export HUGGINGFACE_HUB_CACHE="$E_CACHE/hf/hub"
export TRANSFORMERS_CACHE="$E_CACHE/hf/transformers"
export XDG_CACHE_HOME="$E_CACHE"
export TEMP="$E_CACHE/tmp"
export TMP="$E_CACHE/tmp"
export TMPDIR="$E_CACHE/tmp"

here="/e/IT_SPACES/AI/ZoomCamp/ML/03/classification/notebook"
py="/e/IT_SPACES/AI/ZoomCamp/ML/.venv/Scripts/python.exe"
nbclassic="/e/IT_SPACES/AI/ZoomCamp/ML/.venv/Scripts/jupyter-nbclassic-script.py"
nb="${1:-notebook.ipynb}"

cd "$here"
exec "$py" "$nbclassic" "$nb"
