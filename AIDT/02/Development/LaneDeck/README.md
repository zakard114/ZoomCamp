# LaneDeck

Lightweight Kanban board for organizing tasks across **Todo → Doing → Done**.

Spec-first build: frontend (mocked API) → OpenAPI → FastAPI → SQLite.

## Spec

See [`_docs/specs.md`](_docs/specs.md).

API contract: [`openapi.yaml`](openapi.yaml).

## Layout

```text
LaneDeck/
  _docs/specs.md
  AGENTS.md
  README.md
  openapi.yaml
  frontend/     # Vite + React + TypeScript → HTTP API
  backend/      # FastAPI + uv + SQLAlchemy/SQLite
```

## Commands

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
uv sync --group dev
uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000

# Backend tests
cd backend
uv run pytest -q
```

- Frontend: `http://127.0.0.1:5173`
- Backend: `http://127.0.0.1:8000` · docs at `/docs`
- FE → BE base URL: `http://127.0.0.1:8000` (override with `VITE_API_BASE_URL`)
- DB: SQLite at `backend/data/app.db` by default; override with `DATABASE_URL` (Postgres-ready)

## Homework answers (draft)

Paste-ready answers and verification notes: [`AIDT_02_HW.md`](AIDT_02_HW.md)  
(Module 01 style: `AIDT/01/AIDT_HW_chores/AIDT_01_HW.md`)

| Q | Answer |
|---|--------|
| 1 Project | Mini Kanban board |
| 2 App name | LaneDeck |
| 3 Spec commit SHA | `cf878545446c6ab67ee7a4ccbfe61edcccaa6579` |
| 4 FE start command | `npm run dev` (from `frontend/`) |
| 5 BE start command | `uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000` (from `backend/`) |
| 6 FE → BE URL | `http://127.0.0.1:8000` |
| 7 Test command | `uv run pytest -q` (from `backend/`) |


## Course

- Homework: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/02-development/homework.md
- Submit: https://courses.datatalks.club/ai-dev-tools-2026/homework/hw2
