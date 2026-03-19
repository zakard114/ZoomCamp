# Question 4 & 6 답 도출 과정

Flink Workshop Question 4(5분 텀블링 윈도우)와 Question 6(1시간 텀블링 윈도우) 정답을 얻기 위한 전체 커맨드 순서입니다.

---

## 공통 선행 조건

- `data/green_tripdata_2025-10.parquet` 파일 존재
- Docker Desktop 실행 중

---

## 1단계: 인프라 기동

```bash
cd /e/IT_SPACES/AI/ZoomCamp/DE/Workshop_Stream

# Redpanda, Postgres 기동
docker compose up -d redpanda postgres

# 15초 대기 (Postgres 초기화)
sleep 15
```

---

## 2단계: Postgres 테이블 생성 (윈도우 집계 결과 저장용)

```bash
# Question 4: processed_trips (5분 윈도우 → PULocationID별 num_trips)
docker exec -i workshop_stream-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE IF NOT EXISTS processed_trips (
    window_start TIMESTAMP(3),
    pulocationid INTEGER,
    num_trips BIGINT
);"

# Question 6: processed_trips_window (1시간 윈도우 → SUM(tip_amount))
docker exec -i workshop_stream-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE IF NOT EXISTS processed_trips_window (
    window_start TIMESTAMP(3),
    sum_tip DOUBLE PRECISION
);"
```

또는 init 파일 사용:

```bash
docker exec -i workshop_stream-postgres-1 psql -U postgres -d postgres < init/02_processed_trips.sql
docker exec -i workshop_stream-postgres-1 psql -U postgres -d postgres < init/03_processed_trips_window.sql
```

---

## 3단계: green-trips 토픽에 데이터 적재

```bash
python producer.py
```

---

## 4단계: Flink 잡 빌드 및 실행 (텀블링 윈도우 생성)

```bash
# Flink 이미지 빌드
docker compose build --no-cache flink-driver

# Flink 잡 실행 (내부에서 두 개의 텀블링 윈도우 INSERT 수행)
docker compose run --rm flink-driver
```

**Flink 내부 동작 요약:**
- **Question 4**: `TUMBLE(event_timestamp, INTERVAL '5' MINUTE)` → 5분 단위 PULocationID별 num_trips
- **Question 6**: `TUMBLE(event_timestamp, INTERVAL '1' HOUR)` → 1시간 단위 SUM(tip_amount)

몇 분 정도 기다린 후 Ctrl+C로 종료해도 이미 처리된 결과는 Postgres에 남아 있습니다.

---

## 5단계: 답 조회

### Question 4 – PULocationID별 num_trips 상위 3개

> Which PULocationID has the highest num_trips in processed_trips?

```bash
docker exec workshop_stream-postgres-1 psql -U postgres -d postgres -c \
  'SELECT pulocationid, num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 3;'
```

**Expected (보기 예):** `42`, `74`, `75`, `166` 등

---

### Question 6 – 1시간 윈도우 중 sum_tip 최대인 시각

> Which hour had the highest total tip amount?

```bash
docker exec workshop_stream-postgres-1 psql -U postgres -d postgres -c \
  'SELECT window_start, sum_tip FROM processed_trips_window ORDER BY sum_tip DESC LIMIT 1;'
```

**Options:** `2025-10-01 18:00:00` | `2025-10-16 18:00:00` | `2025-10-22 08:00:00` | `2025-10-30 16:00:00`

---

## 참고: Flink 텀블링 윈도우 SQL

### Question 4 (5분 윈도우)

```sql
INSERT INTO processed_trips
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
    PULocationID AS pulocationid,
    COUNT(*) AS num_trips
FROM green_trips
GROUP BY TUMBLE(event_timestamp, INTERVAL '5' MINUTE), PULocationID;
```

### Question 6 (1시간 윈도우)

```sql
INSERT INTO processed_trips_window
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
    COALESCE(SUM(tip_amount), 0) AS sum_tip
FROM green_trips
GROUP BY TUMBLE(event_timestamp, INTERVAL '1' HOUR);
```
