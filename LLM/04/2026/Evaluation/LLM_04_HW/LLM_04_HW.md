# LLM Zoomcamp 2026 — Homework 4: Evaluation

Submission write-up for **Homework 4: Evaluation**. Full runnable notebook: `LLM_04_HW.ipynb` (same folder as this file).

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/04-evaluation/homework.md)  
**Submit:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4

**Homework URL (for form):**  
`https://github.com/zakard114/ZoomCamp/blob/main/LLM/04/2026/Evaluation/LLM_04_HW/LLM_04_HW.md`

---

## Homework form answers

| # | Form choice |
|---|-------------|
| 1 | **1400** |
| 2 | **01-agentic-rag/lessons/03-rag.md** |
| 3 | **01-agentic-rag/lessons/01-intro.md** |
| 4 | **0.76** |
| 5 | **0.55** |
| 6 | **1** |

---

## Setup (local — continues from HW2)

Official homework continues HW2: same lesson pages at commit `8c1834d` (72 pages), same chunks (`size=2000`, `step=1000` → 295 chunks), same `Embedder` from Module 2.

For Q1, ground-truth question generation uses **Cerebras** (`gemma-4-31b`) via `evaluation_utils.py` (`EVAL_LLM_BACKEND=cerebras` in `LLM/.env`).

```python
import sys
from pathlib import Path

EVAL_CODE = (Path.cwd().parent / "code").resolve()
sys.path.insert(0, str(EVAL_CODE))

from gitsource import GithubRepositoryDataReader
from evaluation_utils import (
    GEMMA_DATA_GEN_INSTRUCTIONS,
    Questions,
    get_default_model,
    get_openai_client,
    get_prompt_tokens,
    llm_structured,
)

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]

client = get_openai_client(local=True)
model = get_default_model(client, local=True)
```

**Output:**

```text
backend=https://api.cerebras.ai/v1/ model=gemma-4-31b docs=72
```

---

## Q1 — Average input tokens (3 lesson pages)

Target pages:

- `01-agentic-rag/lessons/01-intro.md`
- `01-agentic-rag/lessons/02-environment.md`
- `01-agentic-rag/lessons/03-rag.md`

```python
target_files = [
    "01-agentic-rag/lessons/01-intro.md",
    "01-agentic-rag/lessons/02-environment.md",
    "01-agentic-rag/lessons/03-rag.md",
]
input_tokens_list = []

for doc in documents:
    if doc["filename"] not in target_files:
        continue
    user_prompt = (
        f"Filename: {doc['filename']}\n"
        f"Content: {doc['content']}\n\n"
        f"{GEMMA_DATA_GEN_INSTRUCTIONS}"
    )
    _, usage = llm_structured(
        client, GEMMA_DATA_GEN_INSTRUCTIONS, user_prompt, Questions, model=model
    )
    input_tokens_list.append(get_prompt_tokens(usage))

average_tokens = sum(input_tokens_list) / len(input_tokens_list)
```

**Output:**

```text
input tokens per file: [1110, 1352, 1812]
Q1 average input tokens: 1424.6666666666667
```

**Answer:** **1400** (nearest form option)

---

## Ground truth + search setup

Download official ground truth (360 questions, `question` + `filename`):

```bash
wget https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/cohorts/2026/04-evaluation/ground-truth.csv
```

```python
import pandas as pd
from gitsource import chunk_documents
from minsearch import Index, VectorSearch
import numpy as np

df_ground_truth = pd.read_csv("data/ground-truth.csv")
ground_truth = df_ground_truth.to_dict(orient="records")

chunks = chunk_documents(documents, size=2000, step=1000)

ms_text = Index(text_fields=["content"], keyword_fields=["filename"])
ms_text.fit(chunks)

def text_search(query, num_results=5):
    return ms_text.search(query=query, num_results=num_results)
```

**Output:**

```text
ground_truth=360 chunks=295
```

Vector index (HW2 embedder):

```python
EMBED_DIR = Path(r"E:/IT_SPACES/AI/ZoomCamp/LLM/02/2026/Vector_Search/embed")
sys.path.insert(0, str(EMBED_DIR))
from embedder import Embedder

embed_model = Embedder(path=EMBED_DIR / "models/Xenova/all-MiniLM-L6-v2")
chunk_contents = [c["content"] for c in chunks]
X = np.vstack([
    embed_model.encode_batch(chunk_contents[i : i + 50])
    for i in range(0, len(chunk_contents), 50)
])

ms_vector = VectorSearch(keyword_fields=["filename"])
ms_vector.fit(X, chunks)

def vector_search(query, num_results=5):
    return ms_vector.search(embed_model.encode(query), num_results=num_results)
```

