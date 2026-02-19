/* @bruin
name: staging.trips
type: bq.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: vendor_id
    type: INT64
    primary_key: true
    checks:
      - name: not_null
  - name: pickup_datetime
    type: TIMESTAMP
    primary_key: true
    checks:
      - name: not_null
  - name: trip_distance
    type: FLOAT64
    checks:
      - name: non_negative
  - name: payment_type
    type: INT64
    checks:
      - name: not_null
      - name: non_negative
  - name: payment_type_description
    type: STRING
  - name: taxi_type
    type: STRING
    checks:
      - name: not_null
  - name: extracted_at
    type: TIMESTAMP
    checks:
      - name: not_null

custom_checks:
  - name: check_positive_distance
    query: |
      SELECT count(*) FROM staging.trips WHERE trip_distance <= 0
    value: 0
@bruin */

WITH base AS (
  SELECT
    t.vendor_id,
    t.pickup_datetime,
    t.trip_distance,
    t.payment_type,
    p.payment_type_name AS payment_type_description,
    t.taxi_type,
    t.extracted_at
  FROM ingestion.trips AS t
  LEFT JOIN ingestion.payment_lookup AS p
    ON t.payment_type = p.payment_type_id
  WHERE t.pickup_datetime >= '{{ start_date }}'
    AND t.pickup_datetime < '{{ end_date }}'
    AND t.trip_distance > 0
    AND t.payment_type IS NOT NULL
),
deduped AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY vendor_id, pickup_datetime, taxi_type
      ORDER BY extracted_at DESC
    ) AS rn
  FROM base
)
SELECT
  vendor_id,
  pickup_datetime,
  trip_distance,
  payment_type,
  payment_type_description,
  taxi_type,
  extracted_at
FROM deduped
WHERE rn = 1;
