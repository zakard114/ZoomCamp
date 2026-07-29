{{
    config(
        materialized='view',
        pre_hook="SET preserve_insertion_order = false;"
    )
}}
-- 이후 SQL 로직...

with trips as (
    -- int_trips 모델을 참조하는 것이 정석입니다 (이미 int_trips가 성공했으므로)
    select * from {{ ref('int_trips') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
)

select
    -- 1. 고유 ID (int_trips에서 이미 생성했다면 t.trip_id로 가져오면 됩니다)
    t.trip_id,
    
    t.vendor_id,
    t.service_type,  -- Contract에서 요구함
    t.rate_code_id,

    -- 2. 위치 정보 결합
    t.pickup_location_id,
    pz.borough as pickup_borough,
    pz.zone as pickup_zone,
    
    t.dropoff_location_id,
    dz.borough as dropoff_borough,
    dz.zone as dropoff_zone,

    t.pickup_datetime,
    t.dropoff_datetime,
    t.store_and_fwd_flag,

    -- 3. 운행 지표 (타입 불일치 방지를 위한 캐스팅)
    t.passenger_count,
    cast(t.trip_distance as DECIMAL(18,3)) as trip_distance,
    t.trip_type, -- Contract에서 요구함

    -- 4. 시간 계산 (이미 매크로를 만드셨다면 호출하거나 직접 계산)
    {{ get_trip_duration_minutes('t.pickup_datetime', 't.dropoff_datetime') }} as trip_duration_minutes,

    -- 5. 결제 및 금액 정보 (Contract의 DECIMAL(18,3) 규격에 맞춤)
    cast(t.fare_amount as DECIMAL(18,3)) as fare_amount,
    cast(t.extra as DECIMAL(18,3)) as extra,
    cast(t.mta_tax as DECIMAL(18,3)) as mta_tax,
    cast(t.tip_amount as DECIMAL(18,3)) as tip_amount,
    cast(t.tolls_amount as DECIMAL(18,3)) as tolls_amount,
    cast(coalesce(t.ehail_fee, 0) as DECIMAL(18,3)) as ehail_fee, -- Contract에서 요구함
    cast(t.improvement_surcharge as DECIMAL(18,3)) as improvement_surcharge,
    cast(t.total_amount as DECIMAL(18,3)) as total_amount,
    
    t.payment_type,
    t.payment_type_description

from trips t
left join dim_zones as pz
    on t.pickup_location_id = pz.location_id
left join dim_zones as dz
    on t.dropoff_location_id = dz.location_id