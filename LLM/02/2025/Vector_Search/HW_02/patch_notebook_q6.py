"""One-shot patch: replace client.search with query_points in vector_search_homework.ipynb."""
import json
from pathlib import Path

NOTEBOOK = Path(__file__).with_name("vector_search_homework.ipynb")
nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

OLD = """# search_results: Queries the vector DB engine and pulls matching entries based on spatial proximity.
search_results = client.search(
    # collection_name: Specifies the targeted "ml_zoomcamp_faq" collection space for scanning.
    collection_name=collection_name,
    # query_vector: Sets the target user query vector coordinate to measure distances against.
    query_vector=query_vector,
    # limit=1: Constraints the engine to return only the single most accurate matching document score.
    limit=1
)

# 7. Print the highest similarity score (Preserved)
# highest_score: Obtains the literal similarity metric coefficient (.score) of the topmost match from the results.
highest_score = search_results[0].score"""

NEW = """# === Q6 FIX: qdrant-client 1.14+ has no client.search() — use query_points ===
search_response = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=1,
)
search_results = search_response.points

# 7. Print the highest similarity score (Preserved)
highest_score = search_results[0].score"""

patched = 0
for cell in nb["cells"]:
    src = "".join(cell.get("source", []))
    if "client.search" in src and "ml_zoomcamp_faq" in src:
        if OLD not in src:
            raise RuntimeError("Expected search block not found; notebook layout changed.")
        cell["source"] = [line + "\n" for line in src.replace(OLD, NEW).splitlines()]
        cell["outputs"] = []
        cell["execution_count"] = None
        patched += 1

if patched != 1:
    raise RuntimeError(f"Expected 1 cell, patched {patched}")

NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK: patched", NOTEBOOK)
