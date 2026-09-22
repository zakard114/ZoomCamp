# Launch classic Jupyter (nbclassic) with shared ML Zoomcamp venv.
# Do not use `jupyter notebook` — jupyter-notebook.exe is not in this venv.
$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\ML"
$hw = Join-Path $root "01\HW_01"
$py = Join-Path $root ".venv\Scripts\python.exe"
$nb = if ($args.Count -gt 0) { $args[0] } else { "[2026]_HW_01.ipynb" }
Set-Location $hw
& $py "$root\.venv\Scripts\jupyter-nbclassic-script.py" $nb
