# BigQuery Homework 3: 2024 Yellow Taxi Data Analysis

This folder contains the SQL solutions for the Module 3 homework, focusing on BigQuery optimization techniques such as Partitioning, Clustering, and Metadata utilization.

## 📂 Project Structure

```text
ZoomCamp/DE/03/Data_Warehouse_and_BigQuery/03_hw/
├── homework_3_solution.sql   # Full SQL script with DDL and analysis queries
└── README.md                 # Summary of findings and project overview


# BigQuery Homework 3: 2024 Yellow Taxi Data Analysis

This folder contains the SQL solutions for the Module 3 homework, focusing on BigQuery optimization techniques such as Partitioning, Clustering, and Metadata utilization.

## Key Takeaways

### 1. External vs. Native (Regular) Tables
- **External Tables**: Data stays in GCS. BigQuery only stores the schema metadata. Pre-execution "Bytes Processed" shows 0 B because the size is unknown until the files are actually scanned.
- **Native Tables**: Data is ingested into BigQuery storage. This allows for **Metadata-only scans** (0 B processed) for queries like `COUNT(*)`.

### 2. Optimization Results (Question 6)
- **Non-partitioned Table**: Scanned **310.24 MB** for the March 1st-15th range.
- **Partitioned & Clustered Table**: Scanned only **26.84 MB** for the same range.
- **Result**: Partitioning by day and clustering by VendorID achieved a **~91% reduction** in data scanned.

### 3. Storage Efficiency
- Moving data from GCS to BigQuery Native storage enables powerful features like **Clustering** and **Automatic Statistics**, which are essential for cost-effective data engineering.

## SQL Scripts
- [homework_3_solution.sql](./homework_3_solution.sql): Contains all the DDL and DML queries used for this assignment.