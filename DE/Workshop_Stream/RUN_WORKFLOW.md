# Docker Reset 이후 전체 워크플로우 가이드

Docker Reset 후 Redpanda 토픽이 비어있을 때, green-trips → Flink 5분 윈도우 → processed_trips까지 한 번에 실행하는 방법입니다.

---

## 선행 조건

- Docker Desktop 실행 중
- `data/green_tripdata_2025-10.parquet` 파일 존재 (Producer 데이터)
- Python 의존성: `kafka-python`, `pandas`, `pyarrow` (`pip install kafka-python pandas pyarrow`)

---

## 1단계: Redpanda, Postgres 기동

```bash
cd Workshop_Stream
docker compose up -d redpanda postgres
```

기동 대기 (최소 15~20초 권장):

```bash
sleep 15
```

---

## 2단계: Producer 실행 (green-trips 토픽 생성 및 데이터 적재)

Producer가 `green-trips` 토픽을 자동 생성하고 Parquet 데이터를 전송합니다.

```bash
python producer.py
```

성공 시 예: `took 11.05 seconds`와 같은 출력이 나옵니다.

---

## 3단계: 토픽 및 데이터 확인 (rpk)

Redpanda 컨테이너 안에서 rpk를 실행합니다.

### 토픽 목록 확인

```bash
docker compose exec redpanda rpk topic list
```

출력 예: `green-trips`가 보여야 합니다.

### 토픽 메시지 샘플 확인 (최대 5개)

```bash
docker compose exec redpanda rpk topic consume green-trips --num 5
```

JSON 형태의 green trip 데이터가 출력되면 정상입니다. `Ctrl+C`로 종료할 수 있습니다.

### 토픽 상세 정보

```bash
docker compose exec redpanda rpk topic describe green-trips
```

파티션 개수, 메시지 수 등 확인 가능합니다.

---

## 4단계: Flink 잡 실행

```bash
docker compose run --rm flink-driver
```

5분 텀블링 윈도우 집계가 수행되고, 결과가 `processed_trips` 테이블에 저장됩니다.  
정상 종료될 때까지 실행을 유지합니다.

---

## 5단계: Postgres 결과 확인

```bash
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT "PULocationID", num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 10;'
```

Question 4 정답용 쿼리:

```bash
docker compose exec -T postgres psql -U postgres -d postgres -c 'SELECT "PULocationID", num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 3;'
```

---

## 트러블슈팅

| 상황 | 조치 |
|------|------|
| `UNKNOWN_TOPIC_OR_PARTITION` | Producer를 다시 실행해서 토픽 생성 및 데이터 전송 |
| `processed_trips` 0 rows | 1) Producer 재실행 2) Flink 재실행 |
| `data/green_tripdata_2025-10.parquet` 없음 | NYC TLC에서 Parquet 파일 다운로드 후 `data/` 폴더에 저장 |
| Postgres `processed_trips` 테이블 없음 | `cat init_processed_trips.sql \| docker compose exec -T postgres psql -U postgres -d postgres` 실행 |

---

## 원클릭 스크립트

Git Bash / MINGW64:

```bash
./run_full_workflow.sh
```

PowerShell:

```powershell
.\run_full_workflow.ps1
```
