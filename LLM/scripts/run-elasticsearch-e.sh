#!/usr/bin/env bash
# Elasticsearch (데이터 E:). 내부적으로 docker compose 사용.
# Git Bash: bash scripts/run-elasticsearch-e.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

docker compose -f "${ROOT_DIR}/docker-compose.elasticsearch.yml" up -d
echo "Host data: E:/IT_SPACES/AI/ZoomCamp/docker-data/volumes/elasticsearch-data (see LLM/docker-compose.elasticsearch.yml)"
