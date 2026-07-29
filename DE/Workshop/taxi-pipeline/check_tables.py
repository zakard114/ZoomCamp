import duckdb
import os
p = "taxi_pipeline.duckdb"
print("DB exists:", os.path.isfile(p))
if not os.path.isfile(p):
    exit(0)
conn = duckdb.connect(p, read_only=True)
t = conn.execute("SELECT table_schema, table_name FROM information_schema.tables").fetchall()
print("Tables:", t)
conn.close()
