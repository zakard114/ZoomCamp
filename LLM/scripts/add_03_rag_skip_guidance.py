#!/usr/bin/env python3
"""Add B-path guidance and CSV skip/load cells to 03-rag-evals.ipynb."""

import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "04/2026/Evaluation/code/03-rag-evals.ipynb"
nb = json.loads(NB.read_text(encoding="utf-8"))


def md_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [ln + "\n" for ln in text.strip().splitlines()] + (["\n"] if text.strip() else []),
    }


def code_cell(text: str) -> dict:
    lines = text.strip().splitlines()
    source = [ln + "\n" for ln in lines]
    if source:
        source[-1] = source[-1].rstrip("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": source}


INTRO = """## 03 — RAG 답변 생성 (Generating RAG Answers)

### 권장 실행 (B안 — 크레딧 없을 때)
강의 제공 CSV `rag-answers-new.csv`가 이미 있으면 **OpenAI 배치(셀 19~25)는 실행하지 마세요.**

1. 셀 0~18: 데이터·구조 확인용 (선택)
2. **셀「B안: CSV 로드」** 실행 → `df_results` 준비
3. `04-llm-judge.ipynb`로 이동

### A안 (OpenAI API 크레딧 있을 때)
셀 19~25 배치 실행 → `RAG_ANSWERS_CSV` 저장
"""

SKIP_MD = """### 참고: RAG 답변 배치 실행 안내

이미 `rag-answers-new.csv`가 있고 전체 답변 생성이 끝났다면, **아래 병렬 처리 셀(19~25)은 실행하지 않아도 됩니다.**

- 크레딧 없이 `ThreadPoolExecutor` 배치를 돌리면 `RateLimitError`로 중단됩니다.
- 대신 위/아래 **「B안: CSV 로드」** 셀을 실행한 뒤 `04-llm-judge.ipynb`로 넘어가세요.
"""

LOAD_B = """# B안: 배치 스킵 — 강의 제공 CSV 로드 (권장)
df_results = pd.read_csv(RAG_ANSWERS_CSV)
print("loaded:", RAG_ANSWERS_CSV.resolve())
print("rows:", len(df_results))
df_results.head()
"""

# Top intro (index 0)
if not (nb["cells"] and nb["cells"][0].get("cell_type") == "markdown" and "03 — RAG" in "".join(nb["cells"][0].get("source", []))):
    nb["cells"].insert(0, md_cell(INTRO))

# Find ThreadPoolExecutor import cell
batch_idx = None
for i, c in enumerate(nb["cells"]):
    if c.get("cell_type") == "code" and "ThreadPoolExecutor" in "".join(c.get("source", [])):
        batch_idx = i
        break

if batch_idx is None:
    raise SystemExit("ThreadPoolExecutor cell not found")

# Skip markdown + B load cell before batch
already = any("B안: 배치 스킵" in "".join(c.get("source", [])) for c in nb["cells"])
if not already:
    nb["cells"].insert(batch_idx, code_cell(LOAD_B))
    nb["cells"].insert(batch_idx, md_cell(SKIP_MD))

# Patch total_cost cells with safe note (optional comment only)
for c in nb["cells"]:
    if c.get("cell_type") != "code":
        continue
    src = "".join(c.get("source", []))
    if src.strip() == "assistant.total_cost()":
        c["source"] = [
            "# OpenAI API 사용 시에만 의미 있음. B안(CSV 로드) 또는 로컬 LLM이면 스킵 가능.\n",
            "try:\n",
            "    assistant.total_cost()\n",
            "except Exception as e:\n",
            '    print("cost skipped:", e)\n',
        ]

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("updated", NB)
