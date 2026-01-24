/* Data Engineering Zoomcamp 2026
  Module 1 Homework: SQL Solutions
*/

-- Q3. Trip Segmentation Count
-- Period: October 1st 2019 (inclusive) to November 1st 2019 (exclusive)
SELECT 
    COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) AS "Up to 1 mile", 
    COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) AS "1 to 3 miles", 
    COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) AS "3 to 7 miles", 
    COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) AS "7 to 10 miles", 
    COUNT(CASE WHEN trip_distance > 10 THEN 1 END) AS "Over 10 miles" 
FROM green_oct_2019 
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01' 
  AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';

-- Q4. Longest trip for each day
-- Finding the pickup day with the longest trip distance
SELECT 
    lpep_pickup_datetime::date AS pickup_day, 
    MAX(trip_distance) AS max_dist 
FROM green_oct_2019 
GROUP BY pickup_day 
ORDER BY max_dist DESC 
LIMIT 1;

-- Q5. Three biggest pickup zones
-- Zones with total_amount sum > 13,000 on 2019-10-18
SELECT 
    z."Zone", 
    SUM(g.total_amount) AS total_sum 
FROM green_oct_2019 g 
JOIN zones_new z ON g."PULocationID" = z."LocationID" 
WHERE g.lpep_pickup_datetime::date = '2019-10-18' 
GROUP BY z."Zone" 
HAVING SUM(g.total_amount) > 13000 
ORDER BY total_sum DESC;

-- Q6. Largest tip
-- Dropoff zone with the largest tip for passengers picked up in "East Harlem North"
SELECT 
    z_drop."Zone" AS dropoff_zone, 
    MAX(g.tip_amount) AS max_tip 
FROM green_oct_2019 g 
JOIN zones_new z_pick ON g."PULocationID" = z_pick."LocationID" 
JOIN zones_new z_drop ON g."DOLocationID" = z_drop."LocationID" 
WHERE z_pick."Zone" = 'East Harlem North' 
  AND g.lpep_pickup_datetime >= '2019-10-01' AND g.lpep_pickup_datetime < '2019-11-01' 
GROUP BY z_drop."Zone" 
ORDER BY max_tip DESC 
LIMIT 1;