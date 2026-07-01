import json
from pathlib import Path

p = Path(r"E:\IT_SPACES\AI\ZoomCamp\LLM\04\2026\Evaluation\code\01-data-gen.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

for c in nb["cells"]:
    s = "".join(c.get("source", []))

    if "documents_llm = []" in s:
        c["source"] = [
            "# Keep full FAQ corpus (all courses); do NOT filter to llm-zoomcamp\n",
            "# documents_llm = []\n",
            "# for doc in documents:\n",
            "#     if doc[\"course\"] == \"llm-zoomcamp\":\n",
            "#         documents_llm.append(doc)\n",
            "# len(documents_llm)\n",
            "print(\"documents:\", len(documents))\n",
        ]

    if s.strip() == "documents = documents_llm":
        c["source"] = [
            "# documents = documents_llm  # disabled to keep full dataset\n",
            "print(\"documents:\", len(documents))\n",
        ]

    if "with ThreadPoolExecutor(max_workers=1) as pool:" in s:
        c["source"] = [
            "documents = load_faq_data()\n",
            "print(\"documents_full:\", len(documents))\n",
            "\n",
            "with ThreadPoolExecutor(max_workers=1) as pool:\n",
            "    results = map_progress(pool, documents, generate_ground_truth)\n",
        ]

p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("patched")

