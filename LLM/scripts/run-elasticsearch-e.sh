#!/usr/bin/env bash
# Elasticsearch (데이터 E:). 내부적으로 docker compose 사용.
# Git Bash: bash scripts/run-elasticsearch-e.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

docker compose -f "${ROOT_DIR}/docker-compose.elasticsearch.yml" up -d
echo "데이터 디렉터리: E:/DockerVolumes/elasticsearch-data (compose volumes 참고)"
