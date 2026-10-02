# Launch classic Jupyter (nbclassic) with shared ML Zoomcamp venv.
# Do not use `jupyter notebook` — jupyter-notebook.exe is not in this venv.
# Do not pip/uv install the `notebook` package here (nbclassic shims without it).
$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\ML"
$hw = Join-Path $root "02\HW_02"
$py = Join-Path $root ".venv\Scripts\python.exe"
$nb = if ($args.Count -gt 0) { $args[0] } else { "[2026]_HW_02.ipynb" }
$env:OMP_NUM_THREADS = if ($env:OMP_NUM_THREADS) { $env:OMP_NUM_THREADS } else { "1" }
$env:MKL_NUM_THREADS = if ($env:MKL_NUM_THREADS) { $env:MKL_NUM_THREADS } else { "1" }
$env:OPENBLAS_NUM_THREADS = if ($env:OPENBLAS_NUM_THREADS) { $env:OPENBLAS_NUM_THREADS } else { "1" }
$env:NUMEXPR_NUM_THREADS = if ($env:NUMEXPR_NUM_THREADS) { $env:NUMEXPR_NUM_THREADS } else { "1" }
$env:PYTHONUNBUFFERED = "1"
Set-Location $hw

$busy = & $py -c "import socket; s=socket.socket(); s.settimeout(0.5); print('1' if s.connect_ex(('127.0.0.1',8888))==0 else '0')"
if ($busy.Trim() -eq "1") {
  Write-Host "nbclassic already on http://127.0.0.1:8888/"
  Write-Host "Notebook: http://127.0.0.1:8888/notebooks/$nb"
  Write-Host "Do not start a second server. If a token is asked, use the first launch terminal."
  exit 0
}

Write-Host "Starting nbclassic. First launch after reboot can take 1-2 minutes."
Write-Host "If you see ModuleNotFoundError: No module named 'notebook' — that is the nbclassic shim, not a crash."
Write-Host "Wait for the http://127.0.0.1:8888 URL. Do not Ctrl+C."

& $py "$root\.venv\Scripts\jupyter-nbclassic-script.py" `
  --ip=127.0.0.1 --port=8888 `
  --MappingKernelManager.kernel_info_timeout=180 `
  $nb
