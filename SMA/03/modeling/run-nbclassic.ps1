# Shared SMA/.venv has nbclassic, not jupyter-notebook.exe.
$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\SMA"
$here = Join-Path $root "03\modeling"
$py = Join-Path $root ".venv\Scripts\python.exe"
$nb = if ($args.Count -gt 0) { $args[0] } else { "[2026]_Module_03_Time_Series_Modeling.ipynb" }
Set-Location $here
& $py "$root\.venv\Scripts\jupyter-nbclassic-script.py" $nb
