# flink_job.py 실행 (Dockerfile.pyflink, python3 직접 실행)
# 사전: docker compose build flink-driver, processed_trips 테이블, producer.py
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Flink Job 실행 중 (python3 직접): flink_job.py" -ForegroundColor Cyan
docker compose run --rm flink-driver
