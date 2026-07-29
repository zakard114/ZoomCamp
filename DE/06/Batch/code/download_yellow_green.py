# download_yellow_green.py
"""
Yellow & Green 택시 데이터 다운로드 (Windows용, wget 없이)
"""
import os
import sys
import urllib.request

# Spark 관련 환경 변수 (노트북 등에서 이 스크립트 import 후 Spark 사용 시)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

URL_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
YEAR = 2020  # 2020년 (05_taxi_schema.ipynb용)
MONTHS = list(range(1, 13))  # 1~12월 전체 (테스트용 1월만: [1])

for taxi_type in ["yellow", "green"]:
    for month in MONTHS:
        fmonth = f"{month:02d}"
        url = f"{URL_PREFIX}/{taxi_type}/{taxi_type}_tripdata_{YEAR}-{fmonth}.csv.gz"
        local_dir = os.path.join("data", "raw", taxi_type, str(YEAR), fmonth)
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, f"{taxi_type}_tripdata_{YEAR}_{fmonth}.csv.gz")
        print(f"다운로드 중: {url}")
        try:
            urllib.request.urlretrieve(url, local_path)
            size = os.path.getsize(local_path)
            print(f"  완료: {local_path} ({size/1024/1024:.1f} MB)")
        except Exception as e:
            print(f"  실패: {e}")

print("\n모든 다운로드 프로세스 종료.")
