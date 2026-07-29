# finish_setup.ps1 — offline install (avoid ensurepip hang)
# Prefer: reboot done + Defender exclude E:\IT_SPACES\AI

$ErrorActionPreference = "Stop"
$wb = "E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\Workshop\workbench"
$dl = "E:\IT_SPACES\AI\.cache\dlt_wheels"
$py = "C:\Users\HP EliteBook\AppData\Local\Programs\Python\Python313\python.exe"
$cache = "E:\IT_SPACES\AI\.cache"

$env:UV_CACHE_DIR = "$cache\uv"
$env:PIP_CACHE_DIR = "$cache\pip"
$env:TEMP = "$cache\tmp"
$env:TMP = $env:TEMP
$env:UV_HTTP_TIMEOUT = "600"
$env:DO_NOT_TRACK = "1"
New-Item -ItemType Directory -Force -Path $env:UV_CACHE_DIR, $env:PIP_CACHE_DIR, $env:TEMP | Out-Null

Write-Host "==== preflight ===="
$boot = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
Write-Host "last_boot=$boot uptime_h=$([math]::Round(((Get-Date)-$boot).TotalHours,1))"
$wheelCount = @(Get-ChildItem $dl -Filter "*.whl" -EA SilentlyContinue).Count
Write-Host "wheels=$wheelCount"
if (-not (Test-Path "$dl\duckdb-1.5.5-cp313-cp313-win_amd64.whl")) { throw "duckdb wheel missing" }
if (-not (Test-Path $py)) { throw "Python missing: $py" }

Set-Location $wb

Write-Host "==== recreate venv (without pip / no ensurepip) ===="
foreach ($name in @(".venv", ".venv_ok")) {
  $p = Join-Path $wb $name
  if (Test-Path $p) {
    $trash = Join-Path $cache ("trash_{0}_{1}" -f ($name.TrimStart('.')), (Get-Date -Format "HHmmss"))
    Move-Item -LiteralPath $p -Destination $trash -Force
    Write-Host "moved $name -> $trash (delete later)"
  }
}

# Fast path: uv venv (no ensurepip). Fallback: stdlib --without-pip
$uvOk = $false
try {
  uv venv --python 3.13 .venv
  if (Test-Path .\.venv\Scripts\python.exe) { $uvOk = $true; Write-Host "uv venv ok" }
} catch { Write-Host "uv venv failed: $_" }

if (-not $uvOk) {
  & $py -m venv .venv --without-pip
  if (-not (Test-Path .\.venv\Scripts\python.exe)) { throw "venv failed" }
  Write-Host "stdlib venv --without-pip ok"
}

Write-Host "==== offline install via uv pip (local wheels only) ===="
# Use uv pip against the venv — does not need ensurepip
uv pip install --python .\.venv\Scripts\python.exe --offline --find-links $dl `
  "dlt[hub]" "dlthub" "dlthub-client" "pathspec" "duckdb==1.5.5"
if ($LASTEXITCODE -ne 0) {
  Write-Host "uv pip offline failed ($LASTEXITCODE); trying pip bootstrap from ensurepip wheels..."
  $bundled = Join-Path (Split-Path $py) "Lib\ensurepip\_bundled"
  $pipWhl = Get-ChildItem $bundled -Filter "pip-*.whl" | Select-Object -First 1
  if (-not $pipWhl) { throw "no bundled pip wheel at $bundled" }
  # Bootstrap: run pip module from the wheel zip
  & .\.venv\Scripts\python.exe -c "import runpy,sys; sys.argv=['pip','install','--no-index','--find-links',r'$dl','$($pipWhl.FullName)']; runpy.run_path(r'$($pipWhl.FullName)', run_name='__main__')" 2>$null
  # More reliable bootstrap:
  & $py -m pip install --python .\.venv\Scripts\python.exe 2>$null
  & .\.venv\Scripts\python.exe -m pip install --no-index --find-links $dl "dlt[hub]" "dlthub" "dlthub-client" "pathspec" "duckdb==1.5.5"
  if ($LASTEXITCODE -ne 0) { throw "pip install failed: $LASTEXITCODE" }
}

Write-Host "==== verify ===="
& .\.venv\Scripts\python.exe -c "import dlt,duckdb; print('dlt', dlt.__version__); print('duckdb', duckdb.__version__)"
if (Test-Path .\.venv\Scripts\dlthub.exe) {
  & .\.venv\Scripts\dlthub.exe ai status
  Write-Host "status_exit=$LASTEXITCODE"
} else {
  Write-Host "dlthub.exe missing; entry points:"
  & .\.venv\Scripts\python.exe -c "import importlib.metadata as m; print([e.name for e in m.entry_points() if 'dlt' in e.name])"
}

Write-Host "DONE. Lesson 01 env ready."
