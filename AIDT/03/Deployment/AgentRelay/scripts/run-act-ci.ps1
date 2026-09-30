# Local CI with act (Packet 06) — mirrors .github/workflows/ci.yml
# Tests first; deploy only if tests pass (Q6).
#
# On Windows, act + GHA `services:` healthchecks often abort before Postgres
# finishes init. This script therefore:
#   1) runs the same test job via act (workflow starts its own postgres on :5433)
#   2) if act cannot talk to Docker from inside the job, falls back to host pytest
#      against a host-started Postgres — still "tests must pass before deploy".
param(
    [switch]$TestOnly,
    [switch]$HostTest
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
$bin = "E:\IT_SPACES\AI\.cache\bin"
$dockerBin = "C:\Program Files\Docker\Docker\resources\bin"
$env:Path = "$bin;$dockerBin;$env:Path"

if (-not (Get-Command act -ErrorAction SilentlyContinue)) {
    throw "act.exe not found. Expected at $bin\act.exe"
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "docker not in PATH. Start Docker Desktop and re-run."
}

$kubeDir = Join-Path $env:USERPROFILE ".kube"
if (-not (Test-Path (Join-Path $kubeDir "config"))) {
    throw "Missing $kubeDir\config — create kind cluster first (Packet 05)."
}

function Stop-CiPostgres {
    docker rm -f agent-relay-ci-pg 2>$null | Out-Null
}

function Start-CiPostgres {
    Stop-CiPostgres
    docker run -d --name agent-relay-ci-pg `
        -e POSTGRES_USER=relay `
        -e POSTGRES_PASSWORD=relay `
        -e POSTGRES_DB=relay_test `
        -p 5433:5432 `
        postgres:16-alpine | Out-Null
    $url = "postgresql://relay:relay@127.0.0.1:5433/relay_test"
    for ($i = 1; $i -le 90; $i++) {
        docker exec agent-relay-ci-pg pg_isready -U relay -d relay_test 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "postgres ready ($i)"
            return
        }
        Write-Host "waiting for postgres... $i"
        Start-Sleep -Seconds 2
    }
    throw "postgres did not become ready in time"
}

function Invoke-HostPytest {
    Write-Host "==> host pytest against Postgres :5433"
    Start-CiPostgres
    try {
        $env:RELAY_DATABASE_URL = "postgresql+psycopg://relay:relay@127.0.0.1:5433/relay_test"
        uv sync --frozen
        if ($LASTEXITCODE -ne 0) { throw "uv sync failed" }
        uv run pytest -q
        if ($LASTEXITCODE -ne 0) { throw "pytest failed" }
    }
    finally {
        Stop-CiPostgres
    }
}

Write-Host "==> cleanup leftover act containers (if any)"
docker ps -aq --filter "name=act-" | ForEach-Object { docker rm -f $_ 2>$null | Out-Null }
Stop-CiPostgres

$testsOk = $false
if ($HostTest) {
    Invoke-HostPytest
    $testsOk = $true
}
else {
    Write-Host "==> act job: test"
    # Do NOT remount docker.sock — act already binds the daemon (Windows npipe).
    $actArgs = @(
        "-j", "test",
        "-P", "ubuntu-latest=catthehacker/ubuntu:act-latest",
        "--pull=false"
    )
    & act @actArgs
    if ($LASTEXITCODE -eq 0) {
        $testsOk = $true
    }
    else {
        Write-Host "act test job failed — falling back to host pytest (same Q6 gate)."
        try {
            Invoke-HostPytest
            $testsOk = $true
        }
        catch {
            Write-Host "Tests FAILED — stopping. Existing kind Deployment is left unchanged (Q6)."
            Write-Host $_
            exit 1
        }
    }
}

if (-not $testsOk) {
    Write-Host "Tests FAILED — stopping. Existing kind Deployment is left unchanged (Q6)."
    exit 1
}

if ($TestOnly) {
    Write-Host "TestOnly: skip deploy."
    exit 0
}

# Unique tag per run (same idea as GITHUB_RUN_ID in the workflow)
$tag = "ci-local-$(Get-Date -Format 'yyyyMMddHHmmss')"
Write-Host "==> build image ${tag}"
docker build -t "agent-relay:$tag" .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> kind load + rollout"
kind load docker-image "agent-relay:$tag" --name agent-relay
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

kubectl set image deployment/agent-relay "api=agent-relay:$tag"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

kubectl rollout status deployment/agent-relay --timeout=180s
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

kubectl get pods -l app=agent-relay
Write-Host "CI local OK. Tag=$tag"
Write-Host "port-forward if needed: kubectl port-forward svc/agent-relay 8000:8000"
