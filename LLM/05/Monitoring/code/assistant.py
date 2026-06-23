import sys

from ingest import load_faq_data, build_index
from llm_config import get_default_model, get_llm_client
from metrics import RAGWithMetrics
from db_save import save_conversation


def create_assistant():
    documents = load_faq_data()
    index = build_index(documents)

    return RAGWithMetrics(
        index=index,
        llm_client=get_llm_client(),
        model=get_default_model(),
    )


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag(query)
    print(answer)

    try:
        save_conversation(assistant.last_call, query, "llm-zoomcamp")
    except Exception as e:
        print(f"(DB save skipped: PostgreSQL not running - {e})")
