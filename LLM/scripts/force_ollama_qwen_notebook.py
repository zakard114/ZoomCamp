import json
from pathlib import Path

p = Path(r"E:\IT_SPACES\AI\ZoomCamp\LLM\04\2026\Evaluation\code\01-data-gen.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
changed = 0

for c in nb.get("cells", []):
    s = "".join(c.get("source", []))

    if "openai_client = OpenAI()" in s:
        s = """from dotenv import load_dotenv
from openai import OpenAI
import httpx
import re

load_dotenv()

OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"
LLM_MODEL = "qwen2.5:0.5b"
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

httpx.get("http://127.0.0.1:11434/api/tags", timeout=5.0).raise_for_status()
print("Ollama OK:", OLLAMA_BASE_URL, "model=", LLM_MODEL)

def extract_questions_from_text(text):
    questions = re.findall(r"\\d+\\.\\s*(.*)", text)
    if not questions:
        questions = [line.strip() for line in text.split("\\n") if line.strip()]
    return questions[:5]
"""
        c["source"] = [ln + "\n" for ln in s.splitlines()]
        c["source"][-1] = c["source"][-1].rstrip("\n")
        changed += 1

    elif "response = openai_client.responses.parse(" in s:
        s = """# Ollama: use chat.completions (OpenAI-compatible)
response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    temperature=0.0,
)
content = response.choices[0].message.content or ""
result = Questions(questions=extract_questions_from_text(content))
"""
        c["source"] = [ln + "\n" for ln in s.splitlines()]
        c["source"][-1] = c["source"][-1].rstrip("\n")
        changed += 1

    elif "response.output_parsed.questions" in s:
        c["source"] = ["result.questions"]
        changed += 1

    elif "out, usage = llm_structured_retry(" in s and "openai_client" in s:
        s = """def generate_ground_truth(doc):
    user_prompt = json.dumps(doc)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "developer", "content": data_gen_instructions},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    content = response.choices[0].message.content or ""
    questions_list = extract_questions_from_text(content)

    results = []
    for q in questions_list:
        results.append({
            "question": q,
            "document": doc["id"]
        })

    return results, None
"""
        c["source"] = [ln + "\n" for ln in s.splitlines()]
        c["source"][-1] = c["source"][-1].rstrip("\n")
        changed += 1

    elif "ThreadPoolExecutor(max_workers=6)" in s:
        s = s.replace("max_workers=6", "max_workers=1")
        c["source"] = [ln + "\n" for ln in s.splitlines()]
        c["source"][-1] = c["source"][-1].rstrip("\n")
        changed += 1

p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("changed", changed)
