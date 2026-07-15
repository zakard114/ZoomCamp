# q1_trace.py
"""Q1: wrap rag/search/llm in OTel spans and count console spans."""

from dotenv import load_dotenv

load_dotenv()

# --- OpenTelemetry MUST be ready before any traced work ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("llm-zoomcamp")

# --- RAG stack (index from official starter; LLM = local Ollama) ---
import os
from types import SimpleNamespace

from openai import OpenAI

from rag_helper import RAGBase
from starter import index

ollama_base = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
# host.docker.internal is for containers; local script uses localhost
if "host.docker.internal" in ollama_base:
    ollama_base = "http://127.0.0.1:11434/v1"

client = OpenAI(
    base_url=ollama_base,
    api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
)
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")


class RAGTraced(RAGBase):
    """Each of rag / search / llm becomes one span (homework hint)."""

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        # Ollama speaks chat.completions, not responses.create
        with tracer.start_as_current_span("llm"):
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt},
            ]
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            text = response.choices[0].message.content or ""
            # rag() expects .output_text like the OpenAI responses object
            return SimpleNamespace(output_text=text, usage=response.usage)

    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)


if __name__ == "__main__":
    traced = RAGTraced(index=index, llm_client=client, model=MODEL)
    query = "How does the agentic loop keep calling the model until it stops?"
    print("model:", MODEL)
    print("query:", query)
    print("--- ANSWER ---")
    answer = traced.rag(query)
    # Avoid UnicodeEncodeError on Windows cp949 terminals
    print(answer.encode("ascii", errors="backslashreplace").decode("ascii"))
    print("---")
    print("Q1 tip: count ReadableSpan blocks above named rag / search / llm")
