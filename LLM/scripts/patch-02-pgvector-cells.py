"""Replace sqlitesearch cells in vector_search.ipynb with pgvector."""
import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parents[1] / "02/2026/Vector_Search/code/vector_search.ipynb"

CELLS = {
    39: """# pgvector (replaces sqlitesearch — SQL WHERE filter, no post-filter noise)
# Start DB once: docker compose -f ../docker-compose.pgvector.yml up -d
import psycopg

# Port 5433 — module 05 postgres already uses 5432 (password: password)
PG_DSN = 'postgresql://user:pswd@localhost:5433/faq'

conn = psycopg.connect(PG_DSN)
conn.execute('CREATE EXTENSION IF NOT EXISTS vector')

conn.execute('DROP TABLE IF EXISTS documents')
conn.execute('''
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        course TEXT,
        section TEXT,
        question TEXT,
        answer TEXT,
        embedding vector(384)
    )
''')
conn.commit()
print('pgvector table ready')
""",
    40: """def vec_to_str(vector):
    return '[' + ','.join(str(float(x)) for x in vector) + ']'

from tqdm.auto import tqdm

if 'vectors' not in globals() and 'X' in globals():
    vectors = list(X)

for doc, vec in tqdm(zip(documents, vectors), total=len(documents)):
    conn.execute(
        '''
        INSERT INTO documents (course, section, question, answer, embedding)
        VALUES (%s, %s, %s, %s, %s::vector)
        ''',
        (doc['course'], doc['section'], doc['question'], doc['answer'], vec_to_str(vec)),
    )

conn.commit()
print('loaded', len(documents), 'rows')
""",
    41: """query = 'I just discovered the course. Can I still join it?'
query_vector = model.encode(query)
query_str = vec_to_str(query_vector)

results = conn.execute(
    '''
    SELECT course, question, answer,
           1 - (embedding <=> %s::vector) AS similarity
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 5
    ''',
    (query_str, query_str),
).fetchall()

for row in results:
    print(f'[{row[0]}] {row[1]} (similarity: {row[3]:.4f})')
""",
    42: """results = conn.execute(
    '''
    SELECT course, question, answer,
           1 - (embedding <=> %s::vector) AS similarity
    FROM documents
    WHERE course = %s
    ORDER BY embedding <=> %s::vector
    LIMIT 5
    ''',
    (query_str, 'llm-zoomcamp', query_str),
).fetchall()

for row in results:
    print(f'[{row[0]}] {row[1]} (similarity: {row[3]:.4f})')
""",
    43: """conn.execute('''
    CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx
    ON documents USING hnsw (embedding vector_cosine_ops)
''')
conn.commit()

def pgvector_search(query, course='llm-zoomcamp', num_results=5):
    q = vec_to_str(model.encode(query))
    rows = conn.execute(
        '''
        SELECT course, section, question, answer
        FROM documents
        WHERE course = %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        ''',
        (course, q, num_results),
    ).fetchall()
    return [
        {'course': r[0], 'section': r[1], 'question': r[2], 'answer': r[3]}
        for r in rows
    ]

pgvector_search(query)
""",
}


def to_source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if not lines:
        return [""]
    if not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for idx, src in CELLS.items():
        nb["cells"][idx]["source"] = to_source(src)
        nb["cells"][idx]["outputs"] = []
        nb["cells"][idx]["execution_count"] = None
    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"patched {NOTEBOOK} cells {list(CELLS)}")


if __name__ == "__main__":
    main()
