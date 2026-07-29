# Docker Reset 이후 전체 워크플로우: Producer -> Flink -> Postgres 결과 확인
# PowerShell에서 실행

Set-Location $PSScriptRoot

Write-Host "=== 1. Redpanda, Postgres 기동 ===" -ForegroundColor Cyan
docker compose up -d redpanda postgres
Write-Host "15초 대기 중..." -ForegroundColor Gray
Start-Sleep -Seconds 15

Write-Host "`n=== 2. Producer 실행 (green-trips 토픽 생성 + 데이터 전송) ===" -ForegroundColor Cyan
if (-not (Test-Path data/green_tripdata_2025-10.parquet)) {
    Write-Host "오류: data/green_tripdata_2025-10.parquet 없음. NYC TLC에서 다운로드 후 data/ 폴더에 넣어주세요." -ForegroundColor Red
    exit 1
}
python producer.py

Write-Host "`n=== 3. 토픽 확인 (rpk) ===" -ForegroundColor Cyan
docker compose exec redpanda rpk topic list
Write-Host "`ngreen-trips 샘플 3건:" -ForegroundColor Gray
docker compose exec redpanda rpk topic consume green-trips --num 3 2>$null

Write-Host "`n=== 4. Flink 잡 실행 (5분 윈도우 집계 -> processed_trips) ===" -ForegroundColor Cyan
docker compose run --rm flink-driver

Write-Host "`n=== 5. Postgres 결과 확인 ===" -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT "PULocationID", num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 10;'

Write-Host "`n=== 완료 ===" -ForegroundColor Green
