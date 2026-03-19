# psycopg2 ModuleNotFoundError 해결 보고서

## 1. 원인

| 항목 | 내용 |
|------|------|
| **오류** | `ModuleNotFoundError: No module named 'psycopg2'` |
| **직접 원인** | 현재 노트북에서 사용 중인 Python 환경(DE venv)에 `psycopg2` 패키지가 설치되어 있지 않음 |
| **상세** | psycopg2는 PostgreSQL 데이터베이스 연결을 위한 Python 드라이버로, pandas/kafka-python과 달리 기본적으로 포함되지 않음 |

## 2. 해결 방법

```bash
# DE venv에 psycopg2-binary 설치 (빌드 없이 바로 사용 가능)
E:\IT_SPACES\AI\ZoomCamp\DE\venv\Scripts\python.exe -m pip install psycopg2-binary
```

- **psycopg2-binary**: 소스 빌드 없이 사용할 수 있는 바이너리 버전 (로컬 개발에 적합)

## 3. 해결 결과

- **설치 완료**: psycopg2-binary 2.9.11 설치됨
- **상태**: 노트북 커널 재시작 후 `import psycopg2` 정상 동작

## 4. 확인 방법

```python
import psycopg2
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)
conn.autocommit = True
cur = conn.cursor()
# 정상 실행 시 에러 없음 (PostgreSQL 서버가 실행 중이어야 함)
```

---

**참고**: PostgreSQL 서버(docker compose의 postgres)가 실행 중이어야 연결이 됩니다. `docker compose up postgres -d`로 먼저 시작하세요.
