/* @bruin
name: staging.trips
type: bq.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup
  - staging.ensure_trips_table

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

@bruin */

WITH base AS (
  SELECT
    CAST(t.vendor_id AS INT64) AS vendor_id,
    CAST(t.pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    t.trip_distance,
    CAST(t.payment_type AS INT64) AS payment_type,
    p.payment_type_name AS payment_type_description,
    t.taxi_type,
    CAST(t.extracted_at AS TIMESTAMP) AS extracted_at
  FROM ingestion.trips AS t
  LEFT JOIN ingestion.payment_lookup AS p
    ON t.payment_type = p.payment_type_id
  WHERE CAST(t.pickup_datetime AS TIMESTAMP) >= '{{ start_date }}'
    AND CAST(t.pickup_datetime AS TIMESTAMP) < '{{ end_date }}'
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
