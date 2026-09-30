# Allowlisted recovery command. Turns off the injected registration 500.
$flag = Join-Path $PSScriptRoot "..\..\observability\.inject-register-failure"
if (Test-Path $flag) { Remove-Item -Force $flag }
Write-Output "inject flag off"
