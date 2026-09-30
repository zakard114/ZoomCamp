$ErrorActionPreference = "Stop"
$root = "E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay"
Set-Location $root
$py = Join-Path $root ".venv\Scripts\python.exe"
$log = Join-Path $root "observability\uvicorn-hw4.log"

Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

$env:OTEL_ENABLED = "1"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://127.0.0.1:4318"
$env:OTEL_SERVICE_NAME = "agent-relay"
$env:APP_ENV = "dev"
$env:DEPLOYED_VERSION = "hw4-local"
Remove-Item Env:OTEL_SDK_DISABLED -ErrorAction SilentlyContinue

$errLog = Join-Path $root "observability\uvicorn-hw4.err.log"
$proc = Start-Process -FilePath $py -ArgumentList @("-m","uvicorn","main:app","--host","127.0.0.1","--port","8000") `
    -WorkingDirectory $root -RedirectStandardOutput $log -RedirectStandardError $errLog -PassThru -WindowStyle Hidden

$ok = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 2
    try {
        $h = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 3
        if ($h.StatusCode -eq 200) { $ok = $true; break }
    } catch {}
}
if (-not $ok) { throw "uvicorn did not become ready. log=$log" }

function Post-Agent([string]$name) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/agents" -Method POST `
            -ContentType "application/json" -Body (@{ name = $name } | ConvertTo-Json) -TimeoutSec 8
        return [int]$r.StatusCode
    } catch {
        if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
        throw
    }
}

$before = Post-Agent ("ok-" + [guid]::NewGuid().ToString("N").Substring(0,6))
& (Join-Path $root "incident-response\runbooks\enable-inject.ps1")
$fail1 = Post-Agent ("fail-" + [guid]::NewGuid().ToString("N").Substring(0,6))
$fail2 = Post-Agent ("fail-" + [guid]::NewGuid().ToString("N").Substring(0,6))
Start-Sleep -Seconds 20
& (Join-Path $root "incident-response\collect-evidence.ps1") -IncidentId "INC-20260925-001"
& (Join-Path $root "incident-response\runbooks\disable-inject.ps1")
$after = Post-Agent ("rec-" + [guid]::NewGuid().ToString("N").Substring(0,6))

Write-Output "before=$before fail1=$fail1 fail2=$fail2 after=$after uvicorn_pid=$($proc.Id)"
