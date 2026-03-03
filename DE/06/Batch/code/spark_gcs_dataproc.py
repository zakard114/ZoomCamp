"""
Dataproc job submission - converted from 09_spark_gcs.ipynb
Run on GCP Dataproc. Upload to gs://de-zoomcamp-zakard-2026/code/
"""

# ----- Local Windows settings (commented for Dataproc; uncomment for local run) -----
# import os
# # Windows: Run this first. Set HADOOP_HOME before SparkContext creation.
# _hadoop_dirs = [
#     r"E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5",
#     r"E:\IT_SPACES\AI\ZoomCamp\DE\tools\hadoop-3.3.5",
# ]
# for _d in _hadoop_dirs:
#     if os.path.isdir(_d):
#         os.environ["HADOOP_HOME"] = _d
#         os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.join(_d, "bin")
#         break
# else:
#     pass  # Warning: hadoop folder not found
#
# # Windows: hadoop.home.dir required - set in SparkConf (passed to JVM)
# HADOOP_DIR = r"E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5"
# if not os.path.isdir(HADOOP_DIR):
#     HADOOP_DIR = r"E:\IT_SPACES\AI\ZoomCamp\DE\tools\hadoop-3.3.5"
# os.environ["HADOOP_HOME"] = HADOOP_DIR if os.path.isdir(HADOOP_DIR) else ""
# if os.environ["HADOOP_HOME"]:
#     os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.join(HADOOP_DIR, "bin")
#
# # credentials: specify path below or auto-detect
# credentials_location = None  # e.g. r"C:\Users\<user>\.google\credentials\google_credentials.json"
# if not credentials_location or not os.path.isfile(credentials_location):
#     _candidates = [
#         os.path.join(os.path.expanduser("~"), ".google", "credentials", "google_credentials.json"),
#         os.path.join(os.getcwd(), "google_credentials.json"),
#         os.path.join(r"E:\IT_SPACES\AI\ZoomCamp\DE\06\Batch\code", "google_credentials.json"),
#     ]
#     credentials_location = next((p for p in _candidates if os.path.isfile(p)), None)
# if not credentials_location or not os.path.isfile(credentials_location):
#     raise FileNotFoundError("google_credentials.json not found.")
# credentials_location = os.path.normpath(credentials_location).replace("\\", "/")
#
# from pyspark.conf import SparkConf
# from pyspark.context import SparkContext
# conf = SparkConf() \
#     .setMaster('local[*]') \
#     .setAppName('test') \
#     .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
#     .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
#     .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
# if os.path.isdir(HADOOP_DIR):
#     conf = conf.set("spark.hadoop.hadoop.home.dir", HADOOP_DIR)
# sc = SparkContext(conf=conf)
# hadoop_conf = sc._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
# hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
# hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
# hadoop_conf.set("fs.gs.auth.service.account.enable", "true")
# spark = SparkSession.builder.config(conf=sc.getConf()).getOrCreate()
# ----- End of local Windows settings -----

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Dataproc: no .master('local[*]') - cluster assigns master
spark = SparkSession.builder \
    .appName('gcs-green-taxi') \
    .getOrCreate()

# Data path from GCS
df_green = spark.read.parquet('gs://de-zoomcamp-zakard-2026/pq/green/*/*')

print("Row count:", df_green.count())
df_green.printSchema()

# Column names adjusted for schema (case-sensitive)
df_green.select('VendorID', 'lpep_pickup_datetime', 'trip_distance').show(10)

# 'vendor_id' -> 'VendorID' for schema
df_green.groupBy('VendorID').count().show()

spark.stop()
