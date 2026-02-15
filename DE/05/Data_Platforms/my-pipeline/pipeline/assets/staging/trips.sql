/* @bruin
name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  # 'replace' 대신 지원되는 공식 명칭인 'create+replace'를 사용합니다.
  # 이를 통해 테이블 존재 여부와 상관없이 새로 생성합니다.
  strategy: create+replace

columns:
  - name: vendor_id
    type: integer
    primary_key: true
    checks:
      - name: not_null
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null
  - name: trip_distance
    type: float
    checks:
      - name: non_negative
  - name: payment_type
    type: integer
  - name: payment_type_description
    type: string
  - name: taxi_type
    type: string
  - name: extracted_at
    type: timestamp

custom_checks:
  - name: check_positive_distance
    query: |
      SELECT count(*) FROM staging.trips WHERE trip_distance <= 0
    value: 0
@bruin */

-- 쿼리 본문
SELECT 
    t.vendor_id,
    t.pickup_datetime,
    t.trip_distance,
    t.payment_type,
    p.payment_type_name as payment_type_description,
    t.taxi_type,
    t.extracted_at
FROM ingestion.trips as t
LEFT JOIN ingestion.payment_lookup as p 
    ON t.payment_type = p.payment_type_id
WHERE t.pickup_datetime >= '{{ start_date }}'
  AND t.pickup_datetime < '{{ end_date }}'