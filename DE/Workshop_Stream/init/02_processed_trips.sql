-- flink_job.py JDBC sink 스키마 (컬럼명 소문자: JDBC가 unquoted로 삽입 시 PostgreSQL이 lowercase로 해석)
CREATE TABLE IF NOT EXISTS processed_trips (
    window_start TIMESTAMP(3),
    pulocationid INTEGER,
    num_trips BIGINT
);
