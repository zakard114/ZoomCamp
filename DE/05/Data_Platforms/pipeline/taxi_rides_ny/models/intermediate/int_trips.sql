-- Enrich and deduplicate trip data
-- Location: models/intermediate/int_trips.sql

with unioned as (
    select * from {{ ref('int_trips_unioned') }}
),

payment_types as (
    select * from {{ ref('payment_type_lookup') }}
),

cleaned_and_enriched as (
    select
        -- 1. dbt_utils가 설치 안 되었을 경우를 대비한 surrogate key 생성 (DuckDB 호환)
        md5(cast(coalesce(cast(u.vendor_id as string), '') || '-' || 
                 coalesce(cast(u.pickup_datetime as string), '') || '-' || 
                 coalesce(cast(u.pickup_location_id as string), '') || '-' || 
                 coalesce(cast(u.service_type as string), '') as string)) as trip_id,

        -- Identifiers
        u.vendor_id,
        u.service_type,
        u.rate_code_id,

        -- Location IDs
        u.pickup_location_id,
        u.dropoff_location_id,

        -- Timestamps
        u.pickup_datetime,
        u.dropoff_datetime,

        -- Trip details
        u.store_and_fwd_flag,
        u.passenger_count,
        u.trip_distance,
        u.trip_type,

        -- Payment breakdown
        u.fare_amount,
        u.extra,
        u.mta_tax,
        u.tip_amount,
        u.tolls_amount,
        u.ehail_fee,
        u.improvement_surcharge,
        u.total_amount,

        -- 2. 시드 데이터와 조인 (컬럼명 주의: pt.payment_type_description으로 수정)
        coalesce(u.payment_type, 0) as payment_type,
        coalesce(pt.payment_type_description, 'Unknown') as payment_type_description

    from unioned u
    left join payment_types pt
        on cast(u.payment_type as integer) = cast(pt.payment_type as integer)
)

select * from cleaned_and_enriched

-- 3. 중복 제거: DuckDB에서 지원하는 qualify 구문 사용
qualify row_number() over(
    partition by vendor_id, pickup_datetime, pickup_location_id, service_type
    order by dropoff_datetime
) = 1