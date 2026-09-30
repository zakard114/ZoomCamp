# AI Dev Tools Zoomcamp 2026 — Homework 4: DevOps and Observability

Submission write-up for Module 04 homework  
(run app → instrument lookups → telemetry pipeline → 5xx alert → responder → express incident).

**Course:** [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md)  
**Submit form (browser only, not a form answer):** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4  

**Local project:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\`  
**Write-up folder:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\`  
**Homework URL (paste into form):** https://github.com/zakard114/order-tracker

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | **`{"status":"ok"}`** |
| 2 | **`200`** |
| 3 | **`404`** |
| 4 | **`Normal`** |
| 5 | **`Test alert handled successfully; standing down.`** (full agent text in Q5) |
| 6 | **The express delivery date calculation tried to use a day that does not exist in that month.** |

**Homework URL (repo):** https://github.com/zakard114/order-tracker

---

## Q1 — Run the app

What does the health check return?

```text
{"status":"ok"}
```

Evidence: `docker compose up --build -d` then  
`curl.exe http://127.0.0.1:8000/healthz` → exact body `{"status":"ok"}`.

---

## Q2 — Instrument one endpoint

Which HTTP status code does the metric record for `standard-1001`?

```text
200
```

Evidence: `curl.exe http://127.0.0.1:8000/api/orders/standard-1001` → HTTP 200 + order JSON;  
`docker compose logs app` → metric `order_lookup_requests` with  
`route=/api/orders/{order_id}`, `http.status_code=200`.

---

## Q3 — Telemetry pipeline / Grafana

Which HTTP status code does the metric show for `standard-1002`?

```text
404
```

Evidence: `curl` → HTTP 404 `Order not found`; Prometheus/Grafana metric  
`order_lookup_requests_total` with `route=/api/orders/{order_id}`,  
`http_status_code=404`. Dashboard: **Order Tracker — request counts & errors**  
(`http://127.0.0.1:3000/d/order-tracker-requests`).

---

## Q4 — 5xx alert state

What state does Grafana show?

```text
Normal
```

Evidence: after `curl` `standard-1002` (404, not 5xx), Grafana rule  
`Order lookup 5xx responses` → alert state **Normal** (health ok).  
Alerting → Alert rules.

---

## Q5 — Agent responder last line

What did the agent respond? Include the last line.

Full text from `incident-response/responses/last-response.txt`  
(`INC-20260930-f7f9addf`):

```text
Headless coding assistant acknowledgement (Order Tracker).
Incident id: INC-20260930-f7f9addf
Alertname: ResponderTest
Affected endpoint recorded: /api/orders/{order_id}
Summary: Test notification; no incident to fix
Evidence packet was saved under incident-response/evidence/.
Recent logs/traces/metrics were attached when telemetry was reachable.
This is a ResponderTest notification (test=true); no production incident to fix.
No code changes were applied.
Test alert handled successfully; standing down.
```

Last line (form answer):

```text
Test alert handled successfully; standing down.
```

---

## Q6 — What was the problem?

```text
The express delivery date calculation tried to use a day that does not exist in that month.
```

Evidence: `express-1002` → HTTP 500; `order_detail` used  
`placed_at.replace(day=placed_at.day + 2)` (invalid near month end, e.g. 2026-08-31).  
Headless fix → `placed_at + timedelta(days=2)`; app rebuild → HTTP 200 + `estimated_delivery`.

---

## Verification log

Environment: Windows, caches on `E:\IT_SPACES\AI\.cache\` via  
`. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.  
Tools: Docker Desktop; Grafana at `http://127.0.0.1:3000`; responder on `:8001`.

| Check | Result |
|-------|--------|
| `/healthz` | `{"status":"ok"}` |
| `standard-1001` metric | `http.status_code=200` |
| `standard-1002` metric | `http_status_code=404` |
| Grafana 5xx alert | state **Normal** |
| ResponderTest | last line standing down |
| `express-1002` after fix | HTTP 200 + delivery date |

Artifacts:

| Path | Role |
|------|------|
| `order-tracker/` (sibling) | Forked app + compose + OTel |
| `order-tracker/observability/` | Collector, Prom, Loki, Tempo, Grafana |
| `order-tracker/incident-response/` | Webhook server + evidence + headless |
| `_docs/guides/packets/` | Step packets for this write-up folder |

---

## How to run locally

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker

docker compose up --build -d
curl.exe http://127.0.0.1:8000/healthz
curl.exe http://127.0.0.1:8000/api/orders/standard-1001
curl.exe http://127.0.0.1:8000/api/orders/standard-1002

# Grafana (after observability is up)
# http://127.0.0.1:3000
```

- Health: http://127.0.0.1:8000/healthz  
- Grafana: http://127.0.0.1:3000  
- App fork: https://github.com/zakard114/order-tracker  

---

## Reflection

One practical takeaway: **a 404 does not fire a 5xx alert** — and calendar math with  
`datetime.replace(day=…)` breaks at month boundaries; add days with `timedelta` instead.

---

## Learning in public

- Link: _(add LinkedIn / blog URL after posting)_  
- Repo to share: https://github.com/zakard114/order-tracker  

Optional post outline (no secrets): fork Order Tracker → OTel metric on lookups →  
Collector → Grafana → 5xx alert stays Normal on 404 → responder standing-down line →  
express `timedelta` fix.
