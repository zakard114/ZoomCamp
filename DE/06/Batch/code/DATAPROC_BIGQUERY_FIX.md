# BigQueryRelationProvider not a subtype - 해결 방법

## 원인
`spark-bigquery-with-dependencies_2.12` 등 **Scala 기반** JAR는 클러스터의 Spark/Scala 버전과 맞지 않으면 `not a subtype` 에러가 발생합니다.  
Dataproc 2.1+ 클러스터는 Scala 2.13을 쓸 수 있어 `_2.12` JAR와 충돌합니다.

## 해결: Spark 버전별 Java 기반 커넥터 사용

**spark-3.x-bigquery** 시리즈는 Java 기반이라 Scala 버전과 무관하게 동작합니다.  
클러스터의 Spark 버전에 맞는 JAR를 쓰면 됩니다.

### 방법 1: gs://spark-lib 직접 사용 (추천, 다운로드 불필요)

Google이 제공하는 spark-lib을 `--jars`에 그대로 지정합니다. Dataproc는 기본적으로 접근 가능합니다.

```bash
# Spark 3.4 (Dataproc 2.1+에서 가장 흔함)
gcloud dataproc jobs submit pyspark \
    gs://de-zoomcamp-zakard-2026/code/spark_bigquery_v2.py \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-3.4-bigquery-0.44.0.jar
```

Spark 버전이 다르면 아래 중 하나를 사용:

```bash
# Spark 3.3
--jars=gs://spark-lib/bigquery/spark-3.3-bigquery-0.44.0.jar

# Spark 3.5
--jars=gs://spark-lib/bigquery/spark-3.5-bigquery-0.44.0.jar

# Spark 3.2
--jars=gs://spark-lib/bigquery/spark-3.2-bigquery-0.44.0.jar

# Spark 3.1
--jars=gs://spark-lib/bigquery/spark-3.1-bigquery-0.44.0.jar
```

### 방법 2: 클러스터 Spark 버전 확인 후 선택

```bash
gcloud dataproc clusters describe de-zoomcamp-cluster --region=us-central1 --format="yaml(config.softwareConfig.properties)"
```

출력에서 `spark` 항목을 보면 버전(예: 3.4, 3.5)을 알 수 있습니다.

### 방법 3: Maven 타임아웃 시, JAR를 내 버킷에 올려 사용

직접 다운로드 URL (Java 기반, Maven이 아닌 GCS):
- Spark 3.4: https://storage.googleapis.com/spark-lib/bigquery/spark-3.4-bigquery-0.44.0.jar
- Spark 3.5: https://storage.googleapis.com/spark-lib/bigquery/spark-3.5-bigquery-0.44.0.jar
- Spark 3.3: https://storage.googleapis.com/spark-lib/bigquery/spark-3.3-bigquery-0.44.0.jar

업로드 후:
```bash
gsutil cp spark-3.4-bigquery-0.44.0.jar gs://de-zoomcamp-zakard-2026/lib/

gcloud dataproc jobs submit pyspark \
    gs://de-zoomcamp-zakard-2026/code/spark_bigquery_v2.py \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    --jars=gs://de-zoomcamp-zakard-2026/lib/spark-3.4-bigquery-0.44.0.jar
```

## 참고: spark-lib vs with-dependencies

| JAR 종류 | 설명 | Scala 버전 의존 |
|----------|------|-----------------|
| spark-3.4-bigquery-0.44.0.jar | Java 기반, Spark 3.4 전용 | 없음 ✅ |
| spark-bigquery-with-dependencies_2.12-0.34.1.jar | Scala 2.12 기반 | 2.12 필요 ❌ |
