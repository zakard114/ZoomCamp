import pyspark
from pyspark.sql import SparkSession

# Spark 세션 설정 및 생성
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

# Spark 버전 출력
print(f"Spark version: {spark.version}")

# 0부터 9까지의 숫자로 구성된 데이터프레임 생성 및 출력
df = spark.range(10)
df.show()

# 세션 종료
spark.stop()
