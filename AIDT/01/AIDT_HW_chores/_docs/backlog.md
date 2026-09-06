# Backlog — Shared Household Chores (Django)

Derived from [`plan.md`](plan.md). Small, ordered tasks for homework implementation.
Project skeleton (`config` + `chores` app registered in `settings.py`) is already done — start from models.

## Tasks

1. **Create Member and Chore models** — Add `Member` (name) and `Chore` (title, optional notes/due date, assignee FK, `is_done`) in `chores/models.py`, then `makemigrations` / `migrate`.
2. **Register models in Django admin** — Expose Member and Chore in `chores/admin.py` for quick data entry while views are unfinished.
3. **Chore list + create views** — List all chores and a simple form to create a new chore (title, notes, due date).
4. **Assignee on create/edit** — Wire Member choice into chore create/edit so each chore can be assigned.
5. **Completion toggle** — Add a done / not-done action on the list (POST or link) and show status clearly.
6. **Edit and delete chores** — Complete CRUD: update title/notes/due/assignee and delete a chore.
7. **Basic tests** — Cover model creation, list page, assignee, and completion toggle with `manage.py test`.

## Out of scope (from plan)

Reminders, gamification, recurring schedules, realtime sync, shopping lists.
