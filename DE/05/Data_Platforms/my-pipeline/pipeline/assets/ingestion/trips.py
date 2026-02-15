"""@bruin
name: ingestion.trips
type: python
connection: duckdb
image: python:3.11

materialization:
  type: table
  strategy: append

columns:
  - name: vendor_id
    type: integer
  - name: pickup_datetime
    type: timestamp
  - name: trip_distance
    type: float
  - name: payment_type
    type: integer
  - name: taxi_type
    type: string
  - name: extracted_at
    type: timestamp
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime

def materialize():
    """
    Bruin의 Python Materialization 기능을 사용하여 데이터를 생성하고 
    자동으로 DuckDB의 ingestion.trips 테이블에 데이터를 추가(append)합니다.
    """
    
    # 1. 실행 기간(Window) 환경 변수 로드
    # Bruin run 실행 시 전달되는 시작 날짜를 사용합니다.
    start_date = os.getenv("BRUIN_START_DATE", "2024-04-01")
    
    # 2. 파이프라인 변수(taxi_types) 로드
    # pipeline.yml에 정의된 taxi_types 변수를 읽어옵니다.
    bruin_vars = json.loads(os.getenv("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow", "green"])

    all_data = []

    # 3. 데이터 생성 비즈니스 로직
    for t_type in taxi_types:
        # 각 택시 타입별로 샘플 데이터 생성
        data = pd.DataFrame({
            'vendor_id': [1, 2],
            'pickup_datetime': [pd.to_datetime(start_date)] * 2,
            'trip_distance': [2.5, 3.8],
            'payment_type': [1, 2],
            'taxi_type': [t_type, t_type]
        })
        
        # 윈도우 환경에서 pyarrow 타임존 에러를 방지하기 위해 
        # 날짜 데이터를 안전하게 문자열로 변환합니다.
        data['pickup_datetime'] = data['pickup_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        all_data.append(data)

    # 생성된 데이터가 없을 경우 빈 데이터프레임 반환
    if not all_data:
        return pd.DataFrame()

    # 4. 최종 데이터 결합 및 추출 시간(lineage용) 추가
    final_df = pd.concat(all_data, ignore_index=True)
    final_df['extracted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Bruin에게 데이터프레임을 반환하면, Bruin이 이를 연결된 DuckDB 테이블에 적재합니다.
    return final_df