# q2_attribute.py
"""Q2: put token counts (and cost) on the llm span attributes."""

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
from types import SimpleNamespace

from openai import OpenAI

from rag_helper import RAGBase
from starter import index

ollama_base = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
if "host.docker.internal" in ollama_base:
    ollama_base = "http://127.0.0.1:11434/v1"

client = OpenAI(
    base_url=ollama_base,
    api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
)
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Same idea as course modules; local Ollama cost is 0."""
    if "qwen" in model or "phi" in model or "ollama" in model.lower():
        return 0.0
    # gpt-5.4-mini style fallback ($/1M tokens) if using OpenAI later
    return (input_tokens * 0.15 + output_tokens * 0.60) / 1_000_000


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

            # chat.completions field names -> official homework attribute names
            input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
            cost = calculate_cost(self.model, input_tokens, output_tokens)

            span.set_attribute("input_tokens", input_tokens)
            span.set_attribute("output_tokens", output_tokens)
            span.set_attribute("cost", cost)

            print(
                f"[Q2] llm attributes: input_tokens={input_tokens} "
                f"output_tokens={output_tokens} cost={cost}"
            )
            return SimpleNamespace(output_text=text, usage=usage)

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
    print(answer.encode("ascii", errors="backslashreplace").decode("ascii"))
    print("--- look for llm span attributes.input_tokens above ---")
