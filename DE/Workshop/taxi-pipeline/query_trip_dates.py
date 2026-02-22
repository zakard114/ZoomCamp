"""
ny_taxi_data.trips 에서 픽업 datetime 의 MIN/MAX 조회.
컬럼명이 tpep_pickup_datetime 이거나 trip_pickup_date_time 일 수 있음.
"""
import duckdb
conn = duckdb.connect("taxi_pipeline.duckdb", read_only=True)

# 픽업 날짜 컬럼 찾기 (dlt는 보통 snake_case로 저장)
cols = conn.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'ny_taxi_data' AND table_name = 'trips'
    AND (column_name LIKE '%pickup%' OR column_name LIKE '%Pickup%')
""").fetchall()

if not cols:
    print("ny_taxi_data.trips 테이블 또는 pickup 컬럼이 없습니다. 파이프라인 로드가 완료되었는지 확인하세요.")
    conn.close()
    exit(1)

col = cols[0][0]
q = f'SELECT MIN("{col}") AS min_dt, MAX("{col}") AS max_dt FROM ny_taxi_data.trips'
row = conn.execute(q).fetchone()
print(f"컬럼: {col}")
print(f"MIN (시작): {row[0]}")
print(f"MAX (종료): {row[1]}")
conn.close()
