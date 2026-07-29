import json
from pathlib import Path

p = Path(r"E:\IT_SPACES\AI\ZoomCamp\LLM\04\2026\Evaluation\code\01-data-gen.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

for c in nb["cells"]:
    s = "".join(c.get("source", []))

    if s.strip() == "from evaluation_utils import llm_structured":
        c["source"] = [
            "# Ollama path: do not use llm_structured(responses.parse)."
        ]

    if "result, usage = llm_structured(" in s:
        new = """# Ollama direct call (no responses.parse)
response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    temperature=0.0,
)
content = response.choices[0].message.content or ""
result = Questions(questions=extract_questions_from_text(content))
usage = None

print(result.questions)
"""
        c["source"] = [ln + "\n" for ln in new.splitlines()]
        c["source"][-1] = c["source"][-1].rstrip("\n")

    if s.strip() == "from evaluation_utils import llm_structured_retry":
        c["source"] = [
            "# generate_ground_truth below already uses Ollama chat.completions."
        ]

p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("patched")

