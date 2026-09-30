# Bounded, repeatable, read-only evidence. Allowlisted queries only.
param([string]$IncidentId = "INC-20260925-001")

$ErrorActionPreference = "Stop"
$outDir = Join-Path $PSScriptRoot "evidence"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$out = Join-Path $outDir "$IncidentId.json"

function Get-Allowlisted($Url) {
    try {
        return Invoke-RestMethod -Uri $Url -Method GET -TimeoutSec 8
    } catch {
        return @{ error = $_.Exception.Message }
    }
}

$packet = [ordered]@{
    incident_id = $IncidentId
    collected_at = (Get-Date).ToUniversalTime().ToString("o")
    queries = @(
        "GET http://127.0.0.1:8000/health",
        "GET http://127.0.0.1:8000/ready",
        "GET Prometheus up",
        "GET Prometheus agent_relay_http_errors_total",
        "GET Prometheus ALERTS",
        "GET Prometheus rules",
        "git log -5 --oneline"
    )
    health = Get-Allowlisted "http://127.0.0.1:8000/health"
    ready  = Get-Allowlisted "http://127.0.0.1:8000/ready"
    prom_up = Get-Allowlisted "http://127.0.0.1:9090/api/v1/query?query=up"
    http_errors = Get-Allowlisted "http://127.0.0.1:9090/api/v1/query?query=agent_relay_http_errors_total"
    agents_registered = Get-Allowlisted "http://127.0.0.1:9090/api/v1/query?query=agent_relay_agents_registered_total"
    alerts = Get-Allowlisted "http://127.0.0.1:9090/api/v1/query?query=ALERTS"
    rules = Get-Allowlisted "http://127.0.0.1:9090/api/v1/rules"
    inject_flag_present = Test-Path (Join-Path $PSScriptRoot "..\observability\.inject-register-failure")
    recent_commits = @(git -C (Join-Path $PSScriptRoot "..") log -5 --oneline)
    notes = "Read-only packet. No admin credentials. Tokens are not collected."
}

$packet | ConvertTo-Json -Depth 8 | Set-Content -Path $out -Encoding utf8
Write-Output $out
