# Renames DE/Projects -> DE/Project (singular) to match docs. Close Cursor/IDE first if access denied.
$ErrorActionPreference = 'Stop'
$deRoot = $PSScriptRoot
$src = Join-Path $deRoot 'Projects'
$dst = Join-Path $deRoot 'Project'
if (Test-Path $dst) {
    Write-Host "Already exists: $dst"
    exit 0
}
if (-not (Test-Path $src)) {
    Write-Host "Not found: $src"
    exit 1
}
Rename-Item -LiteralPath $src -NewName 'Project'
Write-Host "OK: Renamed Projects -> Project"
