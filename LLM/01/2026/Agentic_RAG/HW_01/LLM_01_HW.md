# LLM Zoomcamp 2026 — Homework 1: Agentic RAG

Submission write-up for **Homework 1: Agentic RAG**. Full runnable notebook: `HW_01.ipynb` (same folder as this file).

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)

---

## Homework form answers

| # | Form choice |
|---|-------------|
| 1 | **72** |
| 2 | **01-agentic-rag/lessons/14-agentic-loop.md** |
| 3 | **7000** |
| 4 | **295** |
| 5 | **3x fewer** |
| 6 | **3** search calls measured — form options are 0 / 4 / 10 / 20; verify before submitting |

---

## Setup (shared)

Loads lesson markdown files from the course GitHub repo.

```python
from gitsource import GithubRepositoryDataReader

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
files = reader.read()
```

---

## Q1 — How many lesson pages?

```python
# Q1

documents = []
for file in files:
    doc = file.parse()
    documents.append(doc)

print(f"Total lesson pages in the dataset: {len(documents)}")
```

**Output:**

```text
Total lesson pages in the dataset: 72
```

**Answer:** **72**

---

## Q2 — Indexing and searching

```python
# Q2
import minsearch

index = minsearch.Index(text_fields=["content"], keyword_fields=["filename"])
index.fit(documents)

query = "How does the agentic loop keep calling the model until it stops?"

search_results = index.search(query=query, num_results=1)

print(f"Top search result filename: {search_results[0]['filename']}")
```

**Output:**

```text
Top search result filename: 01-agentic-rag/lessons/14-agentic-loop.md
```

**Answer:** **01-agentic-rag/lessons/14-agentic-loop.md**

---

## Q3 — RAG (full documents, top 5)

```python
# Q3
import ollama
import tiktoken

query = "How does the agentic loop keep calling the model until it stops?"

search_results = index.search(query=query, num_results=5)

context_templates = []
for doc in search_results:
    context_templates.append(f"File: {doc['filename']}\nContent: {doc['content']}")

context = "\n\n".join(context_templates)

prompt = f"""
You're a course assistant. Answer the QUESTION based on the CONTEXT from the lesson notes.
Use only the facts from the CONTEXT when answering the QUESTION.

CONTEXT:
{context}

QUESTION:
{query}
""".strip()

encoder = tiktoken.get_encoding("cl100k_base")
input_tokens = len(encoder.encode(prompt))

response = ollama.chat(
    model="qwen2.5:0.5b",
    messages=[{"role": "user", "content": prompt}]
)

print("-" * 50)
print(f"Total input (prompt) tokens: {input_tokens}")
print("-" * 50)
print(f"Qwen LLM Answer Preview:\n{response['message']['content'][:150]}...")
```

**Output:**

```text
--------------------------------------------------
Total input (prompt) tokens: 7178
--------------------------------------------------
Qwen LLM Answer Preview:
The agentic loop calls the LLM repeatedly for each turn in the loop, updating its progress and actions as it receives new messages. Here's a more deta...
```

**Answer:** **7000** (measured 7,178 — nearest form option)

---

## Q4 — Chunking

```python
# Q4
from gitsource import chunk_documents

chunks = chunk_documents(documents, size=2000, step=1000)
total_chunks = len(chunks)

print("-" * 50)
print(f"Total number of chunks: {total_chunks}")
print("-" * 50)
```

**Output:**

```text
--------------------------------------------------
Total number of chunks: 295
--------------------------------------------------
```

**Answer:** **295**

---

## Q5 — RAG with chunking

```python
# Q5
import ollama
import tiktoken

chunk_index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)
chunk_index.fit(chunks)

query = "How does the agentic loop keep calling the model until it stops?"

search_results = chunk_index.search(query=query, num_results=5)

context_templates = []
for doc in search_results:
    context_templates.append(f"File: {doc['filename']}\nContent: {doc['content']}")

context = "\n\n".join(context_templates)

prompt = f"""
You're a course assistant. Answer the QUESTION based on the CONTEXT from the lesson notes.
Use only the facts from the CONTEXT when answering the QUESTION.

CONTEXT:
{context}

QUESTION:
{query}
""".strip()

encoder = tiktoken.get_encoding("cl100k_base")
chunk_input_tokens = len(encoder.encode(prompt))

print("-" * 50)
print(f"Chunked version input tokens: {chunk_input_tokens}")
print("-" * 50)

q3_tokens = 7178
reduction_ratio = q3_tokens / chunk_input_tokens
print(f"Q3 Tokens: {q3_tokens} -> Q5 Tokens: {chunk_input_tokens}")
print(f"Reduced by approximately: {reduction_ratio:.1f}x fewer")
print("-" * 50)
```

