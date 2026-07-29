import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from tqdm.auto import tqdm

from rag_helper import RAGBase

class Questions(BaseModel):
    questions: list[str]

GEMMA_DATA_GEN_INSTRUCTIONS = """
You emulate a student who's taking our course.
Formulate exactly 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record.

The output should resemble how people ask questions on the internet. Not too formal, not too short, not too long.

IMPORTANT: Return only valid JSON with a single field "questions" containing exactly 5 strings.
No markdown fences, no commentary, no extra keys.
""".strip()


def _load_llm_dotenv() -> None:
    llm_root = Path(__file__).resolve().parents[4]
    load_dotenv(llm_root / ".env")


def _llm_settings() -> dict[str, str]:
    _load_llm_dotenv()
    local_backend = os.environ.get("LOCAL_LLM_BACKEND", "ollama")
    return {
        "local_base_url": os.environ.get("LLAMA_BASE_URL", "http://127.0.0.1:8081/v1"),
        "local_api_key": os.environ.get("LLAMA_API_KEY", "gemma-mtp"),
        "ollama_base_url": os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1"),
        "ollama_api_key": os.environ.get("OLLAMA_API_KEY", "ollama"),
        "ollama_model": os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b"),
        "cerebras_base_url": os.environ.get("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1"),
        "cerebras_api_key": os.environ.get("CEREBRAS_API_KEY", ""),
        "cerebras_model": os.environ.get("CEREBRAS_MODEL", "gemma-4-31b"),
        "local_backend": local_backend,
        "eval_backend": os.environ.get("EVAL_LLM_BACKEND", local_backend),
        "cloud_model": os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
    }


def get_openai_client(*, local: bool = False, backend: str | None = None) -> OpenAI:
    settings = _llm_settings()
    if local:
        backend = (backend or settings["eval_backend"]).lower()
        if backend == "cerebras":
            if not settings["cerebras_api_key"]:
                raise RuntimeError("CEREBRAS_API_KEY is not set in LLM/.env")
            return OpenAI(
                base_url=settings["cerebras_base_url"],
                api_key=settings["cerebras_api_key"],
            )
        if backend == "ollama":
            return OpenAI(
                base_url=settings["ollama_base_url"],
                api_key=settings["ollama_api_key"],
            )
        return OpenAI(
            base_url=settings["local_base_url"],
            api_key=settings["local_api_key"],
        )
    _load_llm_dotenv()
    return OpenAI()


def get_default_model(
    client: OpenAI,
    *,
    local: bool = False,
    backend: str | None = None,
) -> str:
    settings = _llm_settings()
    if local:
        backend = (backend or settings["eval_backend"]).lower()
        if backend == "cerebras":
            return settings["cerebras_model"]
        if backend == "ollama":
            return settings["ollama_model"]
        return client.models.list().data[0].id
    return settings["cloud_model"]


def check_local_server(client: OpenAI, *, backend: str | None = None) -> None:
    """Raise if local Ollama, Cerebras, or llama-server is not reachable."""
    import httpx

    settings = _llm_settings()
    backend = (backend or settings["eval_backend"]).lower()
    base = str(client.base_url).rstrip("/")

    if backend == "cerebras" or "api.cerebras.ai" in base:
        try:
            client.models.list()
        except Exception as e:
            raise RuntimeError(
                f"Cerebras API not ready at {settings['cerebras_base_url']}. "
                "Check CEREBRAS_API_KEY in LLM/.env"
            ) from e
        return

    if backend == "ollama" or ":11434" in base:
        tags_url = base.replace("/v1", "") + "/api/tags"
        try:
            httpx.get(tags_url, timeout=5.0).raise_for_status()
        except Exception as e:
            raise RuntimeError(
                f"Ollama not ready at {tags_url}. "
                f"Run: ollama serve  &&  ollama pull {settings['ollama_model']}"
            ) from e
        return

    health_url = base.replace("/v1", "") + "/health"
    try:
        httpx.get(health_url, timeout=5.0).raise_for_status()
    except Exception as e:
        raise RuntimeError(
            f"Local llama-server not ready at {health_url}. "
            "Run: powershell -File E:/IT_SPACES/AI/ZoomCamp/LLM/scripts/start-gemma4-e2b-mtp-server.ps1"
        ) from e


def calc_price(usage):
    if usage is None:
        return {"input_cost": 0.0, "output_cost": 0.0, "total_cost": 0.0}

    input_price_per_million = 0.75
    output_price_per_million = 4.50

    input_cost = (usage.input_tokens / 1_000_000) * input_price_per_million
    output_cost = (usage.output_tokens / 1_000_000) * output_price_per_million
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def calc_total_price(usages):
    total_cost = 0.0

    for usage in usages:
        cost = calc_price(usage)
        total_cost = total_cost + cost["total_cost"]

    return total_cost


def _is_cerebras_client(client: OpenAI) -> bool:
    return "api.cerebras.ai" in str(client.base_url)


def get_prompt_tokens(usage) -> int:
    if usage is None:
        return 0
    return getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", 0)


def _parse_json_response(text: str, output_type):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    return output_type.model_validate(json.loads(cleaned))


def _llm_structured_chat(client, instructions, user_prompt, output_type, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Model returned empty content")
    return _parse_json_response(content, output_type), response.usage


def llm_structured(client, instructions, user_prompt, output_type, model=None):
    settings = _llm_settings()
    if model is None:
        model = settings["cloud_model"]
    if _is_cerebras_client(client):
        return _llm_structured_chat(
            client, instructions, user_prompt, output_type, model
        )

    messages = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = client.responses.parse(
        model=model,
        input=messages,
        text_format=output_type
    )

    return response.output_parsed, response.usage


def llm_structured_retry(
    client,
    instructions,
    user_prompt,
    output_type,
    model=None,
    max_retries=3,
):
    settings = _llm_settings()
    if model is None:
        model = settings["cloud_model"]
    for attempt in range(max_retries):
        try:
            return llm_structured(
                client,
                instructions,
                user_prompt,
                output_type,
                model=model,
            )
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)


class RAGWithUsage(RAGBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usages = []
        self.last_usage = None

    def reset_usage(self):
        self.usages = []
        self.last_usage = None

    def search(self, query, num_results=5):
        boost_dict = {"question": 1.0, "answer": 2.0, "section": 0.1}
        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )

    def llm(self, prompt):
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        self.last_usage = response.usage
        self.usages.append(response.usage)

        return response.output_text

    def total_cost(self):
        return calc_total_price(self.usages)


def map_progress(pool, seq, f):
    results = []

    with tqdm(total=len(seq)) as progress:
        futures = []

        for el in seq:
            future = pool.submit(f, el)
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)

        for future in futures:
            result = future.result()
            results.append(result)

    return results
