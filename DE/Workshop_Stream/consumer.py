from kafka import KafkaConsumer
import json

# 1. Consumer 설정
consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # 처음부터 읽기
    enable_auto_commit=False,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    consumer_timeout_ms=5000       # 5초 동안 데이터 안 들어오면 종료
)

count = 0
print("Reading from Redpanda and counting trips with distance > 5.0 km...")

# 2. Iterate messages and check condition
for message in consumer:
    if message.value['trip_distance'] > 5.0:
        count += 1

print("-" * 30)
print(f"Result: trips with trip_distance > 5.0 = {count}")
print("-" * 30)
