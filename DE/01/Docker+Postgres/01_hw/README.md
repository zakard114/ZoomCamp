# Data Engineering Zoomcamp 2026 - Module 1 Homework

This repository contains the solutions for the **Data Engineering Zoomcamp 2026** Module 1 homework. All commands and SQL queries are documented directly in this README.

## 🚀 Key Highlights

* **Early Adoption of Orchestration**: Integrated **Kestra's Backfill feature** (originally a Module 2 topic) to automate and optimize the data loading process for the October 2019 dataset.
* **Infrastructure as Code (IaC)**: Provisioned GCP resources using **Terraform**, implementing professional state management and security practices.

---

## 🐳 Docker & Networking (Questions 1 & 2)

### Q1. Understanding Docker First Run

To check the `pip` version in the `python:3.12.8` image, I executed the following in the terminal:

**Run the container:**

```bash
docker run -it --entrypoint bash python:3.12.8

```

**Check version inside the container:**

```bash
pip --version

```

> **Result:** `pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)`
> **Answer:** `24.3.1`

### Q2. Understanding Docker Networking

Based on the `docker-compose.yaml`, `pgadmin` connects to the PostgreSQL database using the following hostname and port:

> **Answer:** `db:5432`

---

## 📊 SQL Data Analysis (Questions 3 - 6)

### Q3. Trip Segmentation Count

```sql
SELECT 
    COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) AS "Up to 1 mile", 
    COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) AS "1 to 3 miles", 
    COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) AS "3 to 7 miles", 
    COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) AS "7 to 10 miles", 
    COUNT(CASE WHEN trip_distance > 10 THEN 1 END) AS "Over 10 miles" 
FROM green_oct_2019 
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01' 
  AND lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';

```

> **Answer:** `104,802; 198,924; 109,603; 27,678; 35,189`

### Q4. Longest Trip for Each Day

```sql
SELECT 
    lpep_pickup_datetime::date AS pickup_day, 
    MAX(trip_distance) AS max_dist 
FROM green_oct_2019 
GROUP BY pickup_day 
ORDER BY max_dist DESC 
LIMIT 1;

```

> **Answer:** `2019-10-31`

### Q5. Three Biggest Pickup Zones

```sql
SELECT 
    z."Zone", 
    SUM(g.total_amount) AS total_sum 
FROM green_oct_2019 g 
JOIN zones_new z ON g."PULocationID" = z."LocationID" 
WHERE g.lpep_pickup_datetime::date = '2019-10-18' 
GROUP BY z."Zone" 
HAVING SUM(g.total_amount) > 13000 
ORDER BY total_sum DESC;

```

> **Answer:** `East Harlem North, East Harlem South, Morningside Heights`

### Q6. Largest Tip (Pickup: East Harlem North)

```sql
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

```

> **Answer:** `JFK Airport`

---

## 🏗️ Terraform (Question 7)

### Q7. Terraform Workflow Sequence

1. **Initialize**: `terraform init`
2. **Apply with Auto-approve**: `terraform apply -auto-approve`
3. **Destroy**: `terraform destroy`

> **Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

---

## 💡 Engineering Best Practices

* **Security**: Utilized `.gitignore` to prevent GCP Service Account keys and `.tfstate` files from being exposed.
* **Standardization**: Used `terraform fmt` for clean, consistent code formatting.
* **Automation**: Applied Kestra orchestration to replace manual ingestion tasks.
