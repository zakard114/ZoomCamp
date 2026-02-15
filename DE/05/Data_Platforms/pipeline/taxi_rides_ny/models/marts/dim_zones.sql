with taxi_zone_lookup as (
    select * from {{ ref('taxi_zone_lookup') }}
),

renamed as (
    select
        -- 1. LocationID를 location_id로 변경 (fct_trips와 연결 고리)
        locationid as location_id,
        
        -- 2. 가독성을 위해 소문자 표준화 (선택 사항이나 권장)
        borough,
        zone,
        replace(service_zone, 'Boro', 'Green') as service_zone -- 참고: 소문자로 자동 변환되거나 명시해주는게 좋습니다.
    from taxi_zone_lookup
)

select * from renamed