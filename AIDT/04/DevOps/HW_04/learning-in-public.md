# Learning in public — Module 04 (LinkedIn draft)

Copy-paste ready. Style matched to Module 03 post.

---

🚀 AI Dev Tools Zoomcamp 2026 - Module 4 Complete

Wrapped Module 4 of AI Dev Tools Zoomcamp by DataTalksClub (Alexey Grigorev's build-and-ship track). The lesson moved from “it runs on my laptop” into observability: metrics, logs, and traces you can actually query when something breaks. For the assignment I forked Order Tracker and walked the full loop — instrument lookups, ship telemetry through a local Collector stack, alert on user-visible 5xx, wire an automatic responder, then fix a real calendar-edge bug the agent surfaced.

🛠️ What I Built & Learned

Lesson
✅ Thought about delivery as operate + observe, not only build + deploy
✅ Separated signals: metrics for rates/errors, logs for detail, traces for request paths
✅ Stood up a local telemetry path (OpenTelemetry → Collector → Prometheus / Loki / Tempo → Grafana) instead of staring at container logs alone
✅ Practiced alert design around user impact (failed lookups), not every noisy status code
✅ Kept incident response gated: collect evidence first, then decide whether a coding agent may change code

Assignment
✅ Ran Order Tracker with Compose and confirmed `/healthz` → `{"status":"ok"}`
✅ Instrumented order lookups with OpenTelemetry so `standard-1001` records HTTP 200 on the metric
✅ Piped telemetry into Grafana — `standard-1002` (missing order) shows as 404 in the dashboard
✅ Confirmed a 5xx alert stays **Normal** when the failure is only 404 (not a server error)
✅ Triggered the automatic responder (ResponderTest) and captured the standing-down last line
✅ Reproduced `express-1002` 500s from invalid `datetime.replace(day=…)`, fixed with `timedelta(days=2)`, rebuilt, and got a clean 200 + delivery date

💡 Key Engineering Insight
A green health check is not the same as knowing why users fail. Instrumentation plus a small Grafana stack turns “it returned 500” into a route, a status code, and a code path you can fix — and a 404 should not page you like a 5xx. Also: calendar math with `replace(day=…)` is a month-boundary landmine; add days with `timedelta`.

Following along with this amazing course - who else is building with AI coding agents? You can sign up here: https://lnkd.in/gsdZGWE3

#DataTalksClub #LearningInPublic #AIDevTools #OpenTelemetry #Observability #Grafana #Prometheus #Docker #IncidentResponse #Zoomcamp

---

**Repo to share:** https://github.com/zakard114/order-tracker  
**Write-up:** ZoomCamp → AIDT → 04 → DevOps → HW_04 → `AIDT_04_HW.md`