---

## Q2 — First result with text search

```python
query = ground_truth[0]["question"]
search_results = text_search(query)
first_result_filename = search_results[0]["filename"]
```

**Output:**

```text
First result filename: 01-agentic-rag/lessons/03-rag.md
```

**Answer:** **01-agentic-rag/lessons/03-rag.md**

(Ground-truth label for this question: `01-agentic-rag/lessons/01-intro.md` — text search ranks a different page first.)

---

## Q3 — First result with vector search

```python
vector_results = vector_search(query)
vector_result_filename = vector_results[0]["filename"]
```

**Output:**

```text
Vector search result filename: 01-agentic-rag/lessons/01-intro.md
```

**Answer:** **01-agentic-rag/lessons/01-intro.md**

---

## Q4–Q6 — Evaluation metrics

Label = `filename` (not FAQ `document` id). A hit when a returned chunk's `filename` matches the question's `filename`.

```python
def compute_relevance(q, search_function):
    target = q["filename"]
    results = search_function(q["question"])
    return [int(d["filename"] == target) for d in results]

def hit_rate(relevance_total):
    return sum(any(r) for r in relevance_total) / len(relevance_total)

def mrr(relevance_total):
    total = 0.0
    for r in relevance_total:
        if not any(r):
            continue
        rank = next(i + 1 for i, v in enumerate(r) if v)
        total += 1 / rank
    return total / len(relevance_total)

def evaluate(ground_truth, search_function):
    relevance_total = [compute_relevance(q, search_function) for q in ground_truth]
    return {"hit_rate": hit_rate(relevance_total), "mrr": mrr(relevance_total)}

def rrf(result_lists, k=60, num_results=5):
    scores, docs = {}, {}
    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc
    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]

def hybrid_search(query, k=60):
    text_results = text_search(query, num_results=10)
    vector_results = vector_search(query, num_results=10)
    return rrf([text_results, vector_results], k=k)
```

### Q4 — text search Hit Rate

```python
evaluate(ground_truth, text_search)
```

**Output:**

```text
{'hit_rate': 0.7583333333333333, 'mrr': 0.5942592592592593}
```

**Answer:** **0.76**

### Q5 — vector search MRR

```python
evaluate(ground_truth, vector_search)
```

**Output:**

```text
{'hit_rate': 0.725, 'mrr': 0.5486111111111112}
```

**Answer:** **0.55**

### Q6 — hybrid search, best RRF `k`

```python
for k in [1, 50, 100, 200]:
  print(k, evaluate(ground_truth, lambda q, kk=k: hybrid_search(q, k=kk)))
```

**Output:**

```text
1   {'hit_rate': 0.8389, 'mrr': 0.6482}
50  {'hit_rate': 0.8361, 'mrr': 0.6379}
100 {'hit_rate': 0.8361, 'mrr': 0.6379}
200 {'hit_rate': 0.8361, 'mrr': 0.6379}
```

**Answer:** **1** (highest MRR; on tie pick smallest `k`)

---

## Environment

| Item | Notes |
|------|--------|
| Kernel | Python 3.12 (`LLM/.venv`) |
| LLM (Q1) | Cerebras `gemma-4-31b` via OpenAI-compatible API |
| Embedding | ONNX `Embedder` — `02/2026/Vector_Search/embed/` |
| Model | `Xenova/all-MiniLM-L6-v2` |
| Search | `minsearch` (`Index`, `VectorSearch`) |
| Data | `gitsource` at commit `8c1834d` |
| Ground truth | `data/ground-truth.csv` (360 rows) |

```bash
pip install openai pydantic python-dotenv pandas minsearch gitsource numpy onnxruntime tokenizers tqdm
```

---

## Submitting the form

| Field | What to enter |
|-------|----------------|
| **Homework URL** | GitHub link to this file or `LLM_04_HW.ipynb` (public repo) |
| **Learning in public** | Optional — use a **new post URL** per homework, not the same LinkedIn profile URL |

**Form:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4
