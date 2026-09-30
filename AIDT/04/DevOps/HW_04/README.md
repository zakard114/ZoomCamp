# Order Tracker — AIDT Homework 4

Local write-up and packets for
[AI Dev Tools Zoomcamp 2026 — Homework 4: DevOps and Observability](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md)
(Order Tracker: run → instrument → telemetry → alert → responder → express fix).

## Official materials

- Course text (do not edit): [`materials/homework.md`](materials/homework.md)
- Form answers: [`AIDT_04_HW.md`](AIDT_04_HW.md)
- Starter fork: https://github.com/alexeygrigorev/order-tracker
- App clone: `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\`

## Local run

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
docker compose up --build -d
curl.exe http://127.0.0.1:8000/healthz
# after observability stack: Grafana http://127.0.0.1:3000
```

## Submission

- **Form (open in browser):** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4
- **Repository URL (paste into the form):** https://github.com/zakard114/order-tracker
- **Write-up on ZoomCamp:** https://github.com/zakard114/ZoomCamp/tree/main/AIDT/04/DevOps/HW_04
