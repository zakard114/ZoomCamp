# AI Dev Tools Zoomcamp 2026 — Homework 4: DevOps and Observability

Submission write-up for **official** Module 04 homework (Order Tracker).  
(run app → instrument lookups → telemetry pipeline → 5xx alert → responder → express incident).

**Course:** [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md)  
**Submit form:** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw4  
**Deadline:** 6 October 2026, 09:00 (account timezone)

**Starter:** https://github.com/alexeygrigorev/order-tracker  
**Local app:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\`  
**Working:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\`

**Homework URL (paste into form after push):** https://github.com/zakard114/order-tracker

Style reference: `AIDT_01_HW.md` / `AIDT_02_HW.md` / `AIDT_03_HW.md`

The earlier Agent Relay draft answers are **not** used here.

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | `{"status":"ok"}` |
| 2 | `200` |
| 3 | `404` |
| 4 | `Normal` |
| 5 | Last line: `Test alert handled successfully; standing down.` (full text in Q5 section) |
| 6 | The express delivery date calculation tried to use a day that does not exist in that month. |

**Homework URL (repo):** https://github.com/zakard114/order-tracker

---

## Q1 — Run the app

What does the health check return?

**Answer:** `{"status":"ok"}`

Evidence: `curl.exe http://127.0.0.1:8000/healthz` → exact body `{"status":"ok"}`.

---

## Q2 — Instrument one endpoint

Which HTTP status code does the metric record for `standard-1001`?

**Answer:** `200`

Evidence: `curl` → HTTP 200 + order JSON; `docker compose logs app` → metric `order_lookup_requests` with `route=/api/orders/{order_id}`, `http.status_code=200`.

---

## Q3 — Telemetry pipeline / Grafana

Which HTTP status code does the metric show for `standard-1002`?

**Answer:** `404`

Evidence: `curl` → HTTP 404 `Order not found`; Prometheus/Grafana metric `order_lookup_requests_total` with `route=/api/orders/{order_id}`, `http_status_code=404`. Dashboard: **Order Tracker — request counts & errors** (`http://127.0.0.1:3000/d/order-tracker-requests`).

---

## Q4 — 5xx alert state

What state does Grafana show?

**Answer:** `Normal`

Evidence: after `curl` `standard-1002` (404, not 5xx), Grafana rule `Order lookup 5xx responses` → alert state **Normal** (health ok). Alerting → Alert rules.

---

## Q5 — Agent responder last line

What did the agent respond? Include the last line.

**Answer (from `incident-response/responses/last-response.txt`, INC-20260930-f7f9addf):**

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

**Last line:** `Test alert handled successfully; standing down.`

---

## Q6 — What was the problem?

**Answer:** The express delivery date calculation tried to use a day that does not exist in that month.

Evidence: `express-1002` → HTTP 500; `order_detail` used `placed_at.replace(day=placed_at.day + 2)` (invalid near month end, e.g. 2026-08-31). Headless fix → `placed_at + timedelta(days=2)`; app rebuild → HTTP 200 + `estimated_delivery`.

---
