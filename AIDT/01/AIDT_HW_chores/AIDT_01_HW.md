# AI Dev Tools Zoomcamp 2026 — Homework 1: AI-Native Developer Workflow

Submission write-up for Module 01 homework  
(vague idea → spec → backlog → Django implementation).

**Course:** [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/01-ai-native-workflow/homework.md)  
**Submit:** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw1  

**Local project:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AIDT_HW_chores\`

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | **Cursor** |
| 2 | **1. Chore CRUD  2. Assignee  3. Completion toggle** |
| 3 | **`settings.py`** |
| 4 | **Create Member and Chore models** |
| 5 | **`uv run python manage.py runserver`** |
| 6 | **`uv run python manage.py test`** |

**Homework URL (repo):** use your GitHub clone URL for this folder after push (see Verification / Git below).

---

## Q1 — Which coding agent did you use?

```text
Cursor
```

---

## Q2 — What are the 2–4 features your spec settled on?

Saved in [`_docs/plan.md`](_docs/plan.md).

```text
1. Chore CRUD (create / list / edit / delete)
2. Assignee (assign a household member)
3. Completion toggle (done / not done)
```

---

## Q3 — Django project: which file registers the app?

`"chores"` is in `INSTALLED_APPS` in [`config/settings.py`](config/settings.py).

```text
settings.py
```

---

## Q4 — What is task 1 in the backlog?

From [`_docs/backlog.md`](_docs/backlog.md):

```text
Create Member and Chore models
```

---

## Q5 — Which command starts the Django development server?

```text
uv run python manage.py runserver
```

Fallback on this machine (shared AIDT venv, if local `uv` hangs):

```text
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py runserver
```

---

## Q6 — Which command runs tests?

```text
uv run python manage.py test
```

Fallback:

```text
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py test
```

---

## Verification log

Environment: Windows, caches on `E:\IT_SPACES\AI\.cache\` (`UV_CACHE_DIR` / `TEMP` / `TMP`).  
Interpreter used for verification: `E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe` (Django 6.1; avoids hung local `uv pip` / zipimport locale issues).

| Command | Result |
|---------|--------|
| `manage.py check` | System check identified no issues (0 silenced). exit 0 |
| `manage.py makemigrations chores` | Created `chores/migrations/0001_initial.py` (Member, Chore). exit 0 |
| `manage.py migrate` | Applied chores + Django system migrations. exit 0 |
| `manage.py test` | Found 6 test(s). Ran 6 tests. **OK**. exit 0 |

Implemented from backlog:

- Member / Chore models (assignee FK, optional due_date, `is_done`)
- Admin registration
- Chore list / create / edit / delete
- Member list / create
- Completion toggle (POST)
- Tests for models, list, create, assignee, toggle, edit/delete

---

## How to run locally

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AIDT_HW_chores
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
# preferred (course form):
uv run python manage.py runserver
uv run python manage.py test
# if uv hangs >90s, use shared AIDT venv instead:
# E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py runserver
# E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py test
```

Open http://127.0.0.1:8000/
