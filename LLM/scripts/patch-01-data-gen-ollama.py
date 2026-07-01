"""Restore Ollama flow in 01-data-gen.ipynb and remove legacy parse cells."""
import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/01-data-gen.ipynb"
nb = json.loads(NB.read_text(encoding="utf-8"))

OLLAMA_SETUP = '''from dotenv import load_dotenv
from openai import OpenAI
import httpx
import re

load_dotenv()

OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"
OLLAMA_MODEL = "qwen2.5:0.5b"

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
openai_client = client
LLM_MODEL = OLLAMA_MODEL

httpx.get("http://127.0.0.1:11434/api/tags", timeout=5.0).raise_for_status()
print("Ollama OK:", OLLAMA_BASE_URL, "model=", LLM_MODEL)

data_gen_instructions = CLOUD_DATA_GEN_INSTRUCTIONS
data_gen_instructions += "\\n\\nFormat: number each question like 1. ... 2. ... (exactly 5)."


def extract_questions_from_text(text):
    questions = re.findall(r"\\d+\\.\\s*(.*)", text)
    if not questions:
        questions = [line.strip() for line in text.split("\\n") if line.strip()]
    return questions[:5]
'''

CHAT_DEMO = '''# Ollama: chat.completions (NOT responses.parse / output_parsed)
response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=messages,
    temperature=0.0,
)
content = response.choices[0].message.content
result = Questions(questions=extract_questions_from_text(content))
print(result.questions)
'''

RECORDS_CELL = '''records = [{"question": q, "document": doc["id"]} for q in result.questions]
records
'''

GENERATE_GT = '''def generate_ground_truth(doc):
    user_prompt = json.dumps(doc)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "developer", "content": data_gen_instructions},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    content = response.choices[0].message.content
    questions_list = extract_questions_from_text(content)
    results = [{"question": q, "document": doc["id"]} for q in questions_list]
    return results, None
'''


def set_src(cell, text):
    cell["source"] = [line + "\n" for line in text.splitlines()]
    if cell["source"]:
        cell["source"][-1] = cell["source"][-1].rstrip("\n")
    cell["outputs"] = []
    cell["execution_count"] = None


# Insert Ollama if missing
if not any("OLLAMA_BASE_URL" in "".join(c.get("source", [])) for c in nb["cells"]):
    for i, c in enumerate(nb["cells"]):
        if "CLOUD_DATA_GEN_INSTRUCTIONS" in "".join(c.get("source", [])):
            nb["cells"].insert(
                i + 1,
                {"cell_type": "code", "metadata": {}, "source": [], "outputs": [], "execution_count": None},
            )
            set_src(nb["cells"][i + 1], OLLAMA_SETUP)
            break

for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))

    if "responses.parse" in src or (
        "output_parsed" in src and "SKIP" not in src and "chat.completions" not in src
    ):
        if "openai_client.responses.parse" in src or "client.responses.parse" in src:
            set_src(cell, CHAT_DEMO)
        elif "result = response.output_parsed" in src:
            set_src(cell, "# result already set above\nresult.questions")
        elif "response.output_parsed.questions" in src:
            set_src(cell, "result.questions")

    if src.strip().startswith("def generate_ground_truth"):
        set_src(cell, GENERATE_GT)

    if "for q in result.questions" in src and "records =" in src and "generate_ground_truth" not in src:
        set_src(cell, RECORDS_CELL)

    if (
        "data_gen_instructions = CLOUD_DATA_GEN_INSTRUCTIONS" in src
        and "OLLAMA_BASE_URL" not in src
        and "def extract_questions" not in src
    ):
        cell["source"] = ["# moved into Ollama cell above\n"]

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("restored", NB)
