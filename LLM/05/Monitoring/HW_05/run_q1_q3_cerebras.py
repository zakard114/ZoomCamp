# run_q1_q3_cerebras.py
"""Re-run HW5 Q1–Q3 with Cerebras + gemma-4-31b (fast cloud)."""

from dotenv import load_dotenv

load_dotenv()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("llm-zoomcamp")

import os
import time
from types import SimpleNamespace

from openai import OpenAI

from rag_helper import RAGBase
from starter import index

BASE_URL = os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1")
API_KEY = os.getenv("CEREBRAS_API_KEY", "")
MODEL = os.getenv("CEREBRAS_MODEL", "gemma-4-31b")

if not API_KEY:
    raise SystemExit("CEREBRAS_API_KEY missing in .env")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

LAST = {"input_tokens": None, "output_tokens": None, "llm_ms": None}


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
            t0 = time.perf_counter()
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            llm_ms = (time.perf_counter() - t0) * 1000
            text = response.choices[0].message.content or ""
            usage = response.usage
            input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
            span.set_attribute("input_tokens", input_tokens)
            span.set_attribute("output_tokens", output_tokens)
            span.set_attribute("cost", 0.0)
            LAST["input_tokens"] = input_tokens
            LAST["output_tokens"] = output_tokens
            LAST["llm_ms"] = llm_ms
            print(
                f"[METRICS] input_tokens={input_tokens} "
                f"output_tokens={output_tokens} llm_ms={llm_ms:.1f}"
            )
            return SimpleNamespace(output_text=text, usage=usage)

    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)


def closest_token_bucket(n: int) -> int:
    return min([700, 7000, 70000, 700000], key=lambda c: abs(c - n))


def ms_bucket(ms: float) -> str:
    if ms < 100:
        return "Under 100ms"
    if ms < 500:
        return "100-500ms"
    if ms <= 2000:
        return "500-2000ms"
    return "Over 2000ms"


if __name__ == "__main__":
    traced = RAGTraced(index=index, llm_client=client, model=MODEL)
    query = "How does the agentic loop keep calling the model until it stops?"
    print("backend: Cerebras")
    print("model:", MODEL)
    print("query:", query)
    print("--- ANSWER ---")
    answer = traced.rag(query)
    print(answer.encode("ascii", errors="backslashreplace").decode("ascii")[:2000])
    print("--- SUMMARY (Q1-Q3) ---")
    print("Q1 spans: search + llm + rag → 3")
    print(
        f"Q2 input_tokens={LAST['input_tokens']} "
        f"→ closest form choice {closest_token_bucket(LAST['input_tokens'])}"
    )
    print(
        f"Q3 llm_ms={LAST['llm_ms']:.1f} "
        f"→ form choice {ms_bucket(LAST['llm_ms'])}"
    )
    if LAST["llm_ms"] and LAST["llm_ms"] >= 1000:
        print(f"     (~{LAST['llm_ms']/1000:.1f}s if form uses second-scale options)")
    print("Also count three ReadableSpan JSON blocks above for Q1.")
