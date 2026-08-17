# AIDT Module 01 — AI-Native Developer Workflow

Main workspace for the **AI Dev Tools Zoomcamp 2026** Module 1.

## Contents

| Path | Source | Notes |
|------|--------|-------|
| [`materials/`](materials/) | [01-ai-native-workflow](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/tree/main/01-ai-native-workflow) | Upstream snapshot / reference |
| [`AI_Native_Developer_Workflow/weekly-feedback/`](AI_Native_Developer_Workflow/weekly-feedback/) | course example | Vague-prompt CLI example |
| [`AI_Native_Developer_Workflow/retroloop/`](AI_Native_Developer_Workflow/retroloop/) | [alexeygrigorev/retroloop](https://github.com/alexeygrigorev/retroloop) | Spec-driven Django example |
| [`AI_Native_Developer_Workflow/AIDT_HW_01/`](AI_Native_Developer_Workflow/AIDT_HW_01/) | homework | Django TODO app (uv + Cursor) |

Local notes (optional): `E:\IT_SPACES\AI\zoomcamp_misc\ADT\01\AIDT_HW_01.txt`

## Homework

Official homework: [cohorts/2026/01-overview/homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/01-overview/homework.md)  
Submit form (course): https://courses.datatalks.club/ai-dev-tools-2025/homework/hw1  
Answers write-up: [`AI_Native_Developer_Workflow/AIDT_HW_01/AIDT_01_HW.md`](AI_Native_Developer_Workflow/AIDT_HW_01/AIDT_01_HW.md)

### Local run (Windows / E:)

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\01\AI_Native_Developer_Workflow\AIDT_HW_01
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py test
E:\IT_SPACES\AI\ZoomCamp\AIDT\.venv\Scripts\python.exe manage.py runserver 8001
```

Browser: http://127.0.0.1:8001/
