import json
from pathlib import Path

nb_path = Path(r"E:\IT_SPACES\AI\ZoomCamp\LLM\04\2026\Evaluation\code\01-data-gen.ipynb")
nb = json.loads(nb_path.read_text(encoding="utf-8"))

for cell in nb.get("cells", []):
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))

    if src.strip() == "from evaluation_utils import llm_structured":
        cell["source"] = ["# Ollama 사용: llm_structured 미사용\n"]
        continue

    if "result, usage = llm_structured(" in src:
        new_src = """# Ollama 전용 직접 호출 (responses.parse 우회)
response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[
        {"role": "developer", "content": data_gen_instructions},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.0
)

content = response.choices[0].message.content or ""
questions_list = extract_questions_from_text(content)

class Result:
    def __init__(self, questions):
        self.questions = questions

result = Result(questions_list)
usage = None

print(result.questions)
"""
        cell["source"] = [line + "\n" for line in new_src.splitlines()]
        cell["source"][-1] = cell["source"][-1].rstrip("\n")
        continue

    if src.strip() == "from evaluation_utils import llm_structured_retry":
        cell["source"] = ["# Ollama 사용: llm_structured_retry 미사용\n"]
        continue

    if "out, usage = llm_structured_retry(" in src:
        new_src = """def generate_ground_truth(doc):
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
        cell["source"] = [line + "\n" for line in new_src.splitlines()]
        cell["source"][-1] = cell["source"][-1].rstrip("\n")

nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("patched", nb_path)
