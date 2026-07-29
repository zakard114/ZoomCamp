# zone_stats 전체 파이프라인 (프로듀서 → 잡 제출 → 검증)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "1. 기존 zone_stats 초기화..." -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -c "TRUNCATE zone_stats;" 2>$null

Write-Host "2. 프로듀서 실행 (Kafka에 1000건 전송)..." -ForegroundColor Cyan
Start-Process -FilePath "uv" -ArgumentList "run","python","src/producers/producer.py" -Wait -NoNewWindow

Write-Host "3. window_stats_job 컨테이너에 복사..." -ForegroundColor Cyan
docker cp src/job/window_stats_job.py workshop_stream-jobmanager-1:/opt/window_stats_job.py

Write-Host "4. window_stats 잡 제출..." -ForegroundColor Cyan
docker exec workshop_stream-jobmanager-1 ./bin/flink run -py /opt/window_stats_job.py -d

Write-Host "5. 프로듀서 재실행 (백그라운드, 잡이 RUNNING 유지)" -ForegroundColor Cyan
Start-Job -ScriptBlock { Set-Location $using:PSScriptRoot; uv run python src/producers/producer.py } | Out-Null

Write-Host "6. 90초 대기 (윈도우 처리)..." -ForegroundColor Yellow
Start-Sleep -Seconds 90

Write-Host "6. zone_stats 건수 확인:" -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -c "SELECT count(*) FROM zone_stats;"

Write-Host "7. 샘플 데이터 (상위 5건):" -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -c "SELECT * FROM zone_stats ORDER BY window_start DESC LIMIT 5;"

Write-Host "`n완료. Running Jobs: http://localhost:8081/#/job/running" -ForegroundColor Green
