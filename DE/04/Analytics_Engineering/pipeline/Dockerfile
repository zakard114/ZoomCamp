# # 슬림 Python 3.13 이미지 사용
# FROM python:3.13.11-slim

# # 작업 디렉토리
# WORKDIR /code

# # 의존성 설치
# RUN pip install pandas sqlalchemy psycopg2-binary tqdm click

# # 데이터 적재 스크립트 복사
# COPY ingest_data.py ingest_data.py

# # 컨테이너 실행 시 ingest_data.py 실행
# ENTRYPOINT ["python", "ingest_data.py"]



# 슬림 Python 3.13 이미지 사용
FROM python:3.13.11-slim

# uv 바이너리 복사 (의존성 설치용)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# 작업 디렉토리
WORKDIR /code

# 가상환경 PATH에 추가
ENV PATH="/code/.venv/bin:$PATH"

# 의존성 파일 먼저 복사 (캐시 활용)
COPY pyproject.toml uv.lock .python-version ./

# 의존성 설치
RUN uv sync --locked

# 데이터 적재 스크립트 복사
COPY ingest_data.py .

# 컨테이너 실행 시 ingest_data.py 실행
ENTRYPOINT ["python", "ingest_data.py"]
