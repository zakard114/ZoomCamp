SELECT 
    -- identifiers
    cast(VendorID as int) as vendor_id,
    cast(RatecodeID as int) as rate_code_id, 
    cast(PULocationID as int) as pickup_location_id, 
    cast(DOLocationID as int) as dropoff_location_id,       
    
    -- timestamps
    cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime, 
    
    -- trip info
    store_and_fwd_flag, 
    cast(passenger_count as int) as passenger_count, 
    cast(trip_distance as float) as trip_distance, 
    -- Yellow에는 trip_type이 없는 경우가 많아 제외하거나 확인 후 추가하세요.
    1 as trip_type, -- yellow taxis can only be street hail (trip type = 1) 

    -- payment info
    cast(fare_amount as numeric) as fare_amount, 
    cast(extra as numeric) as extra, 
    cast(mta_tax as numeric) as mta_tax, 
    cast(tip_amount as numeric) as tip_amount, 
    cast(tolls_amount as numeric) as tolls_amount, 
    0 as ehail_fee, -- yellow taxis do not have ehail fees
    cast(improvement_surcharge as numeric) as improvement_surcharge, 
    cast(total_amount as numeric) as total_amount,  
    cast(payment_type as int) as payment_type      
FROM {{ source('raw_data', 'yellow_tripdata') }} 
WHERE VendorID is not null