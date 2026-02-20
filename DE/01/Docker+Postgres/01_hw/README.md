# Data Engineering Zoomcamp 2026 - Module 1 Homework

This repository contains the solutions for the **Data Engineering Zoomcamp 2026** Module 1 homework. All commands and SQL queries are documented directly in this README.

## 🚀 Key Highlights

* **Early Adoption of Orchestration**: Integrated **Kestra's pipeline** to automate and optimize the data loading process for the **November 2025 dataset**, ensuring efficient ingestion of Parquet and CSV files into PostgreSQL.
* **Infrastructure as Code (IaC)**: Provisioned GCP resources using **Terraform**, implementing professional state management and security practices.

---

## 🐳 Docker & Networking (Questions 1 & 2)

### Q1. What's the version of pip in the python:3.13 image? 

To check the `pip` version in the `python:3.12.8` image, I executed the following in the terminal:

**Run & check version inside the container:**

```bash
$ docker run -it --rm python:3.13 pip --version

```

> **Result:** `pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)`
> **Answer:** `25.3`

---

### Q2. Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database? 

Based on the `docker-compose.yaml`, `pgadmin` connects to the PostgreSQL database using the following hostname and port:

> **Answer:** `db:5432`

**Clarification on Hostname:**
In my local development environment, I configured the Postgres service name as `pgdatabase` in `docker-compose.yaml`. Therefore, I use `pgdatabase:5432` to connect via pgAdmin. However, based on the **official homework 1 question 2 provided YAML snippet**, the service is defined as `db:`. 

Since Docker Compose uses the service name as the network hostname, the correct answer for the quiz is **`db:5432`**, while my actual implementation uses **`pgdatabase:5432`**.

---

## 📊 SQL Data Analysis (Questions 3 - 6)

### Q3. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles. 

```sql
SELECT count(*) 
FROM public.green_tripdata_2025_11 
WHERE trip_distance <= 1.0 
  AND lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01';

```

> **Answer:** `8,007`

### Q4. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles. 

```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE) AS pickup_day, 
    MAX(trip_distance) AS max_distance
FROM public.green_tripdata_2025_11
WHERE trip_distance < 100
GROUP BY CAST(lpep_pickup_datetime AS DATE)
ORDER BY max_distance DESC
LIMIT 1;

/* or

SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day, 
    MAX(trip_distance) AS max_distance
FROM public.green_tripdata_2025_11
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;
*/
```

> **Answer:** `2025-11-14`

### Q5. Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```sql
SELECT 
    z.zone AS pickup_zone, 
    SUM(g.total_amount) AS total_revenue
FROM public.green_tripdata_2025_11 g
JOIN public.taxi_zone_lookup z 
  ON g.pulocationid::integer = z.locationid
WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z.zone
ORDER BY total_revenue DESC
LIMIT 1;

```

> **Answer:** `East Harlem North`

### Q6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? 

```sql
SELECT 
    z_do.zone AS dropoff_zone, 
    MAX(g.tip_amount) AS max_tip
FROM public.green_tripdata_2025_11 g
JOIN public.taxi_zone_lookup z_pu 
  ON g.pulocationid::integer = z_pu.locationid
JOIN public.taxi_zone_lookup z_do 
  ON g.dolocationid::integer = z_do.locationid
WHERE z_pu.zone = 'East Harlem North'
  AND g.lpep_pickup_datetime >= '2025-11-01' 
  AND g.lpep_pickup_datetime < '2025-12-01'
GROUP BY z_do.zone
ORDER BY max_tip DESC
LIMIT 1;

```

> **Answer:** `Yorkville West`

---

## 🏗️ Terraform (Question 7)

### Q7. Which of the following sequences describes the Terraform workflow for: 1. Downloading plugins and setting up backend, 2. Generating and executing changes, 3. Removing all resources? 

1. **Initialize**: `terraform init`
2. **Apply with Auto-approve**: `terraform apply -auto-approve`
3. **Destroy**: `terraform destroy`

> **Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

---

## 💡 Engineering Best Practices

* **Security**: Utilized `.gitignore` to prevent GCP Service Account keys and `.tfstate` files from being exposed.
* **Standardization**: Used `terraform fmt` for clean, consistent code formatting.
* **Automation**: Applied Kestra orchestration to replace manual ingestion tasks.
