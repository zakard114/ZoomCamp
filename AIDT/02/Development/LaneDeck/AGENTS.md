# Agent notes — LaneDeck (AIDT HW 02)

## Stack

- Frontend: React + Vite + TypeScript under `frontend/`
- Backend: FastAPI with **uv** under `backend/`
- Contract: `openapi.yaml` at repo root (after FE service exists)
- DB: SQLAlchemy; default SQLite; keep `DATABASE_URL`-override ready

## Paths (Windows)

- Workspace: `E:\IT_SPACES\AI\ZoomCamp\AIDT\02\Development\LaneDeck\`
- Caches / downloads: E: only — run `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1` before `uv` / `npm`
- Never put venv, caches, or model weights under `C:\Users\...`

## Workflow

1. Follow `_docs/specs.md` — do not invent large features outside the spec
2. Frontend first with a **central service** (`src/api/cardsApi.ts`); wire to HTTP after backend exists
3. Derive OpenAPI from the FE service layer
4. Backend: tests first where practical; mock store → SQLite
5. Commit in small steps; no `Co-authored-by` / Cursor attribution on commits

## Useful commands

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

# Frontend
cd frontend
npm run dev

# Backend
cd backend
uv sync --group dev
uv run uvicorn lanedeck_backend.main:create_app --factory --reload --host 127.0.0.1 --port 8000
uv run pytest -q
```

## Scope guard

v1: single board, three lanes, card title + lane + order. No auth, no multi-board, no comments.
