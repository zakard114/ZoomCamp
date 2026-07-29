#!/usr/bin/env bash
set -euo pipefail

source /e/IT_SPACES/AI/w64devkit/activate-w64devkit.sh
cd /e/IT_SPACES/AI/ZoomCamp/LLM/llama.cpp

echo "=== g++ ==="
g++ --version | head -1

echo ""
echo "=== make (llama.cpp now uses CMake — expect error) ==="
make 2>&1 | head -8 || true

echo ""
echo "=== cmake configure ==="
cmake -B build -DCMAKE_BUILD_TYPE=Release

echo ""
echo "=== cmake build ==="
cmake --build build --config Release -j 4

echo ""
echo "=== binaries ==="
ls -la build/bin/*.exe 2>/dev/null | head -20
