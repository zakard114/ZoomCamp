import math
import pandas as pd
import json
from time import time
from kafka import KafkaProducer


def clean_nan_for_json(d):
    """JSON 직렬화 시 NaN/Inf → null 로 변환 (Flink JSON 파서 호환)"""
    out = {}
    for k, v in d.items():
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            out[k] = None
        else:
            out[k] = v
    return out


# 1. 데이터 로드 (data 폴더 안의 파일을 읽습니다)
print("Loading data...")
df = pd.read_parquet('data/green_tripdata_2025-10.parquet')

# 2. 숙제 지정 컬럼 8개만 필터링
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime',
    'PULocationID', 'DOLocationID', 'passenger_count',
    'trip_distance', 'tip_amount', 'total_amount'
]
df = df[columns]

# 3. Kafka Producer 설정 (Redpanda 연결)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 4. 데이터 전송 및 시간 측정
print("Sending data to Redpanda...")
t0 = time()

for row in df.itertuples(index=False):
    row_dict = row._asdict()
    
    # JSON 직렬화를 위해 datetime 객체를 문자열로 변환
    row_dict['lpep_pickup_datetime'] = str(row_dict['lpep_pickup_datetime'])
    row_dict['lpep_dropoff_datetime'] = str(row_dict['lpep_dropoff_datetime'])

    # NaN/Inf → null (Flink JSON 파서 호환)
    row_dict = clean_nan_for_json(row_dict)

    producer.send('green-trips', value=row_dict)

# 네트워크 버퍼의 모든 메시지 강제 전송
producer.flush()
t1 = time()

print(f'took {(t1 - t0):.2f} seconds')
