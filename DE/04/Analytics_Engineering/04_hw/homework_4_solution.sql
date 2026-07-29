-- homework_4_solution.sql

-- 0. Environment Setup
-- Tool: DuckDB v1.4.3, dbt v1.11.2
-- Hardware: 12GB RAM (Applied threads: 1, memory_limit: '3GB' in profiles.yml)

-- [Question 1] dbt run --select int_trips_unioned builds which models?
-- Execution:
-- $ dbt run --select int_trips_unioned
/* 1 of 1 START sql view model dev.int_trips_unioned ........... [RUN]
   1 of 1 OK created sql view model dev.int_trips_unioned ...... [OK in 0.52s]
   Done. PASS=1
*/
-- Result: int_trips_unioned only


-- [Question 2] New value 6 appears in payment_type. What happens on dbt test?
-- Rationale: dbt generic tests (accepted_values) fail when a data violation occurs.
-- Result: dbt fails the test with non-zero exit code


-- [Question 3] Count of records in fct_monthly_zone_revenue?
-- Logic: 24 months * ~265 zones * 2 service types
SELECT count(*) AS total_count 
FROM dev.fct_monthly_zone_revenue;

-- Result: 12998


-- [Question 4] Zone with highest revenue for Green taxis in 2020?
SELECT 
    pickup_zone, 
    SUM(total_amount) AS total_revenue
FROM dev.fct_trips 
WHERE 
    service_type = 'Green'
    AND CAST(pickup_datetime AS DATE) BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

/* Result:
┌───────────────────┬───────────────┐
│    pickup_zone    │ total_revenue │
├───────────────────┼───────────────┤
│ East Harlem North │  1816608.850  │
└───────────────────┴───────────────┘
*/


-- [Question 5] Total trips for Green taxis in October 2019?
SELECT 
    SUM(total_monthly_trips) as total_trips_oct_2019
FROM dev.fct_monthly_zone_revenue
WHERE 
    service_type = 'Green' 
    AND date_trunc('month', revenue_month) = '2019-10-01';

/* Result:
┌──────────────────────┐
│ total_trips_oct_2019 │
├──────────────────────┤
│        384624        │
└──────────────────────┘
*/


-- [Question 6] Count of records in stg_fhv_tripdata (dispatching_base_num IS NOT NULL)?
-- Optimized CSV Scan for 43M+ records
SET memory_limit = '4GB';

SELECT count(*) 
FROM read_csv_auto('E:/IT_SPACES/AI/ZoomCamp/DE/04/materials/hw04_materials/fhv_tripdata_2019-*.csv.gz')
WHERE dispatching_base_num IS NOT NULL;

/* Result:
┌─────────────────┐
│   count_star()  │
├─────────────────┤
│    43244693     │
└─────────────────┘
*/