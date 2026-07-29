import io
import os
import requests
import pandas as pd
from google.cloud import storage

# 서비스 URL 설정
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "kestra-zoomcamp-zakard-demo")

# ⭐ 핵심: FAQ에서 권장하는 대로 모든 달의 타입을 강제로 통일합니다.
# 특히 문제가 된 passenger_count를 float64로 잡는 것이 포인트입니다.
TABLE_SCHEMA = {
    "VendorID": "Int64",
    "lpep_pickup_datetime": "datetime64[ns]",
    "lpep_dropoff_datetime": "datetime64[ns]",
    "store_and_fwd_flag": "object",
    "RatecodeID": "float64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "float64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "ehail_fee": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "float64",
    "trip_type": "float64",
    "congestion_surcharge": "float64"
}

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service):
    for i in range(12):
        month = '0'+str(i+1)
        month = month[-2:]

        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        
        if r.status_code != 200:
            print(f"❌ Skip: {file_name}")
            continue
            
        open(file_name, 'wb').write(r.content)
        print(f"Downloaded: {file_name}")

        # ⭐ 핵심 수정: 데이터를 읽을 때 타입을 강제 지정합니다.
        # low_memory=False와 함께 스키마를 적용하여 타입 불일치를 원천 차단합니다.
        df = pd.read_csv(file_name, compression='gzip', low_memory=False)
        
        # 실제 존재하는 컬럼만 스키마 적용 (안전장치)
        existing_schema = {k: v for k, v in TABLE_SCHEMA.items() if k in df.columns}
        df = df.astype(existing_schema)

        file_name_parquet = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name_parquet, engine='pyarrow')

        # GCS로 업로드 (이때 GCS는 비어있어야 함)
        upload_to_gcs(BUCKET, f"{service}/{file_name_parquet}", file_name_parquet)
        print(f"✅ GCS Upload Success: {service}/{file_name_parquet}")
        
        # 로컬 파일 정리 (용량 확보)
        os.remove(file_name)
        os.remove(file_name_parquet)

if __name__ == "__main__":
    web_to_gcs('2019', 'green')
    web_to_gcs('2020', 'green')