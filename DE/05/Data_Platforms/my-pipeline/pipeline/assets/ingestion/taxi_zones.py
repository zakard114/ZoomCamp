"""@bruin
name: ingestion.taxi_zones
type: python
connection: gcp-default
image: python:3.11

requirements:
  - pandas>=2.0.0
  - requests>=2.28.0
  - pyarrow>=14.0.0
  - python-dateutil>=2.8.0
  - google-cloud-bigquery>=3.0.0
@bruin"""

from __future__ import annotations

import io
import os
from datetime import datetime, timezone

import pandas as pd
import requests

# Bruin Cloud / ingestr 목적지 강제 (참고용)
os.environ.setdefault("DESTINATION__BIGQUERY__PROJECT_ID", "bruin-de-zoomcamp")
os.environ.setdefault("DESTINATION__BIGQUERY__DATASET_NAME", "ingestion")

BQ_PROJECT_ID = os.environ.get("BRUIN_GCP_PROJECT_ID", "bruin-de-zoomcamp")
BQ_DATASET_NAME = "ingestion"
BQ_TABLE_TAXI_ZONES = "taxi_zones"

# 택시 존 룩업 CSV (CloudFront는 Bruin Cloud에서 403 → GitHub raw 사용, TLC와 동일 스키마)
TAXI_ZONES_CSV_URL = "https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/master/uber-trip-data/taxi-zone-lookup.csv"


def ingest() -> pd.DataFrame:
    """
    NYC 택시 존 룩업 CSV를 가져와 DataFrame으로 반환합니다.
    (FiveThirtyEight mirror 사용, CloudFront 403 회피)
    """
    resp = requests.get(TAXI_ZONES_CSV_URL, timeout=60)
    resp.raise_for_status()

    df = pd.read_csv(io.BytesIO(resp.content), encoding="utf-8")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["extracted_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return df


def materialize() -> pd.DataFrame:
    df = ingest()
    # 프로젝트 ID/데이터셋 명시 후 BigQuery에 직접 적재 (ingestr 404 방지)
    from google.cloud import bigquery
    from google.cloud.bigquery import WriteDisposition

    client = bigquery.Client(project=BQ_PROJECT_ID)
    table_id = f"{BQ_PROJECT_ID}.{BQ_DATASET_NAME}.{BQ_TABLE_TAXI_ZONES}"
    job_config = bigquery.LoadJobConfig(write_disposition=WriteDisposition.WRITE_TRUNCATE)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    return df
