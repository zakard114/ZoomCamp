# LaneDeck — Product Spec

**Homework:** AI Dev Tools Zoomcamp 2026 — Homework 2  
**Project idea:** Mini Kanban board  
**App name:** **LaneDeck**

A small personal Kanban board: create cards, move them across lanes (Todo → Doing → Done), edit titles, and delete cards. Built with an AI coding agent following: spec → frontend (mocked API) → OpenAPI → FastAPI → connect → SQLite.

---

## 1. Problem

People need a lightweight way to track a handful of tasks visually without setting up a full project tool (Jira, Trello accounts, etc.). LaneDeck is a single-board Kanban that runs locally (and later can be deployed) with a clear frontend/backend contract.

## 2. Goals

- One board with three fixed lanes: **Todo**, **Doing**, **Done**
- Create, rename, delete cards
- Move a card to another lane (status change)
- Persist cards in a database so data survives backend restart
- Keep the stack familiar for the course: React (Vite) + FastAPI + SQLite (SQLAlchemy)

## 3. Non-goals (v1)

- Multiple boards / workspaces
- User accounts / auth
- Drag-and-drop polish (click/menu move is enough for v1)
- Comments, assignees, due dates, attachments
- Realtime multiplayer (nice-to-have later; not required for homework core)
- Mobile-first redesign

## 4. Users & stories

**Primary user:** A solo learner / developer tracking a few tasks.

| ID | Story | Acceptance |
|----|--------|------------|
| US1 | As a user, I open the app and see three lanes with any existing cards. | Board loads; empty lanes show a short empty state. |
| US2 | As a user, I create a card with a title in Todo. | Card appears in Todo with the given title. |
| US3 | As a user, I rename a card. | Updated title is visible immediately and after refresh. |
| US4 | As a user, I move a card to Doing or Done. | Card leaves the old lane and appears in the new one. |
| US5 | As a user, I delete a card. | Card is gone from the board and after refresh. |
| US6 | As a user, I restart the backend and reopen the app. | Cards and lanes are unchanged (persistence). |

## 5. Domain model

### Board (implicit)

v1 has a single implicit board. No board entity required in the API.

### Card

| Field | Type | Notes |
|-------|------|--------|
| `id` | string (uuid) | Primary key |
| `title` | string | Required, trimmed, 1–200 chars |
| `lane` | enum | `todo` \| `doing` \| `done` |
| `position` | number | Order within a lane (integer, ascending) |
| `createdAt` | ISO-8601 datetime | Set on create |
| `updatedAt` | ISO-8601 datetime | Set on create/update |

## 6. UI (frontend)

### Layout

- Header: app name **LaneDeck** + short subtitle
- Main: three columns (Todo / Doing / Done)
- Each column: title, count, “Add card” (Todo only or all lanes — prefer **Add on every lane** for simplicity), list of cards
- Card: title, actions (Edit, Move…, Delete)

### Interactions

- **Add card:** prompt or inline field for title → create in that lane (default Todo if only one button)
- **Edit:** inline or small dialog; save updates title
- **Move:** choose target lane (buttons or select)
- **Delete:** confirm once, then remove

### States

- Loading board
- Empty lane copy (“No cards yet”)
- Error toast / banner if API fails

## 7. API sketch (to become `openapi.yaml`)

Base URL (local): `http://127.0.0.1:8000`

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Liveness |
| `GET` | `/api/cards` | List all cards (optionally `?lane=todo`) |
| `POST` | `/api/cards` | Create card `{ title, lane? }` |
| `PATCH` | `/api/cards/{id}` | Update `{ title?, lane?, position? }` |
| `DELETE` | `/api/cards/{id}` | Delete card |

Frontend must centralize all backend calls in one service layer. First implementation: **mock in-memory / localStorage**. Later: real HTTP client against FastAPI.

## 8. Tech stack

| Layer | Choice |
|-------|--------|
| Frontend | React + Vite + TypeScript (Node.js) |
| Backend | FastAPI + `uv` |
| Contract | `openapi.yaml` derived from the FE service |
| Persistence | SQLAlchemy + SQLite by default; `DATABASE_URL` override for Postgres later |
| Tests | Backend `pytest`; FE unit/smoke as needed |

## 9. Build sequence (homework alignment)

1. Spec (this file) + repo scaffolding — **done in foundation commit**
2. `frontend/` prototype with mocked service
3. `openapi.yaml` from FE expectations
4. `backend/` FastAPI with mock store + tests
5. Wire FE → HTTP API
6. Replace mock store with SQLite (SQLAlchemy), keep tests green

## 10. Success criteria

- [ ] README can start FE and BE locally
- [ ] Main flows US1–US5 work in the UI
- [ ] US6 persistence verified after backend restart
- [ ] Backend tests pass (`uv run pytest` or documented equivalent)
- [ ] Code on GitHub for homework submission

## 11. Open questions (resolved for v1)

| Question | Decision |
|----------|----------|
| Multiple boards? | No |
| Auth? | No |
| DnD? | Optional later; move via controls in v1 |
| Card description field? | No — title only |
