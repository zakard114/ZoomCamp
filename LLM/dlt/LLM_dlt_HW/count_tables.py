import duckdb

con = duckdb.connect("logfire_agent_traces.duckdb", read_only=True)
n = con.execute(
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'agent_traces'"
).fetchone()[0]
print(n)
con.close()
