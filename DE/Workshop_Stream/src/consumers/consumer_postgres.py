import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from kafka import KafkaConsumer
from models import ride_deserializer

# 접속 정보 설정
server = 'localhost:9092' # 카프카(또는 Redpanda) 브로커 주소입니다.
topic_name = 'rides'      # 데이터를 읽어올 토픽 이름입니다.

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()

# PostgreSQL 저장을 위한 새로운 컨슈머를 생성합니다.
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',     # 토픽의 맨 처음 데이터부터 읽기 시작합니다.
    group_id='rides-to-postgres',     # ★중요: DB 저장용 전용 그룹 ID를 사용하여 별도로 위치를 관리합니다.
    value_deserializer=ride_deserializer # 바이트 데이터를 자동으로 Ride 객체로 변환합니다.
)

print(f"Listening to {topic_name} and writing to PostgreSQL...")

count = 0
for message in consumer:
    ride = message.value
    pickup_dt = datetime.fromtimestamp(ride.tpep_pickup_datetime / 1000)
    cur.execute(
        """INSERT INTO processed_events
           (PULocationID, DOLocationID, trip_distance, total_amount, pickup_datetime)
           VALUES (%s, %s, %s, %s, %s)""",
        (ride.PULocationID, ride.DOLocationID,
         ride.trip_distance, ride.total_amount, pickup_dt)
    )
    count += 1
    if count % 100 == 0:
        print(f"Inserted {count} rows...")

consumer.close()
cur.close()
conn.close()
