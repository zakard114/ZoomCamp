# agent_main.py
"""
Agent loop extracted from 1-module agents.ipynb with tool-call logging (HW_05).

Uses ../code/llm_config.py for Ollama/OpenAI and ../code/ingest.py for FAQ search.
"""

from __future__ import annotations

import json
import sys
import time
import uuid
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent.parent / "code"
HW_DIR = Path(__file__).resolve().parent
LLM_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(HW_DIR))


def configure_env() -> None:
    """Postgres vars from code/.env; local Ollama from ZoomCamp/LLM/.env."""
    import os

    from dotenv import load_dotenv

    load_dotenv(CODE_DIR / ".env")
    llm_env = LLM_ROOT / ".env"
    if llm_env.is_file():
        load_dotenv(llm_env, override=True)

    if os.getenv("POSTGRES_HOST") == "postgres":
        os.environ["POSTGRES_HOST"] = "localhost"


configure_env()

from agent_db import get_tool_call_count, save_tool_call  # noqa: E402
from ingest import build_index, load_faq_data  # noqa: E402
from llm_config import get_default_model, get_llm_backend, get_llm_client, load_env  # noqa: E402

DEFAULT_INSTRUCTIONS = """
You're a course teaching assistant.
You're given a question from a course student and your task is to answer it.

If you want to look up information, use the search function.
Use as many keywords from the user question as possible when making first requests.

Make multiple searches. First perform search, analyze the results
and then perform more searches.

The question has to be about the course or its logistics. Off-topic questions
shouldn't be answered. If the search returns nothing, it's likely off-topic.
If you can't answer the question using FAQ, don't invent facts. Only use the
facts from the FAQ database.

At the end, ask if there are other areas that the user wants to explore.
""".strip()

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search the FAQ database for entries matching the given query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query text to look up in the course FAQ.",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}


def build_search_fn(index):
    def search(query: str):
        return index.search(
            query,
            num_results=5,
            boost_dict={"question": 3.0, "section": 0.5},
            filter_dict={"course": "llm-zoomcamp"},
        )

    return search


def log_tool_call(
    session_id: str,
    tool_name: str,
    tool_input: str,
    tool_output: str,
    duration_ms: float,
) -> None:
    row_id = save_tool_call(
        session_id=session_id,
        tool_name=tool_name,
        tool_input=tool_input,
        tool_output=tool_output,
        duration_ms=duration_ms,
    )
    print(f"  logged tool_call id={row_id} duration_ms={duration_ms:.1f}")


def run_logged_search(
    search_fn,
    session_id: str,
    query: str,
) -> str:
    """Execute search and log tool name/input/output/duration."""
    tool_input = json.dumps({"query": query})
    start = time.perf_counter()
    result = search_fn(query=query)
    duration_ms = (time.perf_counter() - start) * 1000
    tool_output = json.dumps(result, indent=2)
    log_tool_call(session_id, "search", tool_input, tool_output, duration_ms)
    print(f"function_call: search {tool_input}")
    return tool_output


def execute_tool_call(
    call,
    search_fn,
    session_id: str,
) -> str:
    """Run a tool and persist name/input/output/duration to Postgres."""
    tool_name = call.function.name
    tool_input = call.function.arguments
    start = time.perf_counter()

    args = json.loads(tool_input)
    if tool_name == "search":
        result = search_fn(**args)
    else:
        result = {"error": f"unknown tool: {tool_name}"}

    duration_ms = (time.perf_counter() - start) * 1000
    tool_output = json.dumps(result, indent=2)

    log_tool_call(session_id, tool_name, tool_input, tool_output, duration_ms)
    return tool_output


def agent_loop(
    instructions: str,
    question: str,
    search_fn,
    session_id: str | None = None,
    model: str | None = None,
    max_iterations: int = 10,
) -> str:
    """
    Monitored agent loop: logged FAQ searches + LLM answer.

    Small Ollama models often skip tool_choice; we always run keyword
    searches first (notebook style) so Postgres/Grafana get data, then
    let the LLM call extra tools if the model supports it.
    """
    from llm_config import chat_completion

    load_env()
    client = get_llm_client()
    model = model or get_default_model()
    session_id = session_id or str(uuid.uuid4())

    messages: list[dict] = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": question},
    ]

    print(f"session_id={session_id}")
    print(f"backend={get_llm_backend()} model={model}")

    seed_queries = [
        question,
        "join course discovered enrollment registration late",
    ]
    print("phase 1: logged FAQ searches...")
    for query in seed_queries:
        output = run_logged_search(search_fn, session_id, query)
        call_id = f"call_{uuid.uuid4().hex[:12]}"
        messages.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": call_id,
                        "type": "function",
                        "function": {
                            "name": "search",
                            "arguments": json.dumps({"query": query}),
                        },
                    }
                ],
            }
        )
        messages.append({"role": "tool", "tool_call_id": call_id, "content": output})

    last_answer = ""
    for it in range(1, max_iterations + 1):
        print(f"iteration #{it}...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=[SEARCH_TOOL],
                tool_choice="auto",
            )
        except Exception:
            response = chat_completion(client, model, messages)
            last_answer = response.output_text
            print("ASSISTANT:")
            print(last_answer)
            break

        message = response.choices[0].message
        tool_calls = message.tool_calls or []

        if tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                }
            )
            for call in tool_calls:
                output = execute_tool_call(call, search_fn, session_id)
                messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": output}
                )
            continue

        last_answer = message.content or ""
        print("ASSISTANT:")
        print(last_answer)
        break
    else:
        raise RuntimeError(f"agent loop exceeded max_iterations={max_iterations}")

    total_logged = get_tool_call_count(session_id)
    print(f"tool calls logged this session: {total_logged}")
    return last_answer


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run monitored agent loop (HW_05)")
    parser.add_argument(
        "question",
        nargs="?",
        default="I just discovered the course. Can I join it?",
        help="User question for the agent",
    )
    parser.add_argument("--session-id", default=None, help="Optional session id for logs")
    args = parser.parse_args()

    print("Loading FAQ index...")
    documents = load_faq_data()
    index = build_index(documents)
    search_fn = build_search_fn(index)

    answer = agent_loop(
        instructions=DEFAULT_INSTRUCTIONS,
        question=args.question,
        search_fn=search_fn,
        session_id=args.session_id,
    )
    print("\n--- final answer ---")
    print(answer)


if __name__ == "__main__":
    main()
