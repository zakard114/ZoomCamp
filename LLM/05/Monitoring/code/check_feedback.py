# db_init.py에서 만들었던 데이터베이스 연결 함수를 그대로 가져옵니다.
from db_init import get_db_connection

def check_data():
    # 데이터베이스에 접속합니다.
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 피드백 테이블에 데이터가 들어있는지 조회하는 쿼리를 실행합니다.
            cur.execute("SELECT id, conversation_id, source, score, timestamp FROM feedback;")
            # 조회된 모든 결과 행을 가져옵니다.
            rows = cur.fetchall()
            
            if not rows:
                print("피드백 테이블이 비어 있습니다. 웹 UI에서 버튼을 눌러보세요!")
                return
                
            print("=== 피드백 데이터베이스 적재 결과 ===")
            for row in rows:
                # 메모장이나 일반 터미널에서도 깨짐 없이 한 줄씩 정돈되어 출력되도록 구현합니다.
                print(f"피드백 번호: {row[0]} | 대화 ID: {row[1]} | 출처: {row[2]} | 점수: {row[3]} | 등록시각: {row[4]}")
    finally:
        # 데이터베이스 연결을 안전하게 닫아줍니다.
        conn.close()

if __name__ == "__main__":
    check_data()