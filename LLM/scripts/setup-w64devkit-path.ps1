# Adds w64devkit to PATH for the current PowerShell session only.
$bin = 'E:\IT_SPACES\AI\w64devkit\bin'
if (-not (Test-Path (Join-Path $bin 'g++.exe'))) {
    Write-Error "w64devkit not found at $bin — run install first."
    exit 1
}
$env:PATH = "$bin;$env:PATH"
Write-Host "w64devkit on PATH — $( & (Join-Path $bin 'g++.exe') --version 2>&1 | Select-Object -First 1 )"