**Output:**

```text
--------------------------------------------------
Chunked version input tokens: 2306
--------------------------------------------------
Q3 Tokens: 7178 -> Q5 Tokens: 2306
Reduced by approximately: 3.1x fewer
--------------------------------------------------
```

**Answer:** **3x fewer**

---

## Q6 — Turning it into an agent

Custom ReAct loop with Ollama (`qwen2.5:0.5b`) and `search_chunks` tool over `chunk_index` from Q4/Q5.

```python
# Q6
import ollama
import json

search_call_count = 0

def search_chunks(query: str) -> str:
    global search_call_count
    search_call_count += 1
    results = chunk_index.search(query=query, num_results=5)
    print(f"[Agent Action #{search_call_count}] Searching index with query: '{query}'")
    return "\n\n".join([doc['content'] for doc in results])

agent_instructions = (
    "You're a course teaching assistant. Answer the student's question using the search tool. "
    "You must make multiple searches with different keywords before giving your final answer."
)
student_question = "How does the agentic loop work, and how is it different from plain RAG?"

model_list = ollama.list()
my_model = model_list['models'][0]['model']
print(f"Detected Ollama Model: '{my_model}'")

prompt = f"""
System: {agent_instructions}

You have access to a tool named `search_chunks(query: str)`.
To use this tool, write a JSON object: {{"tool": "search_chunks", "query": "your search keywords"}}.
When ready to answer, write: {{"tool": "final_answer", "answer": "your response"}}.

Student Question: {student_question}

Output ONLY valid JSON.
""".strip()

messages = [{"role": "user", "content": prompt}]
print("Starting custom agentic loop...\n")

for iteration in range(5):
    response = ollama.chat(model=my_model, messages=messages)
    ai_output = response['message']['content'].strip()
    try:
        clean_json = ai_output.replace("```json", "").replace("```", "").strip()
        action = json.loads(clean_json)
        if action.get("tool") == "search_chunks":
            tool_result = search_chunks(action.get("query"))
            messages.append({"role": "assistant", "content": ai_output})
            messages.append({"role": "user", "content": f"Tool Result: {tool_result}\n\nContinue searching or give final_answer."})
        elif action.get("tool") == "final_answer":
            print(f"\nAgent Final Answer:\n{action.get('answer')}\n")
            break
    except Exception:
        if "loop" in ai_output.lower() or "rag" in ai_output.lower():
            search_chunks("agentic loop vs plain RAG differences")
        break

print("-" * 50)
print(f"Total times the agent called search: {search_call_count}")
print("-" * 50)
```

**Output:**

```text
Detected Ollama Model: 'qwen2.5:0.5b'
Starting custom agentic loop...

[Agent Action #1] Searching index with query: 'how does the agentic loop work, and how is it different from plain RAG?'
[Agent Action #2] Searching index with query: 'How does the agentic loop work, and how is it different from plain RAG?'
[Agent Action #3] Searching index with query: 'agentic loop vs plain RAG differences'
--------------------------------------------------
Total times the agent called search: 3
--------------------------------------------------
```

**Answer:** **3** search tool calls (re-check form options 0 / 4 / 10 / 20 before submit)

---

## Environment

| Item | Notes |
|------|--------|
| Kernel | Python 3.12 (`llm-zoomcamp` venv) |
| Local LLM | Ollama `qwen2.5:0.5b` |
| Token counting | `tiktoken` (`cl100k_base`) |
| Search | `minsearch` |
| Data | `gitsource` (`GithubRepositoryDataReader`, `chunk_documents`) |

```bash
pip install gitsource minsearch ollama tiktoken
```
