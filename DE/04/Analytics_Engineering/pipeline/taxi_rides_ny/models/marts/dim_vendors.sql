{{
    config(
        materialized='view'
    )
}}

with trips as (
    -- 원본의 ref('int_trips_unioned')를 ref('fct_trips')로 변경합니다.
    -- 이렇게 해야 fct_trips 바로 뒤에 브랜치로 붙게 됩니다.
    select * from {{ ref('fct_trips') }}
),

vendors as (
    select
        DISTINCT vendor_id,
        -- 매크로를 사용하여 vendor_id를 이름(Creative, Verifone 등)으로 변환
        {{ get_vendor_names('vendor_id') }} as vendor_name
    from trips
)

select * from vendors