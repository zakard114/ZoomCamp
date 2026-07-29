# 2025 cohort archive

| Path | Notes |
|------|-------|
| [`Introduction/`](Introduction/) | Course notebooks, `llm_01_hw` (Elasticsearch 8.17.6 homework) |
| [`docker-compose.elasticsearch.yml`](docker-compose.elasticsearch.yml) | **Course** Elasticsearch **8.4.3** (lecture stack) |
| [`requirements.txt`](requirements.txt) | Python deps for 2025 Introduction / ES notebooks |
| [`scripts/run-elasticsearch-e.sh`](scripts/run-elasticsearch-e.sh) | Start course ES with data on `docker-data/` |

Homework compose: `Introduction/llm_01_hw/docker-compose.yml` (ES **8.17.6**)  
Course ES data: `ZoomCamp/docker-data/volumes/elasticsearch-data`  
Homework ES data: `ZoomCamp/docker-data/volumes/elasticsearch-hw-data`

Do **not** run course and homework ES stacks together — both use port **9200**.

2026 workspace (Agentic RAG): [`../2026/`](../2026/)
