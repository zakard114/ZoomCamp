# spark_with_winutils.py
"""
한 셀에 모두 넣어서 실행. HADOOP_HOME → Spark → read 순서 보장.
노트북에서 이 파일 내용을 복사해 한 셀에 붙여넣고 실행하세요.
"""
import os

# 1. 반드시 Spark import 전에!
HADOOP_DIR = r"E:\IT_SPACES\AI\ZoomCamp\DE\06\tools\hadoop-3.3.5"
os.environ["HADOOP_HOME"] = HADOOP_DIR
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.join(HADOOP_DIR, "bin")

# 2. 이제 Spark
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

# 3. 읽기
df_green = spark.read.option("header", "true").csv("data/raw/green/2021/01/")
df_green.show(5)
