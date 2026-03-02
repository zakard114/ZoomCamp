"""
08_rdds revenue 집계 - RDD/Python worker 없이 실행 (Windows 대응)
실행: E:\\IT_SPACES\\AI\\ZoomCamp\\DE\\06\\venv\\Scripts\\python.exe run_revenue_no_rdd.py
또는: cd DE\\06\\Batch\\code && ..\\..\\venv\\Scripts\\python run_revenue_no_rdd.py
"""
import os
import sys

# HADOOP_HOME
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
for HADOOP_DIR in [
    os.path.join(SCRIPT_DIR, "..", "..", "tools", "hadoop-3.3.5"),
    os.path.join(SCRIPT_DIR, "..", "..", "..", "tools", "hadoop-3.3.5"),
]:
    HADOOP_DIR = os.path.abspath(HADOOP_DIR)
    if os.path.exists(os.path.join(HADOOP_DIR, "bin", "winutils.exe")):
        os.environ["HADOOP_HOME"] = HADOOP_DIR
        os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.join(HADOOP_DIR, "bin")
        break

os.chdir(SCRIPT_DIR)

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("revenue") \
    .getOrCreate()

df_green = spark.read.parquet("data/pq/green/2020/01")
df_result = df_green \
    .filter(F.col("lpep_pickup_datetime") >= "2020-01-01") \
    .withColumn("hour", F.date_trunc("hour", F.col("lpep_pickup_datetime"))) \
    .groupBy("hour", "PULocationID") \
    .agg(
        F.sum("total_amount").alias("revenue"),
        F.count(F.lit(1)).alias("count")
    ) \
    .withColumnRenamed("PULocationID", "zone")

out_dir = "tmp/green-revenue"
os.makedirs(out_dir, exist_ok=True)
df_result.toPandas().to_parquet(os.path.join(out_dir, "data.parquet"), index=False)
print(f"저장 완료: {out_dir}/data.parquet")

spark.stop()
