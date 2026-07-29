-- pass_through_job JDBC sink 스키마와 일치
CREATE TABLE IF NOT EXISTS processed_events (
    "PULocationID" INTEGER,
    "DOLocationID" INTEGER,
    trip_distance DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP
);
