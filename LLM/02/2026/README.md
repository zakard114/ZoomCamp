# 2026 cohort — Vector Search homework

**2026 homework** uses a different stack from the 2025 Qdrant notebooks in [`../2025/`](../2025/):

- `uv` for dependencies
- ONNX Embedder (`Xenova/all-MiniLM-L6-v2`) — not sentence-transformers
- `gitsource` to load lesson markdown at commit `8c1834d`
- `minsearch` VectorSearch, keyword search, hybrid RRF

Official homework: https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/02-vector-search/homework.md  
Submit: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw2

## Setup (from homework)

```bash
mkdir llm-zoomcamp-hw2 && cd llm-zoomcamp-hw2
uv init --no-workspace
uv add onnxruntime tokenizers numpy tqdm minsearch gitsource
uv add --dev huggingface-hub jupyter
```

Download course helpers:

```bash
PREFIX=https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/02-vector-search/embed
wget $PREFIX/download.py
wget $PREFIX/embedder.py
uv run python download.py
```

Put your solution notebook under `HW_02/` in this folder when ready.
