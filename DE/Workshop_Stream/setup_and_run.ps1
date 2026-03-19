# Question 4 원클릭 실행: green-trips -> 5분 윈도우 -> processed_trips
# 선행조건: Docker Desktop 실행, data/green_tripdata_2025-10.parquet 존재

Set-Location $PSScriptRoot

Write-Host "1. Docker 이미지 빌드..." -ForegroundColor Cyan
docker compose build --no-cache 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "빌드 실패. Docker Desktop 실행 여부 확인." -ForegroundColor Red; exit 1 }

Write-Host "2. Redpanda, Postgres 기동..." -ForegroundColor Cyan
docker compose up -d redpanda postgres
Start-Sleep -Seconds 15

Write-Host "3. Producer로 green-trips 토픽 전송..." -ForegroundColor Cyan
if (-not (Test-Path data/green_tripdata_2025-10.parquet)) {
    Write-Host "data/green_tripdata_2025-10.parquet 없음. 먼저 데이터를 넣어주세요." -ForegroundColor Yellow
} else {
    python producer.py
}

Write-Host "4. Flink 잡 실행 (5분 윈도우 집계 -> processed_trips)..." -ForegroundColor Cyan
docker compose run --rm flink-driver

Write-Host "5. 결과 확인:" -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT "PULocationID", num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 10;'
