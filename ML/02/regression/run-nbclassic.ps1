# Launch classic Jupyter (Esc / a / b shortcuts) with ML Zoomcamp venv.
$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\ML"
$here = "E:\IT_SPACES\AI\ZoomCamp\ML\02\regression\notebook"
$py = Join-Path $root ".venv\Scripts\python.exe"
$nb = if ($args.Count -gt 0) { $args[0] } else { "notebook.ipynb" }
Set-Location $here
& $py "$root\.venv\Scripts\jupyter-nbclassic-script.py" $nb
