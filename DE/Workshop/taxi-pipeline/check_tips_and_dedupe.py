"""현재 데이터: 전체 SUM(tip_amt), 상위 2만 건 SUM, 보기와 비교."""
import duckdb

conn = duckdb.connect("taxi_pipeline.duckdb", read_only=True)

n = conn.execute("SELECT COUNT(*) FROM ny_taxi_data.trips").fetchone()[0]
print("현재 행 수:", n)

total_all = conn.execute("SELECT SUM(tip_amt) FROM ny_taxi_data.trips").fetchone()[0]
print("전체 SUM(tip_amt):", round(total_all, 2) if total_all else total_all)

# 중복 제거: 동일 trip 식별 후 2만 건만. (trip_pickup_date_time, start_lat, end_lat, fare_amt 등으로 유일 키)
# DuckDB: DISTINCT ON 없으면 ROW_NUMBER로 첫 행만 유지
try:
    sum_deduped_20k = conn.execute("""
        SELECT SUM(tip_amt) FROM (
            SELECT tip_amt FROM (
                SELECT tip_amt,
                    ROW_NUMBER() OVER (
                        PARTITION BY trip_pickup_date_time, start_lat, end_lat, fare_amt
                        ORDER BY _dlt_id
                    ) AS rn
                FROM ny_taxi_data.trips
            ) t
            WHERE rn = 1
            LIMIT 20000
        ) u
    """).fetchone()[0]
    print("중복 제거 후 20,000건 SUM(tip_amt):", round(sum_deduped_20k, 2) if sum_deduped_20k else sum_deduped_20k)
    val_to_compare = sum_deduped_20k
except Exception as e:
    print("중복 제거 2만 건 쿼리 실패:", e)
    # 상위 2만 건만 합산
    sum_20k = conn.execute(
        "SELECT SUM(tip_amt) FROM (SELECT tip_amt FROM ny_taxi_data.trips ORDER BY _dlt_id LIMIT 20000) t"
    ).fetchone()[0]
    print("상위 20,000건 SUM(tip_amt):", round(sum_20k, 2) if sum_20k else sum_20k)
    val_to_compare = sum_20k if n >= 20000 else total_all

# 비교할 값: 중복 제거 2만 건 합계 또는 전체(데이터가 2만 미만이면 전체)
compare_val = val_to_compare if n >= 20000 else total_all
if compare_val is None:
    compare_val = 0

options = [4063.41, 6063.41, 8063.41, 10063.41]
closest = min(options, key=lambda o: abs(o - compare_val))
diff = abs(closest - compare_val)
print()
print("비교 기준값:", round(compare_val, 2))
print("가장 가까운 보기: $", closest, "(차이: $", round(diff, 2), ")")
print("Q3 정답 추정: $" + str(closest))

conn.close()
