# Fast offline install: extract local wheels directly into site-packages (skips uv cache I/O).
# Run only when no other uv/pip is touching this venv.

$ErrorActionPreference = "Stop"
$wb = "E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\Workshop\workbench"
$dl = "E:\IT_SPACES\AI\.cache\dlt_wheels"
$sp = Join-Path $wb ".venv\Lib\site-packages"
$scripts = Join-Path $wb ".venv\Scripts"
$py = Join-Path $scripts "python.exe"
$log = Join-Path $wb "zip_install.log"

if (-not (Test-Path $py)) { throw "Missing venv python: $py" }
if (-not (Test-Path $sp)) { throw "Missing site-packages: $sp" }

Add-Type -AssemblyName System.IO.Compression.FileSystem

function Test-Installed([string]$distName) {
  $n = $distName.ToLower().Replace('_', '-')
  Get-ChildItem $sp -Directory -Filter "*.dist-info" -EA SilentlyContinue |
    Where-Object {
      $base = ($_.Name -replace '-[0-9].*$', '').ToLower().Replace('_', '-')
      $base -eq $n
    } | Select-Object -First 1
}

function Install-WheelZip([System.IO.FileInfo]$whl) {
  $tmp = Join-Path $env:TEMP ("whl_" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Force -Path $tmp | Out-Null
  try {
    [System.IO.Compression.ZipFile]::ExtractToDirectory($whl.FullName, $tmp)
    Get-ChildItem $tmp -Force | ForEach-Object {
      $dest = Join-Path $sp $_.Name
      if (Test-Path $dest) { Remove-Item $dest -Recurse -Force -EA SilentlyContinue }
      Move-Item -LiteralPath $_.FullName -Destination $sp -Force
    }
  } finally {
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force -EA SilentlyContinue }
  }
}

function New-ConsoleLauncher([string]$name, [string]$module, [string]$attr = "main") {
  $cmd = Join-Path $scripts "$name.cmd"
  @"
@echo off
"%~dp0python.exe" -c "import runpy,sys; sys.argv[0]=r'%~dp0$name'; from $module import $attr as _m; raise SystemExit(_m())"
"@ | Set-Content -Path $cmd -Encoding ASCII
}

"==== zip_install $(Get-Date) ====" | Tee-Object -FilePath $log

# Prefer lesson-critical set first, then remaining wheels
$priorityNames = @(
  "typing_extensions", "packaging", "six", "idna", "certifi", "charset_normalizer", "urllib3",
  "requests", "pyyaml", "pathspec", "pathvalidate", "pluggy", "semver", "tenacity", "tomlkit",
  "click", "colorama", "mdurl", "markdown_it_py", "pygments", "rich", "rich_argparse",
  "h11", "anyio", "httpcore", "httpx", "sniffio",
  "smmap", "gitdb", "gitpython", "giturlparse",
  "orjson", "simplejson", "fsspec", "humanize", "jsonpath_ng", "tabulate",
  "python_dateutil", "pytz", "tzdata", "pendulum", "croniter", "cron_descriptor",
  "attrs", "pyjwt", "requirements_parser", "sqlglot",
  "pywin32", "duckdb", "dlt", "dlthub_client", "dlthub",
  "setuptools", "wheel", "pip"
)

$byStem = @{}
Get-ChildItem $dl -Filter "*.whl" | ForEach-Object {
  $stem = ($_.BaseName -replace '-cp\d+.*$', '' -replace '-\d+(\.\d+)+.*$', '')
  # better: name before first version digit cluster
  if ($_.Name -match '^(?<n>.+?)-(?=\d)') { $stem = $Matches.n }
  $byStem[$stem.ToLower()] = $_
}

$ordered = New-Object System.Collections.Generic.List[System.IO.FileInfo]
$seen = @{}
foreach ($n in $priorityNames) {
  $key = $n.ToLower()
  $whl = $null
  foreach ($k in @($key, $key.Replace('_','-'), $key.Replace('-','_'))) {
    if ($byStem.ContainsKey($k)) { $whl = $byStem[$k]; break }
  }
  if ($whl -and -not $seen.ContainsKey($whl.FullName)) {
    $ordered.Add($whl); $seen[$whl.FullName] = $true
  }
}
foreach ($whl in (Get-ChildItem $dl -Filter "*.whl" | Sort-Object Name)) {
  if (-not $seen.ContainsKey($whl.FullName)) { $ordered.Add($whl); $seen[$whl.FullName] = $true }
}

$ok = 0; $skip = 0; $fail = 0
$i = 0
foreach ($whl in $ordered) {
  $i++
  $pkg = if ($whl.Name -match '^(?<n>.+?)-(?=\d)') { $Matches.n } else { $whl.BaseName }
  if (Test-Installed $pkg) {
    Write-Host "[$i/$($ordered.Count)] SKIP $pkg"
    $skip++
    continue
  }
  Write-Host "[$i/$($ordered.Count)] ZIP $pkg <- $($whl.Name)"
  $t0 = Get-Date
  try {
    Install-WheelZip $whl
    $sec = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
    Write-Host "  OK ${sec}s"
    "OK $pkg ${sec}s" | Tee-Object -FilePath $log -Append | Out-Null
    $ok++
  } catch {
    $sec = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
    Write-Host "  FAIL ${sec}s $_"
    "FAIL $pkg $_" | Tee-Object -FilePath $log -Append | Out-Null
    $fail++
  }
}

# Entry-point shims (zip extract does not create .exe launchers)
try {
  New-ConsoleLauncher "dlthub" "dlthub.cli" "main"
} catch {
  try { New-ConsoleLauncher "dlthub" "dlthub" "main" } catch { Write-Host "launcher note: $_" }
}

Write-Host "==== summary ok=$ok skip=$skip fail=$fail ===="
Write-Host "ZIP_INSTALL_DONE"
