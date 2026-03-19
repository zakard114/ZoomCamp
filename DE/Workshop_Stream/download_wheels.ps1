# apache-flink 및 의존성 wheels를 로컬에 다운로드 (Docker Linux 환경용)
# 실행: cd Workshop_Stream 후 .\download_wheels.ps1
# 완료 후 docker compose build 실행

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$wheelsDir = "wheels"
if (-not (Test-Path $wheelsDir)) { New-Item -ItemType Directory -Path $wheelsDir | Out-Null }

Write-Host "apache-flink==2.2.0 wheels 다운로드 중 (Linux x86_64, Python 3.12)..." -ForegroundColor Cyan
Write-Host "호스트에서 한 번만 받으면, Docker 빌드 시 네트워크 없이 설치됩니다." -ForegroundColor Gray

# Windows에서 실행하므로 Linux용 wheel 다운로드 필요
uv pip download "apache-flink==2.2.0" `
    -d $wheelsDir `
    --platform linux_x86_64 `
    --python-version 3.12

Write-Host "`n완료. docker compose build 실행하세요." -ForegroundColor Green
