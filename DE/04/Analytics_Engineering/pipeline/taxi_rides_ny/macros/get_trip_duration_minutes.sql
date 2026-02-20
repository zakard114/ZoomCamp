{#
    매크로 설명: 승차 시간과 하차 시간을 이용해 주행 시간(분)을 계산합니다.
    사용자님의 DuckDB 환경 및 다른 DB(BigQuery, Snowflake 등)에서도 호환됩니다.
#}

{% macro get_trip_duration_minutes(pickup_datetime, dropoff_datetime) -%}

    -- dbt.datediff는 내부적으로 각 DB에 맞는 SQL(DuckDB는 date_diff)을 생성합니다.
    {{ dbt.datediff(pickup_datetime, dropoff_datetime, 'minute') }}

{%- endmacro %}