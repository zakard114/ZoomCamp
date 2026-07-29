# q6_token_stability.py
"""Q6: run RAG until 4 llm spans exist, then check input_tokens stability with pandas."""

from dotenv import load_dotenv

load_dotenv()

import os
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
from openai import OpenAI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult

from rag_helper import RAGBase
from starter import index

DB_PATH = Path(__file__).resolve().parent / "traces.db"
TARGET_LLM_RUNS = 4
QUERY = "How does the agentic loop keep calling the model until it stops?"


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


def count_llm_spans() -> int:
    conn = sqlite3.connect(DB_PATH)
    n = conn.execute(
        "SELECT COUNT(*) FROM spans WHERE name = 'llm' AND input_tokens IS NOT NULL"
    ).fetchone()[0]
    conn.close()
    return int(n)


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
    existing = count_llm_spans()
    need = max(0, TARGET_LLM_RUNS - existing)
    print(f"model: {MODEL}")
    print(f"db: {DB_PATH}")
    print(f"existing llm spans with tokens: {existing}; will run {need} more")

    for i in range(need):
        print(f"--- run {existing + i + 1}/{TARGET_LLM_RUNS} ---")
        answer = traced.rag(QUERY)
        preview = answer[:160].encode("ascii", errors="replace").decode("ascii")
        print("answer preview:", preview)

    exporter.shutdown()

    df = pd.read_sql_query(
        "SELECT name, input_tokens, output_tokens, cost FROM spans WHERE name = 'llm'",
        sqlite3.connect(DB_PATH),
    )
    # Keep the first TARGET_LLM_RUNS llm rows that have tokens
    df = df[df["input_tokens"].notna()].head(TARGET_LLM_RUNS).copy()
    tokens = df["input_tokens"].astype(int).tolist()
    print("--- llm input_tokens (first 4) ---")
    print(tokens)

    if len(tokens) < TARGET_LLM_RUNS:
        raise SystemExit(f"Need {TARGET_LLM_RUNS} llm spans, got {len(tokens)}")

    mn, mx = min(tokens), max(tokens)
    if mn == mx:
        answer_q6 = "They're identical"
        pct = 0.0
    else:
        # relative spread vs the smaller value (conservative)
        pct = (mx - mn) / mn * 100
        if pct <= 10:
            answer_q6 = "Within 10% of each other"
        elif pct <= 50:
            answer_q6 = "Within 50% of each other"
        else:
            answer_q6 = "They vary more than 50%"

    print(f"min={mn}, max={mx}, relative_spread_pct={pct:.2f}")
    print(f"Q6 answer: {answer_q6}")
