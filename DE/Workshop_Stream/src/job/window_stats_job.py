"""
zone_stats 잡: 1분 텀블링, PULocationID별 ride_count, total_amount, avg_distance
Kafka rides → Postgres zone_stats (early-fire 제거: Flink 2.2 호환)
"""
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10_000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # 1. Kafka 소스 + proctime (워터마크 대신 처리시각 기준 윈도우 → 무조건 닫힘)
    t_env.execute_sql("""
        CREATE TABLE events (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            tpep_pickup_datetime BIGINT,
            proc_time AS PROCTIME()
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'rides',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """)

    # 2. zone_stats 싱크: window_start, PULocationID, ride_count, total_amount, avg_distance
    t_env.execute_sql("""
        CREATE TABLE zone_stats (
            window_start TIMESTAMP(3),
            PULocationID INT,
            ride_count BIGINT,
            total_amount DOUBLE,
            avg_distance DOUBLE,
            PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'zone_stats',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """)

    # 3. 1분 텀블링, PULocationID별 count, sum, avg
    t_env.execute_sql("""
        INSERT INTO zone_stats
        SELECT
            window_start,
            PULocationID,
            COUNT(*) AS ride_count,
            SUM(total_amount) AS total_amount,
            AVG(trip_distance) AS avg_distance
        FROM TABLE(
            TUMBLE(TABLE events, DESCRIPTOR(event_ts), INTERVAL '1' MINUTE)
        )
        GROUP BY window_start, window_end, PULocationID;
    """).wait()


if __name__ == "__main__":
    main()
