import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code"


def patch_cells(path: Path, replacements: list[tuple[str, str]]) -> int:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        orig = src
        for old, new in replacements:
            src = src.replace(old, new)
        if src != orig:
            lines = src.splitlines()
            cell["source"] = [ln + "\n" for ln in lines]
            if cell["source"]:
                cell["source"][-1] = cell["source"][-1].rstrip("\n")
            changed += 1
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return changed


patch_cells(
    BASE / "03-rag-evals.ipynb",
    [
        (
            "import pandas as pd\n",
            "import pandas as pd\nfrom evaluation_paths import GROUND_TRUTH_CSV, RAG_ANSWERS_CSV\n",
        ),
        (
            'df_ground_truth = pd.read_csv("data/ground_truth-new.csv")',
            "df_ground_truth = pd.read_csv(GROUND_TRUTH_CSV)",
        ),
        (
            'df_results.to_csv("data/rag-answers-new.csv", index=False)',
            "df_results.to_csv(RAG_ANSWERS_CSV, index=False)",
        ),
    ],
)

patch_cells(
    BASE / "04-llm-judge.ipynb",
    [
        (
            "import pandas as pd\n",
            "import pandas as pd\nfrom evaluation_paths import RAG_ANSWERS_CSV, RAG_EVALUATIONS_CSV\n",
        ),
        (
            'df_answers = pd.read_csv("data/rag-answers-new.csv")',
            "df_answers = pd.read_csv(RAG_ANSWERS_CSV)",
        ),
        (
            'df_eval.to_csv("data/rag-evaluations-new.csv", index=False)',
            "df_eval.to_csv(RAG_EVALUATIONS_CSV, index=False)",
        ),
    ],
)

print("patched 03 and 04")
