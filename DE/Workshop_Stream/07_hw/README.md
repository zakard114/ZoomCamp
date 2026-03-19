# Data Engineering Zoomcamp 2026 - Module 7 Homework (Streaming)

This repository contains the solutions for the **Data Engineering Zoomcamp 2026** Module 7 homework. All workflow logic, Kafka producer/consumer code, PyFlink jobs, and PostgreSQL queries are documented directly in this README.

## 🚀 Key Highlights

* **Redpanda as Kafka Replacement**: Used **Redpanda** for Kafka-compatible streaming, with the same protocol and client APIs.
* **PyFlink Streaming**: Built Flink jobs with **tumbling windows** (5-min, 1-hour) and **session windows** (5-min gap) to aggregate NYC Green Taxi October 2025 data.
* **End-to-End Pipeline**: Producer → Redpanda (green-trips) → PyFlink → PostgreSQL for real-time analytics.

---

## ⚙️ Infrastructure Setup

### Environment Initialization

```bash
cd Workshop_Stream
docker compose down -v
docker compose build
docker compose up -d
```

### Topic Creation

```bash
docker exec -it workshop_stream-redpanda-1 rpk topic create green-trips
```

### Data Download

```bash
mkdir -p data && cd data
curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet
cd ..
```

---

## 📊 Quiz Solutions (Questions 1 - 6)

### Q1. What version of Redpanda are you running?

**Command:**

```bash
docker exec -it workshop_stream-redpanda-1 rpk version
```

**Result:**
```
rpk version: v25.3.9
...
```

> **Answer:** `v25.3.9`

---

### Q2. How long did it take to send the data?

**Approach:** Run `producer.py` with time measurement (`t0 = time()`, `producer.flush()`, `t1 = time()`).

**Result:**
```
Loading data...
Sending data to Redpanda...
took 12.20 seconds
```

> **Answer:** `10 seconds` (approximate)

---

### Q3. How many trips have trip_distance > 5.0?

**Approach:** Kafka consumer with `auto_offset_reset='earliest'`, count rows where `trip_distance > 5.0`.

**Consumer code (excerpt):**
```python
consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    ...
)
for message in consumer:
    if message.value['trip_distance'] > 5.0:
        count += 1
```

**Result:**
```
Result: trips with trip_distance > 5.0 = 8506
```

> **Answer:** `8506`

---

### Q4. Which PULocationID had the most trips in a single 5-minute window?

**Approach:** PyFlink job with 5-minute tumbling window, grouped by PULocationID. Write to PostgreSQL `processed_trips`.

**Flink SQL (excerpt):**
```sql
INSERT INTO processed_trips
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
    PULocationID AS pulocationid,
    COUNT(*) AS num_trips
FROM green_trips
GROUP BY TUMBLE(event_timestamp, INTERVAL '5' MINUTE), PULocationID
```

**Query:**
```bash
docker exec workshop_stream-postgres-1 psql -U postgres -d postgres -c 'SELECT pulocationid, num_trips FROM processed_trips ORDER BY num_trips DESC LIMIT 3;'
```

**Result:**
```
 pulocationid | num_trips
--------------+-----------
           74 |        15
           74 |        15
           74 |        14
```

> **Answer:** `74`

---

### Q5. How many trips were in the longest session?

**Approach:** PyFlink job with 5-minute gap session window **per PULocationID**, event time from `lpep_pickup_datetime`, 5-second watermark tolerance. Write to PostgreSQL `session_streaks`.

**Flink SQL (excerpt):**
```sql
INSERT INTO session_streaks
SELECT
    SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS session_start,
    SESSION_END(event_timestamp, INTERVAL '5' MINUTE) AS session_end,
    PULocationID AS pulocationid,
    COUNT(*) AS num_trips
FROM green_trips
GROUP BY PULocationID, SESSION(event_timestamp, INTERVAL '5' MINUTE)
```

**Query:**
```bash
docker exec workshop_stream-postgres-1 psql -U postgres -d postgres -c "SELECT num_trips FROM session_streaks ORDER BY num_trips DESC LIMIT 1;"
```

**Result:**
```
 num_trips
-----------
        81
```

> **Answer:** `81`

---

### Q6. Which hour had the highest total tip amount?

**Approach:** PyFlink job with 1-hour tumbling window, `SUM(tip_amount)` across all locations. Write to PostgreSQL `processed_trips_window`.

**Flink SQL (excerpt):**
```sql
INSERT INTO processed_trips_window
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
    COALESCE(SUM(tip_amount), 0) AS sum_tip
FROM green_trips
GROUP BY TUMBLE(event_timestamp, INTERVAL '1' HOUR)
```

**Query:**
```bash
docker exec workshop_stream-postgres-1 psql -U postgres -d postgres -c "SELECT window_start, sum_tip FROM processed_trips_window ORDER BY sum_tip DESC LIMIT 1;"
```

**Result:**
```
    window_start     |      sum_tip
---------------------+-------------------
 2025-10-16 18:00:00 | 510.8599999999999
```

> **Answer:** `2025-10-16 18:00:00`

---

## 💡 Engineering Best Practices

* **Parallelism 1**: The `green-trips` topic has 1 partition; `env.set_parallelism(1)` is required so watermarks advance correctly.
* **String Timestamps**: Used `TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss')` with 5-second watermark tolerance to handle string timestamps.
* **NaN Handling**: Replaced `NaN`/`Inf` with `null` in producer JSON serialization for Flink JSON parser compatibility.
* **Topic Hygiene**: Delete and recreate the topic when data was sent multiple times: `rpk topic delete green-trips`.
