import json
import os
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI

APP_DIR = Path(__file__).resolve().parent


@dataclass
class LLMUsage:
    input_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatResponse:
    output_text: str
    usage: LLMUsage


def load_env() -> None:
    candidates = [APP_DIR / ".env"]
    for parent in APP_DIR.parents:
        candidates.append(parent / ".env")

    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if path.is_file():
            load_dotenv(path)
    load_dotenv()


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_llm_backend() -> str:
    load_env()
    return _env("LOCAL_LLM_BACKEND", "ollama").lower()


def get_ollama_base_url() -> str:
    return _env("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")


def get_ollama_model() -> str:
    return _env("OLLAMA_MODEL", "qwen2.5:0.5b")


def get_openai_model() -> str:
    return _env("OPENAI_MODEL", "gpt-5.4-mini")


def get_llm_client() -> OpenAI:
    load_env()
    if get_llm_backend() == "ollama":
        check_ollama_server()
        return OpenAI(
            base_url=get_ollama_base_url(),
            api_key=_env("OLLAMA_API_KEY", "ollama"),
        )
    return OpenAI()


def get_default_model() -> str:
    if get_llm_backend() == "ollama":
        return get_ollama_model()
    return get_openai_model()


def check_ollama_server() -> None:
    base_url = get_ollama_base_url()
    model = get_ollama_model()
    tags_url = base_url.replace("/v1", "") + "/api/tags"
    try:
        httpx.get(tags_url, timeout=5.0).raise_for_status()
    except Exception as e:
        raise RuntimeError(
            f"Ollama not ready at {tags_url}. "
            f"Run: ollama serve  &&  ollama pull {model}"
        ) from e


def normalize_messages(messages: list[dict]) -> list[dict]:
    normalized = []
    for message in messages:
        role = message["role"]
        if role == "developer":
            role = "system"
        normalized.append({"role": role, "content": message["content"]})
    return normalized


def chat_completion(
    client: OpenAI,
    model: str,
    messages: list[dict],
    *,
    json_mode: bool = False,
) -> ChatResponse:
    kwargs = {
        "model": model,
        "messages": normalize_messages(messages),
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    usage = response.usage
    return ChatResponse(
        output_text=response.choices[0].message.content or "",
        usage=LLMUsage(
            input_tokens=usage.prompt_tokens or 0,
            completion_tokens=usage.completion_tokens or 0,
            total_tokens=usage.total_tokens or 0,
        ),
    )


def structured_completion(
    client: OpenAI,
    instructions: str,
    user_prompt: str,
    output_type,
    model: str | None = None,
) -> tuple[object, LLMUsage]:
    model = model or get_default_model()
    schema = json.dumps(output_type.model_json_schema(), indent=2)
    system_prompt = (
        f"{instructions}\n\n"
        "Respond with valid JSON only. No markdown fences.\n"
        f"JSON schema:\n{schema}"
    )
    response = chat_completion(
        client,
        model,
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        json_mode=True,
    )
    parsed = output_type.model_validate_json(response.output_text)
    return parsed, response.usage
