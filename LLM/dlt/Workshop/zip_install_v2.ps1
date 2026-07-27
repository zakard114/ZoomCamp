# Fast offline install v2: extract wheels DIRECTLY into site-packages (no temp copy).
$ErrorActionPreference = "Continue"
$wb = "E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\Workshop\workbench"
$dl = "E:\IT_SPACES\AI\.cache\dlt_wheels"
$sp = Join-Path $wb ".venv\Lib\site-packages"
$scripts = Join-Path $wb ".venv\Scripts"
$py = Join-Path $scripts "python.exe"
$log = Join-Path $wb "zip_install_v2.log"
$env:TEMP = "E:\IT_SPACES\AI\.cache\tmp"; $env:TMP = $env:TEMP

if (-not (Test-Path $py)) { throw "Missing venv python" }
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-InstalledSet {
  $set = @{}
  Get-ChildItem $sp -Directory -Filter "*.dist-info" -EA SilentlyContinue | ForEach-Object {
    $n = ($_.Name -replace '-[0-9].*$', '').ToLower().Replace('_', '-')
    $set[$n] = $true
  }
  $set
}

function Install-WheelDirect([System.IO.FileInfo]$whl) {
  $zip = [System.IO.Compression.ZipFile]::OpenRead($whl.FullName)
  try {
    foreach ($entry in $zip.Entries) {
      if ([string]::IsNullOrWhiteSpace($entry.Name) -and $entry.FullName.EndsWith('/')) { continue }
      $dest = Join-Path $sp ($entry.FullName -replace '/', '\')
      $dir = Split-Path $dest -Parent
      if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
      if ($entry.Length -eq 0 -and $entry.FullName.EndsWith('/')) { continue }
      if (Test-Path $dest) { Remove-Item $dest -Force -EA SilentlyContinue }
      [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true)
    }
  } finally { $zip.Dispose() }
}

"==== zip_v2 $(Get-Date) ====" | Set-Content $log

# Critical first (lesson 01), then the rest. Skip heavy optional if time.
$priority = @(
  "typing_extensions","packaging","six","idna","certifi","charset_normalizer","urllib3",
  "requests","pyyaml","pathspec","pathvalidate","pluggy","semver","tenacity","tomlkit",
  "click","colorama","mdurl","markdown_it_py","pygments","rich","rich_argparse",
  "h11","anyio","httpcore","httpx","sniffio",
  "smmap","gitdb","gitpython","giturlparse",
  "orjson","simplejson","fsspec","humanize","jsonpath_ng","tabulate",
  "python_dateutil","pytz","tzdata","pendulum","croniter","cron_descriptor",
  "attrs","pyjwt","requirements_parser","sqlglot",
  "pywin32","duckdb","dlt","dlthub_client","dlthub"
)

$wheels = @{}
Get-ChildItem $dl -Filter "*.whl" | ForEach-Object {
  if ($_.Name -match '^(?<n>.+?)-(?=\d)') {
    $wheels[$Matches.n.ToLower()] = $_
    $wheels[$Matches.n.ToLower().Replace('_','-')] = $_
    $wheels[$Matches.n.ToLower().Replace('-','_')] = $_
  }
}

$installed = Get-InstalledSet
Write-Host "already=$($installed.Count)"

$ok=0;$skip=0;$fail=0;$i=0
$todo = New-Object System.Collections.Generic.List[System.IO.FileInfo]
$seen = @{}
foreach ($n in $priority) {
  $w = $null
  foreach ($k in @($n.ToLower(), $n.ToLower().Replace('_','-'), $n.ToLower().Replace('-','_'))) {
    if ($wheels.ContainsKey($k)) { $w = $wheels[$k]; break }
  }
  if ($w -and -not $seen.ContainsKey($w.FullName)) { $todo.Add($w); $seen[$w.FullName]=$true }
}
# remaining non-priority (except skip list)
$skipNames = @('marimo','pyarrow','cryptography','beartype','jedi','parso')
foreach ($w in (Get-ChildItem $dl -Filter "*.whl")) {
  $stem = if ($w.Name -match '^(?<n>.+?)-(?=\d)') { $Matches.n.ToLower() } else { '' }
  $skipIt = $false
  foreach ($s in $skipNames) { if ($stem -match $s) { $skipIt = $true } }
  if (-not $skipIt -and -not $seen.ContainsKey($w.FullName)) { $todo.Add($w); $seen[$w.FullName]=$true }
}

foreach ($whl in $todo) {
  $i++
  $pkg = if ($whl.Name -match '^(?<n>.+?)-(?=\d)') { $Matches.n } else { $whl.BaseName }
  $key = $pkg.ToLower().Replace('_','-')
  if ($installed.ContainsKey($key) -or $installed.ContainsKey($pkg.ToLower())) {
    Write-Host "[$i/$($todo.Count)] SKIP $pkg"
    $skip++; continue
  }
  Write-Host "[$i/$($todo.Count)] ZIP $pkg"
  $t0 = Get-Date
  try {
    Install-WheelDirect $whl
    $sec = [math]::Round(((Get-Date)-$t0).TotalSeconds,1)
    Write-Host "  OK ${sec}s"
    "OK $pkg ${sec}s" | Add-Content $log
    $installed[$key] = $true
    $ok++
  } catch {
    $sec = [math]::Round(((Get-Date)-$t0).TotalSeconds,1)
    Write-Host "  FAIL ${sec}s $_"
    "FAIL $pkg $_" | Add-Content $log
    $fail++
  }
}

# Simple launcher
$cmd = Join-Path $scripts "dlthub.cmd"
@"
@echo off
"%~dp0python.exe" -m dlthub %*
"@ | Set-Content $cmd -Encoding ASCII

Write-Host "==== summary ok=$ok skip=$skip fail=$fail ===="
Write-Host "ZIP_V2_DONE"
