/* @bruin
name: reports.trips_report
type: bq.sql
description: "일별/택시 타입별/결제수단별 운행 통계 리포트"
owner: zakard

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: taxi_type
    type: STRING
    description: "택시 종류 (yellow, green 등)"
    primary_key: true
    checks:
      - name: not_null
  - name: pickup_date
    type: DATE
    description: "픽업 발생 일자"
    primary_key: true
    checks:
      - name: not_null
  - name: payment_type
    type: INT64
    description: "결제 수단 코드"
    primary_key: true
    checks:
      - name: not_null
      - name: non_negative
  - name: payment_type_description
    type: STRING
    description: "결제 수단 명칭"
    checks:
      - name: not_null
  - name: total_trips
    type: INT64
    description: "총 운행 건수"
    checks:
      - name: not_null
      - name: positive
  - name: total_distance
    type: FLOAT64
    description: "총 주행 거리(km)"
    checks:
      - name: not_null
      - name: non_negative
  - name: total_revenue
    type: FLOAT64
    description: "추정 총 매출 (거리 × 2.5)"
    checks:
      - name: not_null
      - name: non_negative
@bruin */

SELECT
    taxi_type,
    DATE(pickup_datetime) AS pickup_date,
    payment_type,
    MAX(payment_type_description) AS payment_type_description,
    COUNT(*) AS total_trips,
    SUM(trip_distance) AS total_distance,
    SUM(trip_distance * 2.5) AS total_revenue
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
  AND payment_type IS NOT NULL
  AND payment_type_description IS NOT NULL
GROUP BY
    1,
    2,
    3;
