# LLM Zoomcamp 2026 — Homework 2: Vector Search

Submission write-up for **Homework 2: Vector Search**. Full runnable notebook: `vector_search_homework.ipynb` (same folder as this file).

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/02-vector-search/homework.md)  
**Submit:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw2

---

## Homework form answers

| # | Form choice |
|---|-------------|
| 1 | **-0.02** |
| 2 | **0.37** |
| 3 | **02-vector-search/lessons/07-sqlitesearch-vector.md** |
| 4 | **04-evaluation/lessons/05-search-metrics.md** |
| 5 | **02-vector-search/lessons/08-pgvector.md** |
| 6 | **01-agentic-rag/lessons/13-function-calling.md** |

---

## Setup (local — no separate `llm-zoomcamp-hw2` project)

Official homework suggests `uv init` + `wget embedder.py`. On this PC the Module 2 stack already lives on **E:** (`LLM/.venv`, `Vector_Search/embed/`). Run the notebook from `HW_02/` and import the sibling `embed/` folder.

```python
import sys
from pathlib import Path

import numpy as np

EMBED_DIR = (Path.cwd() / ".." / "embed").resolve()
MODEL_DIR = EMBED_DIR / "models" / "Xenova" / "all-MiniLM-L6-v2"
sys.path.insert(0, str(EMBED_DIR))

from embedder import Embedder

model = Embedder(path=MODEL_DIR)
```

---

## Q1 — Embedding a query

**Query:** `How does approximate nearest neighbor search work?`

```python
# Q1

query = "How does approximate nearest neighbor search work?"
v = model.encode(query)

print(f"Q1 shape: {v.shape}")
print(f"Q1 v[0]: {v[0]:.2f}")
```

**Output:**

```text
Q1 shape: (384,)
Q1 v[0]: -0.02
```

**Answer:** **-0.02**

---

## Loading the data

Same as homework 1 — lesson markdown at commit `8c1834d` (72 pages).

```python
from gitsource import GithubRepositoryDataReader

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]
print(f"documents: {len(documents)}")
```

**Output:**

```text
documents: 72
```

---

## Q2 — Cosine similarity

Embed the full `content` of `02-vector-search/lessons/07-sqlitesearch-vector.md` and dot with the Q1 vector (L2-normalized → cosine).

```python
# Q2

target = next(
    d for d in documents
    if d["filename"] == "02-vector-search/lessons/07-sqlitesearch-vector.md"
)
v_doc = model.encode(target["content"])
cosine_sim = float(np.dot(v, v_doc))
print(f"Q2 cosine similarity: {cosine_sim:.2f}")
```

**Output:**

```text
Q2 cosine similarity: 0.36
```

**Answer:** **0.37** (nearest form option)

---

## Q3 — Chunking and search by hand

Sliding window: `size=2000`, `step=1000` (1000-char overlap between consecutive chunks).

```python
# Q3
from gitsource import chunk_documents

chunks = chunk_documents(documents, size=2000, step=1000)
chunk_contents = [c["content"] for c in chunks]

parts = []
for i in range(0, len(chunk_contents), 50):
    parts.append(model.encode_batch(chunk_contents[i : i + 50]))
X = np.vstack(parts)

scores = X.dot(v)
idx = int(np.argmax(scores))
print(f"Q3 score: {scores[idx]:.4f}")
print(f"Q3 filename: {chunks[idx]['filename']}")
```

**Output:**

```text
Q3 score: 0.6489
Q3 filename: 02-vector-search/lessons/07-sqlitesearch-vector.md
```

**Answer:** **02-vector-search/lessons/07-sqlitesearch-vector.md**

---

## Q4 — Vector search with minsearch

```python
# Q4
from minsearch import VectorSearch

ms_vector = VectorSearch(keyword_fields=["filename"])
ms_vector.fit(X, chunks)

q4_query = "What metric do we use to evaluate a search engine?"
r4 = ms_vector.search(model.encode(q4_query), num_results=1)
print(f"Q4 filename: {r4[0]['filename']}")
```

**Output:**

```text
Q4 filename: 04-evaluation/lessons/05-search-metrics.md
```

**Answer:** **04-evaluation/lessons/05-search-metrics.md**

---

## Q5 — Text search vs vector search

**Query:** `How do I store vectors in PostgreSQL?`

```python
# Q5
from minsearch import Index

ms_text = Index(text_fields=["content"], keyword_fields=["filename"])
ms_text.fit(chunks)

q5_query = "How do I store vectors in PostgreSQL?"
text_results = ms_text.search(query=q5_query, num_results=5)
vector_results = ms_vector.search(model.encode(q5_query), num_results=5)

text_files = {d["filename"] for d in text_results}
vector_files = {d["filename"] for d in vector_results}
only_vector = vector_files - text_files

print(f"vector top5: {vector_files}")
print(f"text top5: {text_files}")
print(f"in vector not text: {only_vector}")
```

**Output:**

```text
vector top5: {'02-vector-search/lessons/08-pgvector.md', '03-orchestration/lessons/05-rag.md'}
text top5: {'02-vector-search/lessons/01-intro.md', '02-vector-search/lessons/02-embeddings.md', '03-orchestration/lessons/05-rag.md'}
in vector not text: {'02-vector-search/lessons/08-pgvector.md'}
```

**Answer:** **02-vector-search/lessons/08-pgvector.md**

---

## Q6 — Hybrid search (RRF)

**Query:** `How do I give the model access to tools?` (different from Q5)

RRF uses `(filename, start)` as the chunk key — one lesson file can produce many chunks.

```python
# Q6
q6_query = "How do I give the model access to tools?"

text_results = ms_text.search(query=q6_query, num_results=5)
vector_results = ms_vector.search(model.encode(q6_query), num_results=5)


def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}
    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc
    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]


fused = rrf([vector_results, text_results])
print(f"Q6 filename: {fused[0]['filename']}")
```

**Output:**

```text
Q6 filename: 01-agentic-rag/lessons/13-function-calling.md
```

**Answer:** **01-agentic-rag/lessons/13-function-calling.md**

---

## Environment

| Item | Notes |
|------|--------|
| Kernel | Python 3.12 (`LLM/.venv`) |
| Embedding | ONNX `Embedder` at `../embed/` — no PyTorch |
| Model | `Xenova/all-MiniLM-L6-v2` on E: (`embed/models/`) |
| Search | `minsearch` (`VectorSearch`, `Index`) |
| Data | `gitsource` at commit `8c1834d` |

```bash
pip install onnxruntime tokenizers numpy tqdm minsearch gitsource huggingface-hub
```
