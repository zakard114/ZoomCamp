# AI Dev Tools Zoomcamp 2026 — Homework 1: Django TODO

Submission write-up for **Module 01 — Introduction to AI-Assisted Development** (Django TODO app).

**Course:** [AI Dev Tools Zoomcamp](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/01-overview/homework.md)  
**Submit:** https://courses.datatalks.club/ai-dev-tools-2025/homework/hw1  
**Code folder (this repo):** [`AIDT/01/AI_Native_Developer_Workflow/AIDT_HW_01/`](./)  
**GitHub folder URL (after push):** https://github.com/zakard114/ZoomCamp/tree/main/AIDT/01/AI_Native_Developer_Workflow/AIDT_HW_01

---

## Homework form answers

Official quiz answers (corrected against the 2026 `homework.md`, not Gemini paraphrases).

| # | Form choice |
|---|-------------|
| 1 | **`uv pip install django`** |
| 2 | **`settings.py`** |
| 3 | **Run migrations** |
| 4 | **`views.py`** |
| 5 | **`TEMPLATES['DIRS']` in project's `settings.py`** |
| 6 | **`python manage.py test`** |

---

## Setup (local — E: drive)

Shared AIDT venv + E: caches (do not use C: for caches).

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AI_Native_Developer_Workflow\AIDT_HW_01
```

- **Work dir:** `...\AIDT_HW_01`
- **Venv:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv`
- **AI tool:** Cursor (agent mode) + Gemini tutoring (one question at a time)

---

## Q1 — Install Django

```powershell
uv pip install django --python E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe
```

**Result:** Django **6.1** installed into the AIDT `.venv` on E:.

**Answer (form):** **`uv pip install django`**

---

## Q2 — Project and App

```powershell
python -m django startproject config .
python manage.py startapp todos
```

Registered `"todos"` in `config/settings.py` → `INSTALLED_APPS`.  
Verified with `python manage.py check` (0 issues).

**Answer:** **`settings.py`**

---

## Q3 — Django Models

Implemented `Todo` in `todos/models.py`:

- `title` — `CharField`
- `due_date` — `DateField` (optional)
- `resolved` — `BooleanField(default=False)`

```powershell
python manage.py makemigrations todos
python manage.py migrate
```

**Answer:** **Run migrations**  
(Editing `models.py` is required for implementation; the quiz asks for the **next** step after defining models.)

Also registered the model in `todos/admin.py` (useful, but not the Q3 form choice).

---

## Q4 — TODO Logic

Implemented CRUD + resolve toggle in `todos/views.py`, with:

- `todos/forms.py` — `TodoForm`
- `todos/urls.py` + include from `config/urls.py`

**Answer:** **`views.py`**

---

## Q5 — Templates

Created project-level templates (as required by the homework):

- `templates/base.html`
- `templates/home.html` (list / create / edit / delete / toggle)

Registered in `config/settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        ...
    },
]
```

Also set `ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]` for local + tests.

**Answer:** **`TEMPLATES['DIRS']` in project's `settings.py`**

### Browser check

```powershell
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py runserver 8001
```

Open: http://127.0.0.1:8001/  
(Port `8000` may be used by retroloop.)

---

## Q6 — Tests

Scenarios covered in `todos/tests.py` (7 tests):

- model `__str__` / default `resolved`
- home lists todos
- create with due date
- edit / delete / toggle resolved

```text
$ python manage.py test
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 0.138s

OK
Destroying test database for alias 'default'...
```

**Answer:** **`python manage.py test`**  
(`runserver` is the separate “Running the app” section, not Q6.)

---

## App requirements checklist

| Requirement | Status |
|-------------|--------|
| Create / read / update / delete TODOs | Done |
| Assign due dates | Done (`due_date`) |
| Mark TODOs as resolved | Done (`resolved` + toggle) |
| Tests pass | Done (7/7 OK) |
| `runserver` works | Done (`:8001`) |

---

## Submission notes

1. Push this folder to GitHub (repo already: `zakard114/ZoomCamp`).
2. Paste the **folder URL** into the homework form (example above).
3. Enter Q1–Q6 answers from the table at the top.

If the course prefers a folder literally named `01-todo`, rename/copy this project under that name before submitting, or keep `AIDT_HW_01` and use that path as the folder link.
