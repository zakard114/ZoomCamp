# processed_events 카운트가 0인 이유와 해결 방법

## 원인

`SELECT count(*) FROM processed_events`가 0을 반환하는 주된 원인은 **실행 순서**와 **offset 설정**입니다.

### 1. offset 설정: `latest-offset`

pass_through_job은 기본적으로 `scan.startup.mode = 'latest-offset'`을 사용합니다.

| 설정 | 의미 |
|------|------|
| **latest-offset** | 잡이 **시작된 이후에** Kafka에 들어온 메시지만 읽음 |
| **earliest-offset** | 토픽 **처음부터** 있는 모든 메시지를 읽음 |

### 2. 잘못된 실행 순서

**잘못된 순서:**
1. 프로듀서 실행 → Kafka에 1000건 전송
2. Flink 잡 제출 → `latest-offset`이라 **그 이후** 메시지만 기다림
3. 그 시점에는 새 메시지가 없음 → `count = 0`

**올바른 순서 (latest-offset 사용 시):**
1. Flink 잡 먼저 제출
2. 프로듀서 실행 → Kafka에 1000건 전송
3. Flink가 새 메시지를 읽어서 Postgres에 적재
4. `count = 1000` 확인

---

## 해결 방법

### 방법 1: offset을 `earliest-offset`으로 변경 (권장)

이미 **pass_through_job.py**를 `earliest-offset`으로 수정했습니다.

- 프로듀서를 먼저 실행해도 괜찮음
- Kafka에 이미 쌓인 메시지를 처음부터 읽어서 Postgres에 적재

**코드 변경 후 절차:**

```bash
# 1. 이미지 리빌드 (src가 이미지에 포함됨)
docker compose build jobmanager taskmanager

# 2. Flink 컨테이너 재시작
docker compose up -d jobmanager taskmanager

# 3. 잡 제출
docker compose exec jobmanager ./bin/flink run \
    -py /opt/src/job/pass_through_job.py \
    --pyFiles /opt/src -d

# 4. 15초 정도 대기 후 count 확인
```

### 방법 2: latest-offset 유지하고 올바른 순서로 실행

1. **Flink 잡 제출** (먼저 실행)
2. **프로듀서 실행**
   ```bash
   uv run python src/producers/producer.py
   ```
3. 10~15초 대기
4. **Postgres에서 count 확인**
   ```sql
   SELECT count(*) FROM processed_events;
   ```

---

## 확인 체크리스트

| 항목 | 확인 |
|------|------|
| `processed_events` 테이블 존재 | `\dt` 또는 pgcli에서 확인 |
| Redpanda 실행 중 | `docker compose ps` → redpanda Up |
| Flink jobmanager, taskmanager 실행 중 | `docker compose ps` |
| Flink 잡 제출됨 | http://localhost:8081 에서 Running 상태 |
| 프로듀서 실행됨 | `uv run python src/producers/producer.py` |

---

## 요약

- **원인**: `latest-offset`에서 프로듀서를 먼저 실행해 잡이 그 메시지를 읽지 못함.
- **해결**: `earliest-offset`으로 변경했고, 이미지 리빌드·재시작 후 잡을 다시 제출하면 기존 Kafka 메시지가 Postgres에 적재됨.
