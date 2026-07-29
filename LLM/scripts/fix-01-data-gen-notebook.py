"""Fix 01-data-gen.ipynb client/parse cells."""
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/01-data-gen.ipynb"
text = p.read_text(encoding="utf-8")
text = text.replace("openai_openai_client", "openai_client")
nb = json.loads(text)

for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))
    if "responses.parse" in src:
        if "openai_client.responses.parse" not in src:
            src = src.replace("client.responses.parse", "openai_client.responses.parse")
        src = src.replace('model="gemma-4-e2b"', "model=LLM_MODEL")
        if "result = response.output_parsed" not in src and "response = openai_client" in src:
            src = src.rstrip() + "\nresult = response.output_parsed\nprint(result.questions)\n"
        cell["source"] = [line + "\n" for line in src.splitlines()]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        cell["outputs"] = []
        cell["execution_count"] = None

p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("repaired", p)
