import json

import requests
from minsearch import Index

from evaluation_paths import FAQ_CACHE


def _download_faq_all_courses():
    docs_url = "https://datatalks.club/faq/json/courses.json"
    response = requests.get(docs_url, timeout=60)
    response.raise_for_status()
    courses_raw = response.json()

    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in courses_raw:
        course_url = f"{url_prefix}{course['path']}"
        course_response = requests.get(course_url, timeout=60)
        course_response.raise_for_status()
        documents.extend(course_response.json())

    return documents


def load_faq_data(*, download_if_missing: bool = False):
    """Load llm-zoomcamp FAQ documents from local cache (no network by default)."""
    if FAQ_CACHE.exists():
        return json.loads(FAQ_CACHE.read_text(encoding="utf-8"))

    if not download_if_missing:
        raise FileNotFoundError(
            f"FAQ cache missing: {FAQ_CACHE}\n"
            "Run once from code/:  python snapshot_faq_cache.py\n"
            "(Eval CSVs in data/ are separate; FAQ corpus is not in ground_truth-new.csv.)"
        )

    all_docs = _download_faq_all_courses()
    documents = [d for d in all_docs if d.get("course") == "llm-zoomcamp"]
    FAQ_CACHE.parent.mkdir(parents=True, exist_ok=True)
    FAQ_CACHE.write_text(json.dumps(documents, ensure_ascii=False, indent=2), encoding="utf-8")
    return documents


def build_index(documents):
    index = Index(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"],
    )
    index.fit(documents)
    return index
