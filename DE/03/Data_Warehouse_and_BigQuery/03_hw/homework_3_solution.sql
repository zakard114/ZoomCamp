
-- 0. Environment Setup (Assumes dataset creation is already completed)

-- 1. Creating an External Table
-- This table references Parquet files stored directly in Google Cloud Storage (GCS).
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-zakard-demo/yellow_tripdata_2024-*.parquet']
);

-- 2. Creating a Native (Regular) Table
-- This imports data from the external table into BigQuery's managed storage.
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular` AS
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata_2024`;

-- [Question 1] Check total record count
SELECT count(*) 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;

-- [Question 2] Compare estimated bytes for PULocationID (Dry Run)
-- External Table: Shows 0 B (metadata-only reference)
-- Native Table: Shows actual column size (~155.12 MB)
SELECT DISTINCT(PULocationID) 
FROM `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata_2024`;

SELECT DISTINCT(PULocationID) 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;

-- [Question 3] Compare bytes scanned by the number of columns
-- BigQuery is a columnar database; scanning more columns increases data processed.
SELECT PULocationID 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;

SELECT PULocationID, DOLocationID 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;

-- [Question 4] Find records with fare_amount equal to 0
SELECT count(*) 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular` 
WHERE fare_amount = 0;

-- [Question 5] Create an Optimized Table (Partitioning & Clustering)
-- Using the internal 'regular' table as the source for better reliability.
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;

-- [Question 6] Performance Comparison: Non-partitioned vs Partitioned Table
-- Non-partitioned scans the entire table's relevant columns (~310.24 MB).
-- Partitioned table prunes data and only scans specific date ranges (~26.84 MB).
SELECT DISTINCT(VendorID)
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT(VendorID)
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- [Question 9 - Bonus] Metadata-only scan (0 B)
-- BigQuery retrieves the row count from table statistics without scanning files.
SELECT count(*) 
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_2024_regular`;