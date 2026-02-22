"""Q1~Q3: 데이터셋 기간, 신용카드 비율, 팁 총액."""
import duckdb

conn = duckdb.connect("taxi_pipeline.duckdb", read_only=True)

# 컬럼명 확인 (dlt는 snake_case)
cols = conn.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'ny_taxi_data' AND table_name = 'trips'
    ORDER BY ordinal_position
""").fetchall()
col_names = [c[0] for c in cols]
print("Columns:", col_names)

# 픽업 날짜 컬럼 (Trip_Pickup_DateTime -> trip_pickup_date_time)
pickup_col = next((c for c in col_names if "pickup" in c.lower() and "date" in c.lower()), None)
payment_col = next((c for c in col_names if "payment" in c.lower()), None)
tip_col = next((c for c in col_names if "tip" in c.lower()), None)

print()
# Q1: start/end date
if pickup_col:
    r = conn.execute(f'SELECT MIN("{pickup_col}") AS min_dt, MAX("{pickup_col}") AS max_dt FROM ny_taxi_data.trips').fetchone()
    print("Q1 - Start date / End date:", r[0], "~", r[1])

# Q2: proportion paid with credit card
if payment_col:
    r = conn.execute(f'''
        SELECT COUNT(*) FILTER (WHERE "{payment_col}" = 'Credit') AS credit_count,
               COUNT(*) AS total
        FROM ny_taxi_data.trips
    ''').fetchone()
    pct = (r[0] / r[1] * 100) if r[1] else 0
    print("Q2 - Credit card trips:", r[0], "/", r[1], "=", round(pct, 2), "%")

# Q3: total tips
if tip_col:
    r = conn.execute(f'SELECT SUM("{tip_col}") FROM ny_taxi_data.trips').fetchone()
    print("Q3 - Total tips ($):", r[0])

conn.close()
