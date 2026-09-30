# AI Dev Tools Zoomcamp 2026 — Homework 3: Deploy Agent Relay

Submission write-up for Module 03 homework  
(local run → Docker → Compose+Postgres → kind → local CI with act).

**Course:** [AI Dev Tools Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/03-deployment/homework.md)  
**Submit form (browser only, not a form answer):** https://courses.datatalks.club/ai-dev-tools-2026/homework/hw3  

**Local project:** `E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay\`  
**Homework URL (paste into form):** https://github.com/zakard114/agent-relay

Style reference (Modules 01–02): `AIDT_01_HW.md` / `AIDT_02_HW.md`

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | **Agents claim tasks from a DB through an HTTP API.** |
| 2 | **`completed`** |
| 3 | **`-p`** |
| 4 | **`postgres`** |
| 5 | **`Deployment`** |
| 6 | **Keep the existing version running and stop the deployment.** |

**Homework URL (repo):** https://github.com/zakard114/agent-relay

---

## Q1 — Understand the project (architecture)

Which description matches the project's architecture?

```text
Agents claim tasks from a DB through an HTTP API.
```

Evidence: local run at `http://127.0.0.1:8000/`, README / `storage.py` / `database.py`.  
Tasks and attempts live in SQLite (later Postgres). Agents use Bearer HTTP to register, claim, and complete. No message broker, no P2P, browser is dashboard-only.

---

## Q2 — Sender status after recipient result

After the recipient posts a result, which status does the sender see?

```text
completed
```

Evidence: live PowerShell scenario (alice → bob claim/complete) +  
`test_sender_sees_completed_after_recipient_result`.  
Sender `GET /api/v1/tasks/{id}` returns `status: completed` (not `delivered` / `queued` / `processing`).

Lifecycle observed: `queued` → `processing` → `completed`.

---

## Q3 — Containerization (publish port)

Which Docker option publishes the container port on the host?

```text
-p
```

Evidence: `Dockerfile` (uvicorn `--host 0.0.0.0 --port 8000`) +  
`docker run -p 8000:8000 agent-relay:local`.  
`--expose` documents only; `-v` is volumes; `--name` is container name.

---

## Q4 — Docker Compose DB hostname

Which hostname should the API use to reach the Postgres service in Compose?

```text
postgres
```

Evidence: `compose.yaml` — service name `postgres`,  
`RELAY_DATABASE_URL=postgresql+psycopg://relay:relay@postgres:5432/relay`.  
Inside the Compose network, service DNS is the hostname (not `localhost`).  
Verified with `/health` and  
`docker compose exec postgres psql ... SELECT id, status FROM tasks ...` → `completed`.

---

## Q5 — Kubernetes replica resource

Which resource keeps the requested number of replicas running and manages updates?

```text
Deployment
```

Evidence: `k8s/api.yaml`, `k8s/postgres.yaml` (Deployments + Services + Secret + readiness).  
kind cluster `agent-relay` via `k8s/kind-config.yaml` (E: pgdata extraMount).  
`kubectl port-forward svc/agent-relay 8000:8000` → `/health` ok.

---

## Q6 — CI/CD if tests fail

What should happen if a test fails in this workflow?

```text
Keep the existing version running and stop the deployment.
```

Evidence: `.github/workflows/ci.yml` — `build-and-deploy` has `needs: test`.  
Local runner: `scripts/run-act-ci.ps1` (act + host fallback) — failed tests skip kind deploy.  
Dashboard heading updated to **Agent Relay v2**; CI rebuilt/loaded unique tag  
`agent-relay:ci-local-20260920195051`; port-forward shows `<h1>Agent Relay v2</h1>`.

---

## Verification log

Environment: Windows, caches on `E:\IT_SPACES\AI\.cache\` via  
`. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`.  
Tools: Docker Desktop, `kind` / `act` under `E:\IT_SPACES\AI\.cache\bin\`.

| Check | Result |
|-------|--------|
| Local /health | `{"status":"ok"}` |
| Q2 task flow (API + dashboard) | sender sees `completed` |
| Docker image `agent-relay:local` | build + `-p 8000:8000` OK |
| Compose + Postgres | api + postgres up; tasks in Postgres |
| kind deploy | pods Ready; port-forward OK |
| Local CI (`run-act-ci.ps1`) | `CI local OK`; image tag `ci-local-20260920195051` |
| Dashboard v2 | served HTML `<h1>Agent Relay v2</h1>` |

Artifacts:

| Path | Role |
|------|------|
| `Dockerfile` | App image |
| `compose.yaml` | api + postgres (E: `docker/pgdata/data`) |
| `k8s/*.yaml` | kind manifests |
| `.github/workflows/ci.yml` | test → build → kind deploy |
| `scripts/run-act-ci.ps1` | Windows local CI entry |

---

## How to run locally

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
$env:Path = "E:\IT_SPACES\AI\.cache\bin;C:\Program Files\Docker\Docker\resources\bin;$env:Path"

# Compose (Packet 04)
docker compose up --build -d
# http://127.0.0.1:8000/health

# kind (Packet 05) — after compose down if port 8000 conflicts
# kind create cluster --config k8s/kind-config.yaml
# docker build -t agent-relay:local .
# kind load docker-image agent-relay:local --name agent-relay
# kubectl apply -f k8s/postgres.yaml -f k8s/api.yaml
# kubectl port-forward svc/agent-relay 8000:8000

# Local CI (Packet 06)
.\scripts\run-act-ci.ps1
# or: .\scripts\run-act-ci.ps1 -HostTest
```

- Dashboard: http://127.0.0.1:8000/  
- Health: http://127.0.0.1:8000/health  

---

## Reflection

One practical takeaway from this module: **inside Compose/Kubernetes, the hostname is the service name (`postgres`), not `localhost`** — and CI should refuse to deploy when tests fail so the last good Deployment keeps serving traffic.

---

## Learning in public

- Link: _(add LinkedIn / blog URL after posting)_  
- Repo to share: https://github.com/zakard114/agent-relay  

Optional post outline (no secrets): fork → Docker `-p` → Compose hostname `postgres` → kind `Deployment` → act CI stops deploy on test failure → dashboard **Agent Relay v2** rollout.
