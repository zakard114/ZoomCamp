# processed_events count가 0인 이유 및 해결

## 가능한 원인

| 원인 | 설명 | 확인 방법 |
|------|------|-----------|
| 1. **잘못된 실행 순서** | `latest-offset` 사용 시, Flink 잡이 **먼저** 떠 있어야 프로듀서 데이터를 읽음 | 아래 “올바른 순서” 참고 |
| 2. **이미지에 옛날 코드** | `src`가 빌드 시점에 이미지에 들어가므로, 코드 변경 후 **리빌드** 필요 | `docker compose build --no-cache jobmanager` |
| 3. **Flink 잡 실패** | JDBC 연결 실패, Kafka 연결 실패 등 | `docker compose logs jobmanager` 또는 http://localhost:8081 |
| 4. **`processed_events` 없음** | 테이블이 없으면 쓰기 실패 | pgcli에서 `\dt` 로 확인 |
| 5. **Kafka에 데이터 없음** | 프로듀서 미실행 또는 실패 | 프로듀서를 다시 실행 |

---

## 올바른 실행 순서

### `earliest-offset` 사용 시 (현재 설정)
1. **프로듀서 실행** → Kafka에 1000건 전송  
2. **Flink 잡 제출** → 토픽 처음부터 읽어서 처리  
3. **약 30초 대기** 후 `SELECT count(*) FROM processed_events;` 확인

### `latest-offset` 사용 시
1. **Flink 잡 제출** → Kafka 대기  
2. **프로듀서 실행** → 1000건 전송  
3. **약 30초 대기** 후 `SELECT count(*) FROM processed_events;` 확인  

---

## 해결 절차

### 1단계: 초기화
```bash
cd Workshop_Stream

# (선택) 테이블 초기화
docker compose exec -T postgres psql -U postgres -d postgres -c "TRUNCATE processed_events;"
```

### 2단계: 이미지 리빌드
```bash
docker compose build --no-cache jobmanager taskmanager
docker compose up -d
```

### 3단계: 실행
```bash
# 프로듀서 먼저 (earliest-offset 사용 시)
uv run python src/producers/producer.py

# Flink 잡 제출
docker compose exec jobmanager ./bin/flink run \
    -py /opt/src/job/pass_through_job.py \
    --pyFiles /opt/src -d

# 30초 대기 후 count 확인
# pgcli 또는: docker compose exec -T postgres psql -U postgres -d postgres -c "SELECT count(*) FROM processed_events;"
```

### 또는 배치 스크립트 사용
```bash
run_full_pipeline.bat
```

---

## Flink 잡 상태 확인

1. **웹 UI**: http://localhost:8081  
2. **Running Jobs**에서 `pass_through_job` 상태 확인  
3. 실패 시 **Failed Jobs**에서 에러 메시지 확인  
4. 로그: `docker compose logs jobmanager --tail 100`

---

## processed_events 테이블 생성 (없을 때)

```sql
CREATE TABLE processed_events (
    PULocationID INTEGER,
    DOLocationID INTEGER,
    trip_distance DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP
);
```
