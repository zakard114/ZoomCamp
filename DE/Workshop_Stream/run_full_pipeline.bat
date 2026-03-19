@echo off
REM ===== processed_events가 0인 문제 해결 스크립트 =====
REM 1. 프로듀서 먼저 실행 (Kafka에 데이터 적재)
REM 2. Flink 잡 제출 (earliest-offset으로 topic 처음부터 읽음)
REM 3. 약 30초 대기 후 pg에서 count 확인

cd /d "%~dp0"

echo [1/5] Kafka에 데이터 전송 (프로듀서 실행)...
call uv run python src/producers/producer.py
if errorlevel 1 (
    echo 프로듀서 실패. uv sync 후 재시도하세요.
    pause
    exit /b 1
)

echo.
echo [2/5] Flink 잡 제출...
docker compose exec jobmanager ./bin/flink run -py /opt/src/job/pass_through_job.py -d
if errorlevel 1 (
    echo 잡 제출 실패.
    pause
    exit /b 1
)

echo.
echo [3/5] 30초 대기 (Flink가 Kafka 데이터 처리 중)...
timeout /t 30 /nobreak

echo.
echo [4/5] PostgreSQL count 확인...
echo SELECT count(*) FROM processed_events; | docker compose exec -T postgres psql -U postgres -d postgres

echo.
echo [5/5] 완료. count가 1000이면 성공입니다.
pause
