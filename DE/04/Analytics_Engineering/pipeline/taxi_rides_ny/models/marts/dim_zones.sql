/* File: models/core/dim_zones.sql */

with taxi_zone_lookup as (
    select * from {{ ref('taxi_zone_lookup') }}
),

renamed as (
    select
        -- Cast to int64 for BigQuery compatibility
        cast(locationid as int64) as location_id,
        
        -- Explicitly cast strings to avoid varchar issues
        cast(borough as string) as borough,
        cast(zone as string) as zone,
        cast(replace(service_zone, 'Boro', 'Green') as string) as service_zone
        
    from taxi_zone_lookup
)

select * from renamed   