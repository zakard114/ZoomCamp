# LLM Zoomcamp — Module 04 (Evaluation)

2026 curriculum: former module 3 → **module 4**.

## Layout

| Path | Cohort | Notes |
|------|--------|-------|
| [`2026/Evaluation/`](2026/Evaluation/) | **2026** | Main workspace (updated course) |
| [`2025/Evaluation/`](2025/Evaluation/) | 2025 | Archive — ground-truth, offline eval |

**Module-level (shared by both cohorts):**

| Item | Purpose |
|------|---------|
| `docker-compose.qdrant.yml` | Qdrant on E: (`docker-data/volumes/qdrant-data`) |
| `cache/` | FastEmbed / Hugging Face cache (see `.env.example`) |
| `fix-docker-wsl*.ps1`, `RUN-DOCKER-FIX.bat` | Docker Desktop / WSL troubleshooting |
| `.env.example` | Cache paths for this module |

**Repo-level:** `LLM/.env`, `LLM/.venv`, `LLM/models/`, `LLM/scripts/`, `LLM/atomic-llama-cpp-turboquant/`

---

## Qdrant

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\LLM\04
docker compose -f docker-compose.qdrant.yml up -d
```

Or reuse module 02 Qdrant — do not bind port **6333** twice.

---

## Notebook cache (E:)

```python
import os
os.environ["FASTEMBED_CACHE_PATH"] = r"E:/IT_SPACES/AI/ZoomCamp/LLM/04/cache/fastembed"
os.environ["HF_HOME"] = r"E:/IT_SPACES/AI/ZoomCamp/LLM/04/cache/huggingface"
```
