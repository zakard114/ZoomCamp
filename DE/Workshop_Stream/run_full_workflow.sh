#!/usr/bin/env bash
# Docker Reset 이후 전체 워크플로우: Producer -> Flink -> Postgres 결과 확인
# Git Bash / MINGW64 / WSL에서 실행

set -e
cd "$(dirname "$0")"

echo "=== 1. Redpanda, Postgres 기동 ==="
docker compose up -d redpanda postgres
echo "15초 대기 중..."
sleep 15

echo ""
echo "=== 2. Producer 실행 (green-trips 토픽 생성 + 데이터 전송) ==="
if [ ! -f data/green_tripdata_2025-10.parquet ]; then
    echo "오류: data/green_tripdata_2025-10.parquet 없음. NYC TLC에서 다운로드 후 data/ 폴더에 넣어주세요."
    exit 1
fi
python producer.py

echo ""
echo "=== 3. 토픽 확인 (rpk) ==="
docker compose exec redpanda rpk topic list
echo ""
echo "green-trips 샘플 3건:"
docker compose exec redpanda rpk topic consume green-trips --num 3 2>/dev/null || true

echo ""
echo "=== 4. Flink 잡 실행 (5분 윈도우 집계 -> processed_trips) ==="
docker compose run --rm flink-driver

echo ""
echo "=== 5. Postgres 결과 확인 ==="
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT "PULocationID", num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 10;'

echo ""
echo "=== 완료 ==="
