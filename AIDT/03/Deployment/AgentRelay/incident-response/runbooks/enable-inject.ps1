# Deliberate breakage for HW4. Local only.
$flag = Join-Path $PSScriptRoot "..\..\observability\.inject-register-failure"
New-Item -ItemType File -Force -Path $flag | Out-Null
Write-Output "inject flag on: $flag"
