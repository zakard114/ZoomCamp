# Plan — Shared Household Chores

## Vague starting idea

> A tool for managing shared household chores

## Homework scope decisions

Scoped for a short Django homework (not a full product).  
Assumptions made so the app stays small and shippable:

- One household (no multi-tenant orgs).
- Members are simple names (no full auth/invite system in v1).
- Web UI only (no mobile app / notifications).
- SQLite is enough for local demo.

## Core features (2–4) — form Q2 answers

1. **Chore CRUD** — Create, list, edit, and delete chore items (title + optional notes/due date).
2. **Assignee** — Assign each chore to a household member (who is responsible).
3. **Completion toggle** — Mark a chore done / not done and see status in the list.

Out of scope for this homework (explicitly deferred):

- Push/email reminders
- Points / gamification
- Recurring calendar schedules with RRULE
- Real-time multi-user sync
- Payments / grocery shopping lists

## How it should work (short)

1. Add household members (minimal: name only).
2. Add chores and optionally set a due date.
3. Assign a member to a chore.
4. When finished, toggle completion; reopen if needed.

## Stack

- Python + Django + `uv`
- Coding agent: Cursor

## Next step

Break this plan into a small Django backlog → `_docs/backlog.md`.
