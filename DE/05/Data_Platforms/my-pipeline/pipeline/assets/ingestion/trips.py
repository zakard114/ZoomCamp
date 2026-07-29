"""@bruin
name: ingestion.trips
type: python
connection: gcp-default
image: python:3.11

requirements:
  - pandas>=2.0.0
  - requests>=2.28.0
  - pyarrow>=14.0.0
  - python-dateutil>=2.8.0
  - google-cloud-bigquery>=3.0.0

columns:
  - name: vendor_id
    type: integer
  - name: pickup_datetime
    type: timestamp
    checks:
      - name: not_null
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
import io
from datetime import datetime

import pandas as pd
import requests

# Bruin Cloud / ingestr가 잘못된 프로젝트를 쓰지 않도록 목적지 강제 (참고용)
os.environ.setdefault("DESTINATION__BIGQUERY__PROJECT_ID", "bruin-de-zoomcamp")
os.environ.setdefault("DESTINATION__BIGQUERY__DATASET_NAME", "ingestion")

# BigQuery 목적지 고정 (404 방지)
BQ_PROJECT_ID = os.environ.get("BRUIN_GCP_PROJECT_ID", "bruin-de-zoomcamp")
BQ_DATASET_NAME = "ingestion"
BQ_TABLE_TRIPS = "trips"

TLC_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def _month_range(start_date: str, end_date: str):
    """Yield (year, month) tuples from start_date to end_date (inclusive)."""
    from dateutil.relativedelta import relativedelta

    start = datetime.strptime(start_date[:10], "%Y-%m-%d").date()
    end = datetime.strptime(end_date[:10], "%Y-%m-%d").date()
    current = start.replace(day=1)
    end_first = end.replace(day=1)
    while current <= end_first:
        yield current.year, current.month
        current += relativedelta(months=1)


def _col(df: pd.DataFrame, *candidates: str):
    """컬럼명 대소문자 무시하고 첫 번째 매칭 컬럼 반환."""
    lower = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name.lower() in lower:
            return df[lower[name.lower()]]
    return None


def _normalize_trips(df: pd.DataFrame, taxi_type: str) -> pd.DataFrame:
    """TLC Parquet 컬럼을 ingestion.trips 스키마로 맞춤."""
    pickup_col = "tpep_pickup_datetime" if taxi_type == "yellow" else "lpep_pickup_datetime"
    out = pd.DataFrame(index=df.index)
    v = _col(df, "VendorID", "vendorid")
    out["vendor_id"] = v if v is not None else 0
    p = _col(df, pickup_col, "tpep_pickup_datetime", "lpep_pickup_datetime")
    out["pickup_datetime"] = pd.to_datetime(p).dt.strftime("%Y-%m-%d %H:%M:%S") if p is not None else None
    td = _col(df, "trip_distance")
    out["trip_distance"] = td if td is not None else 0.0
    pt = _col(df, "payment_type")
    out["payment_type"] = pt if pt is not None else 0
    out["taxi_type"] = taxi_type
    out["extracted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return out


def _ensure_trips_table_exists(client):
    """Bruin Cloud가 ingestr로 올리기 전에 테이블이 있어야 하므로, 없으면 생성."""
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound

    table_ref = f"{BQ_PROJECT_ID}.{BQ_DATASET_NAME}.{BQ_TABLE_TRIPS}"
    try:
        client.get_table(table_ref)
        return
    except NotFound:
        pass
    schema = [
        bigquery.SchemaField("vendor_id", "INT64"),
        bigquery.SchemaField("pickup_datetime", "TIMESTAMP"),
        bigquery.SchemaField("trip_distance", "FLOAT64"),
        bigquery.SchemaField("payment_type", "INT64"),
        bigquery.SchemaField("taxi_type", "STRING"),
        bigquery.SchemaField("extracted_at", "TIMESTAMP"),
    ]
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table)


def materialize():
    """
    NYC TLC trip-data Parquet을 BRUIN_START_DATE ~ BRUIN_END_DATE,
    taxi_types에 맞춰 다운로드해 ingestion.trips에 append합니다.
    """
    from google.cloud import bigquery

    start_date = os.getenv("BRUIN_START_DATE", "2022-01-01")
    end_date = os.getenv("BRUIN_END_DATE", "2022-01-31")

    bruin_vars = json.loads(os.getenv("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow", "green"])

    frames = []
    for taxi_type in taxi_types:
        for year, month in _month_range(start_date, end_date):
            filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            url = f"{TLC_BASE}/{filename}"
            try:
                resp = requests.get(url, timeout=60)
                resp.raise_for_status()
                df = pd.read_parquet(io.BytesIO(resp.content))
                if df.empty:
                    continue
                out = _normalize_trips(df, taxi_type)
                frames.append(out)
            except Exception:
                continue

    client = bigquery.Client(project=BQ_PROJECT_ID)

    if not frames:
        # 데이터가 없어도 테이블이 있어야 Bruin Cloud ingestr 업로드 시 404 안 남
        _ensure_trips_table_exists(client)
        return pd.DataFrame(columns=["vendor_id", "pickup_datetime", "trip_distance", "payment_type", "taxi_type", "extracted_at"])

    final = pd.concat(frames, ignore_index=True)
    final = final.dropna(subset=["pickup_datetime"])

    # 테이블만 만들어 두고, 적재는 Bruin Cloud의 ingestr가 수행 (이중 적재 방지)
    _ensure_trips_table_exists(client)
    return final
