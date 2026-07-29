"""
최소 테스트 잡: Kafka rides 토픽에서 읽어서 그대로 print sink로 출력
(윈도우/워터마크 없이 잡이 살아있는지 확인용)
"""
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # 1. Kafka 소스 (워터마크 없음, 단순 스키마)
    t_env.execute_sql("""
        CREATE TABLE events (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            tpep_pickup_datetime BIGINT
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'rides',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """)

    # 2. Print 싱크
    t_env.execute_sql("""
        CREATE TABLE print_sink (
            PULocationID INT,
            DOLocationID INT,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            tpep_pickup_datetime BIGINT
        ) WITH (
            'connector' = 'print'
        );
    """)

    # 3. SELECT * → print
    t_env.execute_sql("""
        INSERT INTO print_sink
        SELECT * FROM events;
    """).wait()


if __name__ == "__main__":
    main()
