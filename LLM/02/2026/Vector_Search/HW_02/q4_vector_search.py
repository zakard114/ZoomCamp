"""HW2 Q4 — run if notebook cell still has wrong Gemini API (ndims)."""
import sys
from pathlib import Path

import numpy as np
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import VectorSearch

HW_DIR = Path(__file__).resolve().parent
EMBED_DIR = (HW_DIR / ".." / "embed").resolve()
MODEL_DIR = EMBED_DIR / "models" / "Xenova" / "all-MiniLM-L6-v2"
sys.path.insert(0, str(EMBED_DIR))

from embedder import Embedder  # noqa: E402

model = Embedder(path=MODEL_DIR)
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [f.parse() for f in reader.read()]
chunks = chunk_documents(documents, size=2000, step=1000)
contents = [c["content"] for c in chunks]
parts = [model.encode_batch(contents[i : i + 50]) for i in range(0, len(contents), 50)]
X = np.vstack(parts)

ms_vector = VectorSearch(keyword_fields=["filename"])
ms_vector.fit(X, chunks)

q4_query = "What metric do we use to evaluate a search engine?"
v_q4 = model.encode(q4_query)
result = ms_vector.search(v_q4, num_results=1)[0]
print(f"Top Result Filename: {result['filename']}")
