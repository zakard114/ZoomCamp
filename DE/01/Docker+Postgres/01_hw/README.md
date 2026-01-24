Data Engineering Zoomcamp 2026 - Module 1 Homework
This repository contains the solutions for the Module 1 homework of the Data Engineering Zoomcamp 2026. As per the instructions, all SQL queries and shell commands used for the solutions are documented directly in this README.

🚀 Key Highlights & Applied Strategies
Early Adoption of Orchestration: I integrated Kestra's Backfill feature (originally a Module 2 topic) into this assignment. This allowed for automated, efficient data loading of the October 2019 dataset, significantly improving resource management compared to manual scripts.

Infrastructure as Code (IaC): Used Terraform to provision GCP resources, focusing on professional habits like state management and secure credential handling.

🐳 Docker & SQL (Questions 1 & 2)
Q1. Understanding Docker First Run
Running python:3.12.8 image in interactive mode with bash as the entrypoint to check the pip version:

Bash
docker run -it --entrypoint bash python:3.12.8
# Inside the container
pip --version
Answer: 24.3.1

Q2. Understanding Docker Networking
Based on the provided docker-compose.yaml, for pgadmin to connect to the PostgreSQL database within the same network:

Answer: db:5432

📊 SQL Data Analysis (Questions 3 - 6)
Data Preparation: Loaded green_tripdata_2019-10.csv and taxi_zone_lookup.csv into PostgreSQL.

Total Row Count Check: 476,386

Q3. Trip Segmentation Count
SQL
SELECT
    COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) AS "Up to 1 mile",
    COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) AS "1 to 3 miles",
    COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) AS "3 to 7 miles",
    COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) AS "7 to 10 miles",
    COUNT(CASE WHEN trip_distance > 10 THEN 1 END) AS "Over 10 miles"
FROM green_oct_2019
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
Answer: 104,802; 198,924; 109,603; 27,678; 35,189

Q4. Longest Trip for Each Day
SQL
SELECT lpep_pickup_datetime::date AS pickup_day, MAX(trip_distance) AS max_dist
FROM green_oct_2019
GROUP BY pickup_day
ORDER BY max_dist DESC
LIMIT 1;
Result: 2019-10-31 (Distance: 515.89)

Answer: 2019-10-31

Q5. Three Biggest Pickup Zones
SQL
SELECT z."Zone", SUM(g.total_amount) AS total_sum
FROM green_oct_2019 g
JOIN zones_new z ON g."PULocationID" = z."LocationID"
WHERE g.lpep_pickup_datetime::date = '2019-10-18'
GROUP BY z."Zone"
HAVING SUM(g.total_amount) > 13000
ORDER BY total_sum DESC;
Answer: East Harlem North, East Harlem South, Morningside Heights

Q6. Largest Tip
SQL
SELECT z_drop."Zone" AS dropoff_zone, MAX(g.tip_amount) AS max_tip
FROM green_oct_2019 g
JOIN zones_new z_pick ON g."PULocationID" = z_pick."LocationID"
JOIN zones_new z_drop ON g."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND g.lpep_pickup_datetime >= '2019-10-01' AND g.lpep_pickup_datetime < '2019-11-01'
GROUP BY z_drop."Zone"
ORDER BY max_tip DESC
LIMIT 1;
Result: JFK Airport (Tip: 87.3)

Answer: JFK Airport

🏗️ Terraform (Question 7)
Q7. Terraform Workflow
The sequence for provider setup, execution, and resource cleanup:

Initialize & Download Plugins: terraform init

Generate plan & Auto-execute: terraform apply -auto-approve

Remove all resources: terraform destroy

Answer: terraform init, terraform apply -auto-approve, terraform destroy

💡 Engineering Best Practices
Security: Utilized .gitignore to ensure GCP Service Account keys (.json) and Terraform state files (.tfstate) are never pushed to the public repository.

Standardization: Ran terraform fmt to maintain clean, industry-standard HCL code.

Automation: By pre-learning and applying Kestra, I moved away from manual ingestion scripts to a more scalable orchestration-based approach.