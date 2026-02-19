/* @bruin
name: reports.ensure_trips_report_table
type: bq.sql
@bruin */

-- reports.trips_report 테이블이 없으면 생성 (Bruin Cloud pre-hook 미실행 대비)
CREATE TABLE IF NOT EXISTS `bruin-de-zoomcamp.reports.trips_report` (
  taxi_type STRING,
  pickup_date DATE,
  payment_type INT64,
  payment_type_description STRING,
  total_trips INT64,
  total_distance FLOAT64,
  total_revenue FLOAT64
);
