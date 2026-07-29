"""DuckDB에 로드된 authors 테이블 상위 5건 조회."""
import duckdb

DB_PATH = "open_library_pipeline.duckdb"
QUERY = """
SELECT * FROM open_library_data.authors
LIMIT 5;
"""

def main():
    conn = duckdb.connect(DB_PATH, read_only=True)
    result = conn.execute(QUERY)
    rows = result.fetchall()
    columns = [d[0] for d in result.description]
    # 컬럼명 출력
    print("\t".join(columns))
    print("-" * 80)
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    main()
