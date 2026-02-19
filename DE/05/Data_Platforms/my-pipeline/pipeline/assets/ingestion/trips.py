"""@bruin
name: ingestion.trips
type: python
connection: gcp-default
image: python:3.11

materialization:
  type: table
  strategy: append

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


def materialize():
    """
    NYC TLC trip-data Parquet을 BRUIN_START_DATE ~ BRUIN_END_DATE,
    taxi_types에 맞춰 다운로드해 ingestion.trips에 append합니다.
    """
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
            except Exception as e:
                # 해당 월 파일이 없거나 오류 시 스킵 (미래 월 등)
                continue

    if not frames:
        return pd.DataFrame(columns=["vendor_id", "pickup_datetime", "trip_distance", "payment_type", "taxi_type", "extracted_at"])

    final = pd.concat(frames, ignore_index=True)
    return final
