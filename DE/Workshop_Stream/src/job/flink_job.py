"""
Question 4: green-trips → 5분 텀블링 윈도우 → PULocationID별 num_trips → processed_trips
Question 5: green-trips → 세션 윈도우(gap 30min) → longest streak = MAX(num_trips) per session
Question 6: green-trips → 1시간 텀블링 윈도우 → SUM(tip_amount) per hour → processed_trips_window
- parallelism 1 필수 (green-trips 1 파티션, 워터마크 진행)
"""
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


def run_flink_job():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Kafka 소스 (tip_amount 포함, Question 6용)
    source_ddl = """
        CREATE TABLE green_trips (
            lpep_pickup_datetime VARCHAR,
            PULocationID INT,
            tip_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'flink-consumer-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """
    t_env.execute_sql(source_ddl)

    # Question 4: processed_trips (5분 윈도우, PULocationID별 num_trips)
    sink_ddl_q4 = """
        CREATE TABLE processed_trips (
            window_start TIMESTAMP(3),
            pulocationid BIGINT,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'processed_trips',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """
    t_env.execute_sql(sink_ddl_q4)

    # Question 5: session_streaks (세션 윈도우, gap 5분, PULocationID별 → max num_trips = 12~81)
    sink_ddl_q5 = """
        CREATE TABLE session_streaks (
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            pulocationid BIGINT,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'session_streaks',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """
    t_env.execute_sql(sink_ddl_q5)

    # Question 6: processed_trips_window (1시간 윈도우, SUM(tip_amount))
    sink_ddl_q6 = """
        CREATE TABLE processed_trips_window (
            window_start TIMESTAMP(3),
            sum_tip DOUBLE
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'processed_trips_window',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """
    t_env.execute_sql(sink_ddl_q6)

    # Question 4: 5분 텀블링 윈도우
    t_env.execute_sql("""
        INSERT INTO processed_trips
        SELECT
            TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
            PULocationID AS pulocationid,
            COUNT(*) AS num_trips
        FROM green_trips
        GROUP BY TUMBLE(event_timestamp, INTERVAL '5' MINUTE), PULocationID
    """)

    # Question 5: 세션 윈도우 (gap 5분, PULocationID별) → longest streak = max num_trips
    t_env.execute_sql("""
        INSERT INTO session_streaks
        SELECT
            SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS session_start,
            SESSION_END(event_timestamp, INTERVAL '5' MINUTE) AS session_end,
            PULocationID AS pulocationid,
            COUNT(*) AS num_trips
        FROM green_trips
        GROUP BY PULocationID, SESSION(event_timestamp, INTERVAL '5' MINUTE)
    """)

    # Question 6: 1시간 텀블링 윈도우, SUM(tip_amount)
    t_env.execute_sql("""
        INSERT INTO processed_trips_window
        SELECT
            TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
            COALESCE(SUM(tip_amount), 0) AS sum_tip
        FROM green_trips
        GROUP BY TUMBLE(event_timestamp, INTERVAL '1' HOUR)
    """).wait()


if __name__ == '__main__':
    run_flink_job()
