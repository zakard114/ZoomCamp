# Order Tracker — AIDT Homework 4

Write-up folder for
[AI Dev Tools Zoomcamp 2026 — Homework 4](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md)
(Order Tracker: run → instrument → telemetry → alert → responder → express fix).

## Form answers

[`AIDT_04_HW.md`](AIDT_04_HW.md)

## Local run

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
docker compose up --build -d
curl.exe http://127.0.0.1:8000/healthz
```

- Health: http://127.0.0.1:8000/healthz  
- Grafana: http://127.0.0.1:3000  

## Submission

- **Form (open in browser):** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4
- **Repository URL (paste into the form):** https://github.com/zakard114/order-tracker
