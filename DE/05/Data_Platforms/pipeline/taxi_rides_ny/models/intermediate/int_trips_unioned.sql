with green_tripdata as (
    -- Green 택시 데이터임을 식별하기 위해 service_type 추가
    SELECT *, 'Green' as service_type FROM {{ ref('stg_green_tripdata') }}
),

yellow_tripdata as (
    -- Yellow 택시 데이터임을 식별하기 위해 service_type 추가
    SELECT *, 'Yellow' as service_type FROM {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    SELECT * FROM green_tripdata  
    union all
    SELECT * FROM yellow_tripdata 
)

SELECT * FROM trips_unioned