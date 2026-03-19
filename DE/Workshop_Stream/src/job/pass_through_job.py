"""
?�이?��? 그�?�??�과?�키??Flink ??(Pass-through Job)
?�이??컨슈머�? ?�던 ?�을 Flink�??�일?�게 구현?�니??
"""
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_events_source_kafka(t_env):
    """카프카에???�이?��? ?�어?�기 ?�한 가???�이블을 ?�의?�니??"""
    table_name = "events"
    # Flink SQL DDL 문법???�용?�여 카프카�? ?�결???�이블을 ?�성?�니??
    source_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,      -- ?�차 ?�치 ID
            DOLocationID INTEGER,      -- ?�차 ?�치 ID
            trip_distance DOUBLE,      -- 주행 거리
            total_amount DOUBLE,       -- �??�금
            tpep_pickup_datetime BIGINT -- Unix ?�?�스?�프 (밀리초 ?�위)
        ) WITH (
            'connector' = 'kafka',     -- 카프�?커넥???�용
            'properties.bootstrap.servers' = 'redpanda:29092', -- ?�커 ?��? ?�트?�크??Redpanda 주소
            'topic' = 'rides',         -- 구독??카프�??�픽 ?�름
            'scan.startup.mode' = 'earliest-offset', -- ?�픽 처음부??모든 메시지 ?�음 (?�험??
            'properties.auto.offset.reset' = 'earliest', -- ?�프??초기값이 ?�을 경우 처음부???�기
            'format' = 'json'          -- ?�이???�맷?� JSON?�로 ?�동 ??��?�화
        );
        """
    t_env.execute_sql(source_ddl)  # SQL문을 ?�행?�여 ?�경???�이블을 ?�록?�니??
    return table_name


def create_processed_events_sink_postgres(t_env):
    """?�이?��? ?�보??목적지(Postgres)�??�의?�니?? JDBC 커넥?�로 psycopg2/INSERT 불필??"""
    table_name = 'processed_events'
    # JDBC 커넥?��? ?�용?�여 PostgreSQL ?�이블과 ?�결?�니??
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            pickup_datetime TIMESTAMP -- 가공된 ?�?�스?�프 ?�?�용
        ) WITH (
            'connector' = 'jdbc',      -- JDBC 커넥???�용
            'url' = 'jdbc:postgresql://postgres:5432/postgres', -- ?�커 ?��???Postgres 주소
            'table-name' = '{table_name}', -- ?�제 DB ???�이�??�름
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver' -- Postgres JDBC ?�라?�버 지??
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name


def log_processing():
    """?�행 로직: ?�트리밍 ?�경 ?�정 ??Kafka ??Postgres ?�이?�라?�을 가?�합?�다."""
    # 1. ?�트리밍 ?�행 ?�경???�정?�니??
    env = StreamExecutionEnvironment.get_execution_environment()

    # 2. 체크?�인???�성??(10초마???�태�??�?�합?�다).
    #    ?�애 발생 ??마�?�??�??지?��????�동?�로 복구?�게 ?�줍?�다.
    env.enable_checkpointing(10 * 1000)

    # 3. ?�이�??�경 ?�정???�성?�고 ?�트리밍 모드�?지?�합?�다.
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        # 4. ?�스(카프�??� ?�크(Postgres) ?�이블을 ?�성?�니??
        source_table = create_events_source_kafka(t_env)
        postgres_sink = create_processed_events_sink_postgres(t_env)

        # 5. SQL???�행?�여 ?�이?�라?�을 가?�합?�다.
        #    TO_TIMESTAMP_LTZ ?�수�??�자???�?�스?�프�??�간 ?�식?�로 변?�합?�다.
        #    .wait()???�이 종료???�까지 ?�기합?�다 (?�트리밍?��?�??�실??계속 ?�행??.
        t_env.execute_sql(
            f"""
            INSERT INTO {postgres_sink}
            SELECT
                PULocationID,
                DOLocationID,
                trip_distance,
                total_amount,
                TO_TIMESTAMP_LTZ(tpep_pickup_datetime, 3) as pickup_datetime
            FROM {source_table}
            """
        ).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))


if __name__ == '__main__':
    log_processing()
