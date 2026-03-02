# raw_to_parquet.py
"""
data/raw/ 의 Green, Yellow CSV(.gz) 파일을 Parquet으로 변환
→ df_green = spark.read.parquet('data/pq/green/*/*')
→ df_yellow = spark.read.parquet('data/pq/yellow/*/*')

USE_PANDAS=True: winutils 없이 pandas+pyarrow로 변환 (윈도우 권장)
USE_PANDAS=False: Spark 사용 (winutils 필요)
"""

import os
import glob

# winutils 없으면 True로 변경
USE_PANDAS = True

# ========== Pandas 경로 (winutils 불필요) ==========
def run_pandas():
    import pandas as pd
    try:
        import pyarrow  # to_parquet에 필요
    except ImportError:
        raise ImportError("pyarrow 필요: pip install pyarrow")

    # Green
    green_paths = glob.glob("data/raw/green/2021/01/*.csv.gz")
    os.makedirs("data/pq/green/2021/01", exist_ok=True)
    for p in green_paths:
        df = pd.read_csv(p)
        out = "data/pq/green/2021/01/" + os.path.basename(p).replace(".csv.gz", ".parquet")
        df.to_parquet(out, index=False)
    print("Green 변환 완료: data/pq/green/2021/01/")

    # Yellow
    yellow_paths = glob.glob("data/raw/yellow/2021/01/*.csv.gz")
    os.makedirs("data/pq/yellow/2021/01", exist_ok=True)
    for p in yellow_paths:
        df = pd.read_csv(p)
        out = "data/pq/yellow/2021/01/" + os.path.basename(p).replace(".csv.gz", ".parquet")
        df.to_parquet(out, index=False)
    print("Yellow 변환 완료: data/pq/yellow/2021/01/")

    print("완료 (pandas).")

# ========== Spark 경로 (winutils 필요) ==========
def run_spark():
    from pyspark.sql import SparkSession
    from pyspark.sql import types

    # 윈도우용 hadoop 경로 (winutils.exe 있는 폴더의 상위)
    HADOOP_DIRS = [
        r"E:\IT_SPACES\AI\ZoomCamp\DE\tools\hadoop-3.2.0",
        r"E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.2.0",
        r"C:\hadoop",
    ]
    hadoop_home = None
    for d in HADOOP_DIRS:
        if os.path.exists(os.path.join(d, "bin", "winutils.exe")):
            hadoop_home = d.replace("\\", "/")
            break

    green_schema = types.StructType([
        types.StructField("VendorID", types.IntegerType(), True),
        types.StructField("lpep_pickup_datetime", types.TimestampType(), True),
        types.StructField("lpep_dropoff_datetime", types.TimestampType(), True),
        types.StructField("store_and_fwd_flag", types.StringType(), True),
        types.StructField("RatecodeID", types.IntegerType(), True),
        types.StructField("PULocationID", types.IntegerType(), True),
        types.StructField("DOLocationID", types.IntegerType(), True),
        types.StructField("passenger_count", types.IntegerType(), True),
        types.StructField("trip_distance", types.DoubleType(), True),
        types.StructField("fare_amount", types.DoubleType(), True),
        types.StructField("extra", types.DoubleType(), True),
        types.StructField("mta_tax", types.DoubleType(), True),
        types.StructField("tip_amount", types.DoubleType(), True),
        types.StructField("tolls_amount", types.DoubleType(), True),
        types.StructField("ehail_fee", types.DoubleType(), True),
        types.StructField("improvement_surcharge", types.DoubleType(), True),
        types.StructField("total_amount", types.DoubleType(), True),
        types.StructField("payment_type", types.IntegerType(), True),
        types.StructField("trip_type", types.IntegerType(), True),
        types.StructField("congestion_surcharge", types.DoubleType(), True),
    ])

    yellow_schema = types.StructType([
        types.StructField("VendorID", types.IntegerType(), True),
        types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
        types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
        types.StructField("passenger_count", types.IntegerType(), True),
        types.StructField("trip_distance", types.DoubleType(), True),
        types.StructField("RatecodeID", types.IntegerType(), True),
        types.StructField("store_and_fwd_flag", types.StringType(), True),
        types.StructField("PULocationID", types.IntegerType(), True),
        types.StructField("DOLocationID", types.IntegerType(), True),
        types.StructField("payment_type", types.IntegerType(), True),
        types.StructField("fare_amount", types.DoubleType(), True),
        types.StructField("extra", types.DoubleType(), True),
        types.StructField("mta_tax", types.DoubleType(), True),
        types.StructField("tip_amount", types.DoubleType(), True),
        types.StructField("tolls_amount", types.DoubleType(), True),
        types.StructField("improvement_surcharge", types.DoubleType(), True),
        types.StructField("total_amount", types.DoubleType(), True),
        types.StructField("congestion_surcharge", types.DoubleType(), True),
    ])

    builder = SparkSession.builder \
        .master("local[*]") \
        .appName("raw_to_parquet") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.default.parallelism", "8")

    if hadoop_home:
        builder = builder \
            .config("spark.driver.extraJavaOptions", f"-Dhadoop.home.dir={hadoop_home}") \
            .config("spark.hadoop.hadoop.home.dir", hadoop_home)

    spark = builder.getOrCreate()

    df_green = spark.read \
        .option("header", "true") \
        .schema(green_schema) \
        .csv("data/raw/green/2021/01/*.csv.gz")

    df_green.repartition(8).write.mode("overwrite").parquet("data/pq/green/2021/01")
    print("Green 변환 완료: data/pq/green/2021/01/")

    df_yellow = spark.read \
        .option("header", "true") \
        .schema(yellow_schema) \
        .csv("data/raw/yellow/2021/01/*.csv.gz")

    df_yellow.repartition(8).write.mode("overwrite").parquet("data/pq/yellow/2021/01")
    print("Yellow 변환 완료: data/pq/yellow/2021/01/")

    spark.stop()
    print("완료 (Spark).")

# ========== 실행 ==========
if __name__ == "__main__":
    if USE_PANDAS:
        run_pandas()
    else:
        run_spark()
