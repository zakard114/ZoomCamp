/* File: models/intermediate/int_trips.sql */

{{ config(materialized='table') }}

with unioned as (
    select * from {{ ref('int_trips_unioned') }}
),

payment_types as (
    select * from {{ ref('payment_type_lookup') }}
),

cleaned_and_enriched as (
    select
        -- Wrap MD5 with TO_HEX to return a STRING instead of BYTES
        to_hex(md5(concat(
            coalesce(cast(u.vendor_id as string), ''),
            coalesce(cast(u.pickup_datetime as string), ''),
            coalesce(cast(u.pickup_location_id as string), ''),
            coalesce(cast(u.service_type as string), '')
        ))) as trip_id,

        u.vendor_id,
        cast(u.service_type as string) as service_type,
        u.rate_code_id,
        u.pickup_location_id,
        u.dropoff_location_id,
        u.pickup_datetime,
        u.dropoff_datetime,
        u.store_and_fwd_flag,
        u.passenger_count,
        u.trip_distance,
        u.trip_type,
        u.fare_amount,
        u.extra,
        u.mta_tax,
        u.tip_amount,
        u.tolls_amount,
        u.ehail_fee,
        u.improvement_surcharge,
        u.total_amount,
        coalesce(u.payment_type, 0) as payment_type,
        cast(coalesce(pt.payment_type_description, 'Unknown') as string) as payment_type_description

    from unioned u
    left join payment_types pt
        on cast(u.payment_type as int64) = cast(pt.payment_type as int64)
)

select * from cleaned_and_enriched
qualify row_number() over(
    partition by vendor_id, pickup_datetime, pickup_location_id, service_type
    order by dropoff_datetime
) = 1