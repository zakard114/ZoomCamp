# q5_duration.py
"""Q5: run one more traced RAG query, then compare total span durations in SQLite."""

from dotenv import load_dotenv

load_dotenv()

import os
import sqlite3
from pathlib import Path
from types import SimpleNamespace

from openai import OpenAI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult

from rag_helper import RAGBase
from starter import index

DB_PATH = Path(__file__).resolve().parent / "traces.db"


class SQLiteSpanExporter(SpanExporter):
    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
            """
        )
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self, timeout_millis: int = 30000):
        return True


provider = TracerProvider()
exporter = SQLiteSpanExporter(str(DB_PATH))
provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("llm-zoomcamp")

BASE_URL = os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1")
API_KEY = os.getenv("CEREBRAS_API_KEY", "")
MODEL = os.getenv("CEREBRAS_MODEL", "gemma-4-31b")
if not API_KEY:
    raise SystemExit("CEREBRAS_API_KEY missing in .env")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)


class RAGTraced(RAGBase):
    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt},
            ]
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            text = response.choices[0].message.content or ""
            usage = response.usage
            input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
            span.set_attribute("input_tokens", input_tokens)
            span.set_attribute("output_tokens", output_tokens)
            span.set_attribute("cost", 0.0)
            return SimpleNamespace(output_text=text, usage=usage)

    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)


if __name__ == "__main__":
    traced = RAGTraced(index=index, llm_client=client, model=MODEL)
    query = "How does the agentic loop keep calling the model until it stops?"
    print("model:", MODEL)
    print("db:", DB_PATH)
    print("query:", query)

    answer = traced.rag(query)
    print("answer preview:", answer[:200].encode("ascii", errors="replace").decode("ascii"))
    exporter.shutdown()

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """
        SELECT
            name,
            COUNT(*) AS n,
            SUM(end_time - start_time) AS total_ns,
            ROUND(SUM(end_time - start_time) / 1e6, 2) AS total_ms
        FROM spans
        WHERE name != 'rag'
        GROUP BY name
        ORDER BY total_ns DESC
        """
    ).fetchall()
    conn.close()

    print("--- total duration excluding rag ---")
    for name, n, total_ns, total_ms in rows:
        print(f"  {name}: count={n}, total_ms={total_ms}")

    if not rows:
        raise SystemExit("No spans found (excluding rag)")

    winner = rows[0][0]
    if len(rows) >= 2:
        ratio = rows[0][3] / rows[1][3] if rows[1][3] else float("inf")
        close = ratio < 1.2
    else:
        close = False

    if close:
        answer_q5 = "They're all about the same"
    else:
        answer_q5 = winner

    print(f"Q5 answer: {answer_q5}")
