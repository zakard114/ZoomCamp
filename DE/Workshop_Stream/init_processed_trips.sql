-- flink_job.py JDBC sink 스키마 (수동 실행용: docker compose exec -T postgres psql -U postgres -d postgres -f - < init_processed_trips.sql 또는 stdin)
CREATE TABLE IF NOT EXISTS processed_trips (
    window_start TIMESTAMP(3),
    "PULocationID" INTEGER,
    num_trips BIGINT
);
