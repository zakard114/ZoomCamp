# Launch classic Jupyter (Esc / a / b shortcuts) with ML Zoomcamp venv.
# Avoids Anaconda Notebook 7.0.8 shortcut bug.
$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\ML"
$py = Join-Path $root ".venv\Scripts\python.exe"
$nb = if ($args.Count -gt 0) { $args[0] } else { "07-numpy.ipynb" }
Set-Location (Join-Path $root "01\intro")
& $py "$root\.venv\Scripts\jupyter-nbclassic-script.py" $nb
