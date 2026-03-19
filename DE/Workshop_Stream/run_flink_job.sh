#!/usr/bin/env bash
# flink_job.py 실행 (Dockerfile.pyflink 빌드 이미지, python3 직접 실행)
# 사전: docker compose build flink-driver, processed_trips 테이블, producer.py
set -e
cd "$(dirname "$0")"

docker compose run --rm flink-driver
