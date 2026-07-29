import duckdb
conn = duckdb.connect("taxi_pipeline.duckdb", read_only=True)
# 컬럼명은 tip_amt (API: Tip_Amt -> dlt snake_case: tip_amt)
n = conn.execute("SELECT COUNT(*) FROM ny_taxi_data.trips").fetchone()[0]
total_tips = conn.execute("SELECT SUM(tip_amt) FROM ny_taxi_data.trips").fetchone()[0]
print("Rows in ny_taxi_data.trips:", n)
print("SUM(tip_amt) =", total_tips)
conn.close()
