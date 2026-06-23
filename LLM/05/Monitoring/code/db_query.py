from dataclasses import dataclass

from db_init import get_db_connection
from metrics import LLMCallRecord


@dataclass
class Stats:
    total: int
    avg_response_time: float
    total_cost: float
    avg_tokens: float


def row_to_record(row):
    return LLMCallRecord(
        model=row[4],
        prompt=row[6],
        instructions=row[5],
        answer=row[2],
        prompt_tokens=row[7],
        completion_tokens=row[8],
        total_tokens=row[9],
        response_time=row[10],
        cost=row[11],
        timestamp=row[12],
    )

def get_conversations(limit=10):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, question, answer, course, model,
                       instructions, prompt,
                       prompt_tokens, completion_tokens, total_tokens,
                       response_time, cost, timestamp
                FROM conversations
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return [row_to_record(row) for row in rows]


def get_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*),
                    AVG(response_time),
                    SUM(cost),
                    AVG(total_tokens)
                FROM conversations
            """)
            row = cur.fetchone()
    finally:
        conn.close()

    return Stats(
        total=row[0],
        avg_response_time=row[1],
        total_cost=row[2],
        avg_tokens=row[3],
    )


def get_relevance_stats():
    """AI 판단기가 매긴 관련성 등급별(RELEVANT, PARTLY_RELEVANT 등) 누적 빈도수를 딕셔너리 형태로 가져옵니다."""
    # 데이터베이스와 안전하게 연결을 소통할 커넥션 객체를 생성합니다.
    conn = get_db_connection()
    try:
        # SQL 문정을 실행하기 위해 데이터베이스 커서(Cursor)를 엽니다.
        with conn.cursor() as cur:
            # feedback 테이블에서 출처가 'judge'인 행들만 필터링하여 등급별로 그룹화한 뒤 개수를 세어주는 SQL을 실행합니다.
            cur.execute("""
                SELECT relevance, COUNT(*)
                FROM feedback
                WHERE source = 'judge'
                GROUP BY relevance
            """)
            # 쿼리 실행 결과로 나온 모든 행(Row) 데이터를 튜플 리스트 형태로 긁어옵니다.
            rows = cur.fetchall()
    finally:
        # 데이터베이스 자원 누수를 막기 위해 사용이 끝난 커넥션을 안전하게 닫아줍니다.
        conn.close()
    
    # 결과로 반환된 [('RELEVANT', 5), ('NON_RELEVANT', 1)] 형태의 리스트를 {'RELEVANT': 5, 'NON_RELEVANT': 1} 형태의 딕셔너리로 변환하여 리턴합니다.
    return dict(rows)


def get_user_feedback_stats():
    """실제 유저들이 누른 좋아요(Thumbs up)와 싫어요(Thumbs down)의 총 합산 개수를 계산하여 반환합니다."""
    # 데이터베이스와 안전하게 연결을 소통할 커넥션 객체를 생성합니다.
    conn = get_db_connection()
    try:
        # SQL 문정을 실행하기 위해 데이터베이스 커서(Cursor)를 엽니다.
        with conn.cursor() as cur:
            # feedback 테이블에서 출처가 'user'인 행들을 대상으로, 점수가 0보다 크면 좋아요로, 0보다 작으면 싫어요로 판별해 각각 SUM(합산)합니다.
            cur.execute("""
                SELECT
                    SUM(CASE WHEN score > 0 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN score < 0 THEN 1 ELSE 0 END)
                FROM feedback
                WHERE source = 'user'
            """)
            # 단 한 줄로 축약되어 나오는 통계 집계 결과 행을 안전하게 가져옵니다.
            row = cur.fetchone()
    finally:
        # 데이터베이스 자원 누수를 막기 위해 사용이 끝난 커넥션을 안전하게 닫아줍니다.
        conn.close()
    
    # 계산된 (좋아요 총합, 싫어요 총합) 형태의 튜플 데이터를 최종 리턴합니다.
    return row


if __name__ == "__main__":
    records = get_conversations()
    for record in records:
        print(record)


