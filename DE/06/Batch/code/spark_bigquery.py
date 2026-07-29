"""
Dataproc job - read GCS Parquet, write BigQuery.
Upload to gs://de-zoomcamp-zakard-2026/code/
Target: bruin-de-zoomcamp.reports.green_revenue_2020
"""

# ----- Local Windows settings (commented for Dataproc; uncomment for local run) -----
# import os
# HADOOP_DIR = r"E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5"
# ...
# credentials_location = ...
# conf = SparkConf().setMaster('local[*]').set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar")
# ----- End of local Windows settings -----

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName('gcs-to-bigquery') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', 'dataproc-temp-us-central1-123863166112-12wrgrap')

df_green = spark.read.parquet('gs://de-zoomcamp-zakard-2026/pq/green/*/*')
df_green.createOrReplaceTempView('green')

df_revenue = spark.sql("""
SELECT
    date_trunc('hour', lpep_pickup_datetime) AS hour,
    PULocationID AS zone,
    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    green
WHERE
    lpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
""")

df_revenue.write.format('bigquery') \
    .option('table', 'bruin-de-zoomcamp.reports.green_revenue_2020') \
    .mode('overwrite') \
    .save()

print("Written to bruin-de-zoomcamp.reports.green_revenue_2020")
spark.stop()
