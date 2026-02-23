/* @bruin
name: staging.ensure_trips_table
type: bq.sql
@bruin */

-- staging.trips가 없으면 생성 (Bruin Cloud에서 pre-hook 미실행 시 대비)
CREATE TABLE IF NOT EXISTS `bruin-de-zoomcamp.staging.trips` (
  vendor_id INT64,
  pickup_datetime TIMESTAMP,
  trip_distance FLOAT64,
  payment_type INT64,
  payment_type_description STRING,
  taxi_type STRING,
  extracted_at TIMESTAMP
);
