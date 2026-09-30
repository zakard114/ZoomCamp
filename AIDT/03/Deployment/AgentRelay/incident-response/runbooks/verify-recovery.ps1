# Read-only enough to confirm users can enroll again. Prints status only — no token.
$ErrorActionPreference = "Stop"
$name = "recovery-" + [guid]::NewGuid().ToString("N").Substring(0, 8)
$resp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/agents" -Method POST `
    -ContentType "application/json" -Body (@{ name = $name } | ConvertTo-Json) -TimeoutSec 8
Write-Output ("register_status=" + [int]$resp.StatusCode)
if ([int]$resp.StatusCode -ne 201) { exit 1 }
