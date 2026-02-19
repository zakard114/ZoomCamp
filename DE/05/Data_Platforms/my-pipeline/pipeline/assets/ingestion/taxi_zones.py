"""@bruin
name: ingestion.taxi_zones
type: python
connection: gcp-default
image: python:3.11

materialization:
  type: table
  strategy: create+replace
@bruin"""

from __future__ import annotations

import io
from datetime import datetime, timezone

import pandas as pd
import requests

# NYC TLC 공식 택시 존 룩업 테이블 (실제 서비스되는 URL)
TLC_TAXI_ZONES_CSV = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"


def ingest() -> pd.DataFrame:
    """
    NYC TLC 공식 taxi zone lookup CSV를 가져와 DataFrame으로 반환합니다.
    (api.city-data.com은 존재하지 않는 예시 URL이므로 TLC 공식 소스로 대체)
    """
    resp = requests.get(TLC_TAXI_ZONES_CSV, timeout=60)
    resp.raise_for_status()

    df = pd.read_csv(io.BytesIO(resp.content), encoding="utf-8")
    df["extracted_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return df


def materialize() -> pd.DataFrame:
    return ingest()
