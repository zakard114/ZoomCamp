import dataclasses
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaProducer
from models import Ride, ride_from_row

# NYC 택시 Zone ID (1-263)
PICKUP_LOCATIONS = [79, 107, 48, 132, 234, 148, 249, 68, 90, 263, 138, 230, 161, 162, 170, 237, 239, 186, 164, 236]
DROPOFF_LOCATIONS = PICKUP_LOCATIONS


def _load_from_parquet():
    """Parquet URL에서 1000행 로드 (메모리 충분 시)"""
    import pandas as pd
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
    columns = ['PULocationID', 'DOLocationID', 'trip_distance', 'total_amount', 'tpep_pickup_datetime']
    df = pd.read_parquet(url, columns=columns).head(1000)
    return [ride_from_row(row) for _, row in df.iterrows()]


def _generate_synthetic(num=1000):
    """메모리 부족 시 대체: 합성 Ride 1000건 생성"""
    import pandas as pd
    base_ts = pd.Timestamp('2025-11-01', tz='UTC')
    rides = []
    for i in range(num):
        ts = base_ts + pd.Timedelta(minutes=i)
        rides.append(Ride(
            PULocationID=random.choice(PICKUP_LOCATIONS),
            DOLocationID=random.choice(DROPOFF_LOCATIONS),
            trip_distance=round(random.uniform(0.5, 20.0), 2),
            total_amount=round(random.uniform(5.0, 100.0), 2),
            tpep_pickup_datetime=int(ts.timestamp() * 1000),
        ))
    return rides


try:
    rides = _load_from_parquet()
    print("(실제 NYC 택시 Parquet 데이터 사용)")
except Exception as e:
    print(f"(Parquet 로드 실패: {e})\n합성 데이터로 대체합니다.")
    rides = _generate_synthetic()

def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=ride_serializer
)
t0 = time.time()

topic_name = 'rides'

for ride in rides:
    producer.send(topic_name, value=ride)
    print(f"Sent: {ride}")
    time.sleep(0.01)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
