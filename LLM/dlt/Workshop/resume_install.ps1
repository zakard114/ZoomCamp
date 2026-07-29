# resume_install.ps1 — install ONE local wheel at a time (resumable, visible progress)
# Does NOT recreate .venv. Skips wheels already present as dist-info.

$ErrorActionPreference = "Continue"
$wb = "E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\Workshop\workbench"
$dl = "E:\IT_SPACES\AI\.cache\dlt_wheels"
$py = Join-Path $wb ".venv\Scripts\python.exe"
$log = Join-Path $wb "resume_install.log"
$cache = "E:\IT_SPACES\AI\.cache"

$env:UV_CACHE_DIR = "$cache\uv"
$env:TEMP = "$cache\tmp"
$env:TMP = $env:TEMP
$env:DO_NOT_TRACK = "1"

if (-not (Test-Path $py)) {
  Write-Host "Creating venv with uv (fast)..."
  Set-Location $wb
  uv venv --python 3.13 .venv
}

# Fix broken setuptools pth if present
$badPth = Join-Path $wb ".venv\Lib\site-packages\distutils-precedence.pth"
if (Test-Path $badPth) {
  Remove-Item $badPth -Force
  Write-Host "removed broken distutils-precedence.pth"
}

# Core set for Lesson 01 (skip marimo/pyarrow/cryptography for now — optional later)
$priority = @(
  "setuptools", "wheel", "pip",
  "typing_extensions", "packaging", "six", "idna", "certifi", "charset_normalizer", "urllib3",
  "requests", "pyyaml", "pathspec", "pathvalidate", "pluggy", "semver", "tenacity", "tomlkit",
  "click", "colorama", "mdurl", "markdown_it_py", "pygments", "rich", "rich_argparse",
  "h11", "anyio", "httpcore", "httpx", "sniffio",
  "smmap", "gitdb", "gitpython", "giturlparse",
  "orjson", "simplejson", "fsspec", "humanize", "jsonpath_ng", "tabulate",
  "python_dateutil", "pytz", "tzdata", "pendulum", "croniter", "cron_descriptor",
  "attrs", "pyjwt", "requirements_parser", "sqlglot",
  "pywin32", "duckdb", "dlt", "dlthub_client", "dlthub"
)

function Get-InstalledNames {
  Get-ChildItem (Join-Path $wb ".venv\Lib\site-packages") -Directory -Filter "*.dist-info" -EA SilentlyContinue |
    ForEach-Object { ($_.Name -replace '-[0-9].*$', '').ToLower().Replace('_', '-') }
}

function Find-Wheel([string]$name) {
  $n = $name.ToLower().Replace('_', '-')
  Get-ChildItem $dl -Filter "*.whl" | Where-Object {
    $wn = $_.Name.ToLower()
    $wn.StartsWith($n + "-") -or $wn.StartsWith($n.Replace('-', '_') + "-")
  } | Select-Object -First 1
}

Set-Location $wb
"==== resume $(Get-Date) ====" | Tee-Object -FilePath $log -Append
$installed = @(Get-InstalledNames)
Write-Host "already_distinfo=$($installed.Count)"

$ok = 0; $skip = 0; $fail = 0
foreach ($name in $priority) {
  $key = $name.ToLower().Replace('_', '-')
  $alts = @($key, $key.Replace('-', '_'))
  $have = $false
  foreach ($a in $alts) {
    if ($installed -contains $a -or $installed -contains $a.Replace('_','-')) { $have = $true }
  }
  # also check common rename: pyyaml -> yaml package but dist-info PyYAML
  if ($key -eq "pyyaml" -and ($installed -contains "pyyaml")) { $have = $true }
  if ($key -eq "python-dateutil" -or $key -eq "python_dateutil") {
    if ($installed -contains "python-dateutil") { $have = $true }
  }
  if ($have) {
    Write-Host "SKIP $name"
    $skip++
    continue
  }

  $whl = Find-Wheel $name
  if (-not $whl) {
    # try alternate spellings
    $whl = Find-Wheel ($name.Replace('_', '-'))
    if (-not $whl) { $whl = Find-Wheel ($name.Replace('-', '_')) }
  }
  if (-not $whl) {
    Write-Host "NO_WHEEL $name"
    "NO_WHEEL $name" | Tee-Object -FilePath $log -Append | Out-Null
    $fail++
    continue
  }

  Write-Host "INSTALL $name <- $($whl.Name)"
  $t0 = Get-Date
  uv pip install --python $py --offline --no-deps $whl.FullName 2>&1 | Tee-Object -FilePath $log -Append | Out-Null
  $code = $LASTEXITCODE
  $sec = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
  if ($code -eq 0) {
    Write-Host "  OK ${sec}s"
    "OK $name ${sec}s" | Tee-Object -FilePath $log -Append | Out-Null
    $ok++
    $installed = @(Get-InstalledNames)
  } else {
    Write-Host "  FAIL exit=$code after ${sec}s"
    "FAIL $name exit=$code" | Tee-Object -FilePath $log -Append | Out-Null
    $fail++
  }
}

Write-Host "==== summary ok=$ok skip=$skip fail=$fail ===="
Write-Host "verify..."
& $py -c "import dlt, duckdb; print('dlt_ok'); print('duckdb', duckdb.__version__)"
Write-Host "import_exit=$LASTEXITCODE"
if (Test-Path (Join-Path $wb ".venv\Scripts\dlthub.exe")) {
  & (Join-Path $wb ".venv\Scripts\dlthub.exe") ai status
} else {
  Write-Host "dlthub.exe not yet; trying import dlthub"
  & $py -c "import dlthub; print('dlthub_ok')"
}
Write-Host "RESUME_DONE"
