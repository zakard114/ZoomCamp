---
name: ml-zoomcamp-hw-setup
description: >-
  Compare a completed ML Zoomcamp module against the 2026 cohort and scaffold
  homework in the HW_01/HW_02 folder format. Use when the user asks to check
  module N lessons vs cohorts/2026, set up HW_0N, or mentions homework.md,
  course_lead_scoring, car_fuel_efficiency, nbclassic, or ml-zoomcamp-2026 homework.
---

# ML Zoomcamp 2026 homework setup

## Paths

Root: `E:/IT_SPACES/AI/ZoomCamp/ML/`

| Kind | Path |
|------|------|
| Lessons (working) | `0N/<name>/` (notebook) |
| Lesson materials (do not edit) | `0N/<name>/materials/` or `0N/materials/` |
| Homework | `0N/HW_0N/` |
| Shared venv | `ML/.venv` — junction only, never a new venv |
| Cache | `E:/IT_SPACES/AI/.cache/` after `use_e_drive.ps1` |

Never C: pip/uv/wget/jupyter. Never `!pip` / `!wget` in notebooks.

## Compare first

1. Local lesson `.md` vs GitHub `03-classification`-style evergreen folder (`https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/main/0N-<name>`).
2. Local `homework.md` (often a 2021–2025 stub) vs `cohorts/2026/homework/0N-<name>/homework.md`.
3. Expanded unit writeups + new images ≠ new syllabus. Same 3.1–3.14 (etc.) titles and videos → do **not** rewrite the lesson notebook.
4. If only homework changed (or was never done): scaffold `HW_0N`. Do not solve questions.

## Scaffold `0N/HW_0N/` like HW_02

Copy structure from `02/HW_02/`, not from lesson notebooks.

- `materials/homework.md` + `homework.yaml` — curl from `cohorts/2026/homework/...` (do not edit)
- `data/<pinned-2026.csv>` — curl to E: (`--max-time`; abort if >5 min)
- `[2026]_HW_0N.ipynb` — title, E: cache env, load local CSV, exact split/model snippets from homework.md, empty answer cells
- `ML_0N_HW.md` — form-answer table blank, Q sections, submit URL
- `run-nbclassic.ps1` / `run-nbclassic.sh` — HW_02 port/OMP/nbclassic pattern; **not** `jupyter notebook`
- `.venv` junction → `ML/.venv`
- gitignore `0N/HW_0N/data/` in `ML/.gitignore`

Download:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
curl.exe -L --fail --max-time 120 -o <E-path> <raw.githubusercontent.com URL>
```

Submit: `https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw0N`

## Do not

- Put ML Zoomcamp work under `Projects/`
- Independent `.venv` on C: or inside HW besides the junction
- Fill answers or pick nearby multiple-choice values
- Edit course `materials/` originals
- Start Docker/AWS/pipenv for homework unless that module’s 2026 homework requires it
