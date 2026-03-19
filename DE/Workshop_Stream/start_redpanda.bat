@echo off
cd /d "%~dp0"
echo Docker 실행 확인 중...
docker info >nul 2>&1
if errorlevel 1 (
    echo.
    echo [오류] Docker가 실행되지 않았습니다.
    echo Docker Desktop을 먼저 실행해 주세요.
    pause
    exit /b 1
)
echo Redpanda 시작...
docker compose up redpanda -d
if errorlevel 1 (
    pause
    exit /b 1
)
echo.
echo Redpanda가 localhost:9092에서 실행 중입니다.
docker compose ps
pause
