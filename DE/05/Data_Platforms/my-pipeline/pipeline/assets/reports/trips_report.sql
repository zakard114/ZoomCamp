/* @bruin
name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  # create+replace 전략을 사용하여 테이블 존재 여부와 상관없이 새로 생성합니다.
  # 이 전략에서는 incremental_key가 필요 없으므로 제거했습니다.
  strategy: create+replace

columns:
  - name: taxi_type
    type: string
    description: "Type of taxi (yellow, green, etc.)"
    primary_key: true
  - name: pickup_date
    type: DATE
    description: "The date when the pickup occurred"
    primary_key: true
  - name: total_trips
    type: BIGINT
    description: "Total number of trips for this date and taxi type"
    checks:
      - name: non_negative
  - name: total_distance
    type: float
    description: "Total distance traveled"
    checks:
      - name: non_negative
  - name: total_revenue
    type: float
    description: "Estimated total revenue (distance * 2.5)"
    checks:
      - name: non_negative
@bruin */

-- 리포트 생성 로직: 일별/택시 타입별 집계
SELECT 
    taxi_type,
    CAST(pickup_datetime AS DATE) as pickup_date,
    count(*) as total_trips,
    sum(trip_distance) as total_distance,
    sum(trip_distance * 2.5) as total_revenue
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY 
    taxi_type, 
    pickup_date