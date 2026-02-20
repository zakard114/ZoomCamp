

Markdown
# Data Engineering Zoomcamp 2026 - Module 2 Homework

This repository contains the solutions for the **Data Engineering Zoomcamp 2026** Module 2 homework. All workflow logic, BigQuery queries, and file analysis are documented directly in this README.

## 🚀 Key Highlights

* **Advanced Workflow Orchestration**: Leveraged **Kestra** to build dynamic ETL pipelines, automating the ingestion of NYC Taxi data (Yellow and Green) into **Google Cloud Storage** and **BigQuery**.
* **Historical Data Backfilling**: Efficiently processed the **2021 dataset (Jan-July)** using Kestra's backfill trigger functionality, ensuring data consistency across multiple partitions.

---

## ⚙️ Kestra Orchestration (Assignment)

### Task: Extend existing flows to include data for the year 2021.

To handle the 2021 data, I utilized the **Backfill** feature in Kestra for the `09_gcp_taxi_scheduled` flow. This allowed for automatic execution across the required months without manual triggers.

**Backfill Configuration:**
* **Start Date:** `2021-01-01`
* **End Date:** `2021-07-31`
* **Inputs:** Executed for both `taxi: yellow` and `taxi: green`.

---

## 📊 Quiz Solutions (Questions 1 - 6)

### Q1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size?

To find the size of `yellow_tripdata_2020-12.csv`, I checked the object metadata in the GCS bucket (`gs://kestra-zoomcamp-zakard-demo`).

**Size Calculation:**
* **Reported Size:** `134.5 MB`
* **Calculation:** $134.5 \div 1.048576 \approx 128.26 \text{ MiB}$

> **Result:** `134.5 MB (uncompressed)`
> **Answer:** `128.3 MiB`

---

### Q2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04?

The flow uses the following expression:
`{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`

> **Answer:** `green_tripdata_2020-04.csv`

---

### Q3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

**BigQuery SQL:**

```sql
SELECT 'Yellow 2020' as category, count(*) as row_count
FROM `de-zoomcamp-02-zakard.zoomcamp.yellow_tripdata`
WHERE filename LIKE 'yellow_tripdata_2020%';
Result: 24,648,499 Answer: 24,648,499

Q4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
BigQuery SQL:

SQL
SELECT 'Green 2020' as category, count(*) as row_count
FROM `de-zoomcamp-02-zakard.zoomcamp.green_tripdata`
WHERE filename LIKE 'green_tripdata_2020%';
Result: 1,734,051 Answer: 1,734,051

Q5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
BigQuery SQL:

SQL
SELECT 'Yellow 2021-03' as category, count(*) as row_count
FROM `de-zoomcamp-02-zakard.zoomcamp.yellow_tripdata`
WHERE filename LIKE 'yellow_tripdata_2021-03%';
Result: 1,925,152 Answer: 1,925,152

Q6. How would you configure the timezone to New York in a Schedule trigger?
To set the timezone, the timezone property must be added to the Schedule trigger using the IANA Time Zone database name.

Example YAML Snippet:

YAML
triggers:
  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    timezone: America/New_York
    inputs:
      taxi: yellow
Answer: Add a timezone property set to America/New_York in the Schedule trigger configuration

💡 Engineering Best Practices
Security & Git: Configured .gitignore to strictly exclude .env_encoded and GCP Service Account JSON keys, preventing sensitive credential leaks.

Timezone Synchronization: Managed the 10-hour offset between UTC and local time (UTC+10 in Guam) for accurate trigger monitoring.

Data Validation: Verified BigQuery row counts using the filename metadata column to ensure extraction and loading phases were successful.