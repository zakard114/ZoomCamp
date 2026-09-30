# AI Dev Tools Zoomcamp 2026 — Homework 2: Build and Ship an AI-Assisted Full-Stack App

Submission write-up for Module 02 homework  
(spec → frontend mock → OpenAPI → FastAPI → connect → SQLAlchemy/SQLite).

**Course:** [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/02-development/homework.md)  
**Submit form (browser only, not a form answer):** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw2  

**Local project:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\02\Development\LaneDeck\`  
**Homework URL (paste into form):** https://github.com/zakard114/LaneDeck

Style reference (Module 01): `E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AIDT_HW_chores\AIDT_01_HW.md`

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | **Mini Kanban board** |
| 2 | **LaneDeck** |
| 3 | **`cf878545446c6ab67ee7a4ccbfe61edcccaa6579`** |
| 4 | **`npm run dev`** (from `frontend/`) |
| 5 | **`uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000`** (from `backend/`) |
| 6 | **`http://127.0.0.1:8000`** |
| 7 | **`uv run pytest -q`** (from `backend/`) |

**Homework URL (repo):** https://github.com/zakard114/LaneDeck

---

## Q1 — Which project did you choose?

Official options: Expense splitter / Restaurant waitlist manager / Mini Kanban board / Sports-league scoreboard.

```text
Mini Kanban board
```

---

## Q2 — Spec first — what's the name you chose?

Spec saved in [`_docs/specs.md`](_docs/specs.md).

```text
LaneDeck
```

---

## Q3 — GitHub repository — sha1 of the foundation commit?

Repo created with `_docs/specs.md`, `.gitignore`, `README.md`, `AGENTS.md`, then committed and pushed.

```text
cf878545446c6ab67ee7a4ccbfe61edcccaa6579
```

Commit message: `Add LaneDeck homework foundation: spec, README, AGENTS, gitignore.`

---

## Q4 — Frontend prototype — which command starts the frontend?

Interactive Kanban UI in [`frontend/`](frontend/) with centralized API calls in [`frontend/src/api/cardsApi.ts`](frontend/src/api/cardsApi.ts) (first mocked, later HTTP).

```text
npm run dev
```

Run from `frontend/` after `npm install`. Opens http://127.0.0.1:5173/

---

## Q5 — Backend — which command starts the backend?

FastAPI + `uv` under [`backend/`](backend/), contract in [`openapi.yaml`](openapi.yaml).

```text
uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000
```

Run from `backend/` after `uv sync --group dev`. Docs: http://127.0.0.1:8000/docs

Local note: if port 8000 is occupied (e.g. another app), use another port and set `VITE_API_BASE_URL` to match. Form answer stays **8000** (code default).

---

## Q6 — Connect frontend and backend — which URL does the frontend use?

```text
http://127.0.0.1:8000
```

Defined as `API_BASE_URL` in [`frontend/src/api/cardsApi.ts`](frontend/src/api/cardsApi.ts) (override with `VITE_API_BASE_URL`).

---

## Q7 — Database — which command runs tests?

Mock store replaced with SQLAlchemy + SQLite (`backend/data/app.db`; `DATABASE_URL` override ready). Persistence covered in [`backend/tests/test_persistence.py`](backend/tests/test_persistence.py).

```text
uv run pytest -q
```

Run from `backend/`.

---

## Verification log

Environment: Windows, caches on `E:\IT_SPACES\AI\.cache\` via `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.

| Check | Result |
|-------|--------|
| Frontend build | `npm run build` OK |
| Backend tests | **9 passed** (`uv run pytest -q`) |
| Manual UI | Create / move across Todo→Doing→Done / edit / delete; data survives refresh |

Key commits (GitHub `main`):

| SHA (short) | Step |
|-------------|------|
| `cf87854` | Spec foundation (Q3) |
| `cd27d4f` | Frontend + mocked API (Q4) |
| `333b50b` | OpenAPI + FastAPI mock + tests (Q5) |
| `07f5e18` | FE → HTTP backend (Q6) |
| `3f0c5e4` | SQLAlchemy / SQLite (Q7) |

---

## How to run locally

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

# Backend
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\02\Development\LaneDeck\backend
uv sync --group dev
uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000

# Frontend (other terminal)
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\02\Development\LaneDeck\frontend
npm install
npm run dev

# Tests
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\02\Development\LaneDeck\backend
uv run pytest -q
```

- UI: http://127.0.0.1:5173/  
- API docs: http://127.0.0.1:8000/docs  
