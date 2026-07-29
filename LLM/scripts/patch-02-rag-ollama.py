"""Fix RAGPgVector typo and Ollama client cells in vector_search.ipynb."""
import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parents[1] / "02/2026/Vector_Search/code/vector_search.ipynb"

CELL_45 = """from rag_helper import RAGBase

class RAGPgVector(RAGBase):
    def __init__(self, embedder, conn, **kwargs):
        super().__init__(index=None, **kwargs)
        self.embedder = embedder
        self.conn = conn

    def search(self, query, num_results=5):
        query_vector = self.embedder.encode(query)
        query_str = vec_to_str(query_vector)
        rows = self.conn.execute(
            '''
            SELECT course, section, question, answer
            FROM documents
            WHERE course = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            ''',
            (self.course, query_str, num_results),
        ).fetchall()
        return [
            {'course': r[0], 'section': r[1], 'question': r[2], 'answer': r[3]}
            for r in rows
        ]
"""

CELL_46 = """from openai import OpenAI

OLLAMA_MODEL = 'qwen2.5:0.5b'

ollama_client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

vector_assistant = RAGPgVector(
    embedder=model,
    conn=conn,
    llm_client=ollama_client,
    model=OLLAMA_MODEL,
)

vector_assistant.rag('the program has already begun, can I still sign up?')
"""


def to_source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines or [""]


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for idx, src in ((45, CELL_45), (46, CELL_46)):
        nb["cells"][idx]["source"] = to_source(src)
        nb["cells"][idx]["outputs"] = []
        nb["cells"][idx]["execution_count"] = None
    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("patched cells 45-46")


if __name__ == "__main__":
    main()
