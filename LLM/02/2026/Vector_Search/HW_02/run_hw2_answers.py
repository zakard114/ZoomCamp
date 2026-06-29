"""Compute all HW2 answers for submission write-up."""
import sys
from pathlib import Path

import numpy as np
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch

HW_DIR = Path(__file__).resolve().parent
EMBED_DIR = (HW_DIR / ".." / "embed").resolve()
MODEL_DIR = EMBED_DIR / "models" / "Xenova" / "all-MiniLM-L6-v2"
sys.path.insert(0, str(EMBED_DIR))

from embedder import Embedder  # noqa: E402

model = Embedder(path=MODEL_DIR)

# Q1
query = "How does approximate nearest neighbor search work?"
v = model.encode(query)
print("Q1 v[0]:", round(float(v[0]), 2))

# Load data
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [f.parse() for f in reader.read()]

# Q2 official
target = next(d for d in documents if d["filename"] == "02-vector-search/lessons/07-sqlitesearch-vector.md")
v_doc = model.encode(target["content"])
q2 = float(np.dot(v, v_doc))
print("Q2 cosine:", round(q2, 2))

# Q3
chunks = chunk_documents(documents, size=2000, step=1000)
contents = [c["content"] for c in chunks]
parts = [model.encode_batch(contents[i : i + 50]) for i in range(0, len(contents), 50)]
X = np.vstack(parts)
scores = X.dot(v)
idx = int(np.argmax(scores))
print("Q3 file:", chunks[idx]["filename"], "score:", round(float(scores[idx]), 4))

# Q4
ms_vector = VectorSearch(keyword_fields=["filename"])
ms_vector.fit(X, chunks)
q4_query = "What metric do we use to evaluate a search engine?"
v_q4 = model.encode(q4_query)
r4 = ms_vector.search(v_q4, num_results=1)[0]
print("Q4 file:", r4["filename"])

# Q5
ms_text = Index(text_fields=["content"], keyword_fields=["filename"])
ms_text.fit(chunks)
q5_query = "How do I store vectors in PostgreSQL?"
text_results = ms_text.search(query=q5_query, num_results=5)
vector_results = ms_vector.search(model.encode(q5_query), num_results=5)
text_files = {d["filename"] for d in text_results}
vector_files = {d["filename"] for d in vector_results}
print("Q5 vector only:", vector_files - text_files)

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
print("Q6 file:", fused[0]["filename"])
