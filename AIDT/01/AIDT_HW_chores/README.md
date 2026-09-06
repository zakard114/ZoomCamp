# Household Chores — AIDT Homework 1

A small Django app for **managing shared household chores**, built for
[AI Dev Tools Zoomcamp 2026 — Homework 1](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/01-ai-native-workflow/homework.md).

## Idea → spec → backlog

Vague idea: *a tool for managing shared household chores*.

- Plan: [`_docs/plan.md`](_docs/plan.md)
- Backlog: [`_docs/backlog.md`](_docs/backlog.md)
- Form answers: [`AIDT_01_HW.md`](AIDT_01_HW.md)

## Features

1. Chore CRUD
2. Assignee (household members)
3. Completion toggle

## Coding agent

**Cursor**

## Local run

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AIDT_HW_chores
uv run python manage.py migrate
uv run python manage.py runserver
uv run python manage.py test
```

If `uv` hangs on this machine, use the shared AIDT venv:

```powershell
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py runserver
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py test
```

## Submission

https://courses.datatalks.club/ai-dev-tools-2026/homework/hw1
