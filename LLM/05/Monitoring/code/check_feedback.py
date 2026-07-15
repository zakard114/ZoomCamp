# Reuse the DB connection helper from db_init.py.
from db_init import get_db_connection


def check_data():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, conversation_id, source, score, timestamp FROM feedback;"
            )
            rows = cur.fetchall()

            if not rows:
                print("Feedback table is empty. Try the +/- buttons in the web UI.")
                return

            print("=== Feedback rows ===")
            for row in rows:
                print(
                    f"id: {row[0]} | conversation_id: {row[1]} | "
                    f"source: {row[2]} | score: {row[3]} | timestamp: {row[4]}"
                )
    finally:
        conn.close()


if __name__ == "__main__":
    check_data()
