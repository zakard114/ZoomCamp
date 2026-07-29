#!/usr/bin/env bash
# 2025 cohort — course Elasticsearch (data on E:). Uses docker compose.
# Git Bash: bash scripts/run-elasticsearch-e.sh  (from LLM/01/2025)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

docker compose -f "${ROOT_DIR}/docker-compose.elasticsearch.yml" up -d
echo "Host data: <repo>/docker-data/volumes/elasticsearch-data (see LLM/01/2025/docker-compose.elasticsearch.yml)"
