# Offsets 실험 실행 스크립트 (earliest vs latest)
# 사전: Flink UI에서 기존 pass_through 잡 Cancel
# 실행: .\run_offset_experiment.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "0. processed_events 테이블 생성 (없으면)..." -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -f init_processed_events.sql

Write-Host "`n1. processed_events 테이블 비우기..." -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -c "TRUNCATE processed_events;"

Write-Host "`n2. pass_through_job 잡 제출 (earliest-offset)..." -ForegroundColor Cyan
# 임시로 earliest로 변경 후 제출하려면 pass_through_job.py를 earliest로 바꿔둔 상태여야 함
# 실험 후 latest로 되돌리려면 pass_through_job.py를 latest로 수정 후 다시 빌드/재시작
docker compose exec jobmanager ./bin/flink run -py /opt/src/job/pass_through_job.py -d

Write-Host "`n3. 15초 대기..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "`n4. processed_events 건수 확인:" -ForegroundColor Cyan
docker compose exec -T postgres psql -U postgres -c "SELECT count(*) FROM processed_events;"

Write-Host "`n5. offset을 latest-offset으로 복원 (실험 완료)..." -ForegroundColor Cyan
$jobPath = Join-Path $PSScriptRoot "src\job\pass_through_job.py"
(Get-Content $jobPath -Raw) -replace "latest-offset", "LATEST_PLACEHOLDER" -replace "earliest-offset", "latest-offset" -replace "LATEST_PLACEHOLDER", "earliest-offset" -replace "'latest'", "'LATEST_PLACEHOLDER'" -replace "'earliest'", "'latest'" -replace "'LATEST_PLACEHOLDER'", "'earliest'" | Set-Content $jobPath -NoNewline
# 위 치환이 earliest<->latest 스왑이므로, 현재 earliest인 파일을 latest로 바꿈
(Get-Content $jobPath -Raw) -replace "earliest-offset", "latest-offset" -replace "'earliest'", "'latest'" | Set-Content $jobPath -NoNewline

Write-Host "`n완료. pass_through_job.py가 latest-offset으로 설정되었습니다." -ForegroundColor Green
