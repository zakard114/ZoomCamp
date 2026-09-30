# Operations and security report

Incident ID: **INC-20260925-001**

The model may reason; the system must observe, authorize, verify, and remember.

## Deployed version and user impact

- Service: `agent-relay`
- Environment: `dev`
- Deployed version: `hw4-local`
- User impact: `POST /api/v1/agents` returned **500**. New operators could not register an agent, so they could not send or receive tasks.

## Alert and evidence

Alert `AgentRegistrationFailures` in `observability/alerts.yaml`:

- Condition: `increase(agent_relay_http_errors_total{endpoint="/api/v1/agents",status="500"}[2m]) > 0`
- Not CPU. Payload labels: service, environment, owner, dashboard URL, runbook.

Evidence packet: `incident-response/evidence/INC-20260925-001.json`  
Queries used: allowlisted `/health`, Prometheus `up` / error counters, and registration **status codes only** (bodies dropped so tokens never enter the packet).

Local telemetry pipeline (Docker, already up from the Module 4 collector on :4317/:4318/:9090/:3000/:3100/:3200): OpenTelemetry Collector → Prometheus, Loki, Tempo → Grafana. Repo copy: `observability/compose.yaml`. **No AWS Create stack.**

## Model / configuration and proposed action

- Agent: Cursor coding agent, read-only evidence + `incident-response/responder-task.md`
- Output schema: `incident-response/response.schema.json`
- Response: `incident-response/last-response.json`
- Proposed action: run allowlisted `incident-response/runbooks/disable-inject.ps1`

## Policy decision and command executed

Authorized by `incident-response/autonomy-policy.yaml` (not model confidence, not alert severity).

Command executed: delete `observability/.inject-register-failure` (same effect as `disable-inject.ps1`).

## Recovery verification or escalation

After the flag was removed, `POST /api/v1/agents` returned **201** again (verified in `test_hw4_inject.py`; live uvicorn on this Windows session failed to bind in time). Escalation was not required.

## Security finding and disposition

- Scanner: Semgrep paired with model review (`security-audit/`)
- Finding: inject flag is a local homework fault. Keep it off by default.
- Tokens: not logged, not stored in evidence.
- Responder credentials: see `security-audit/capability-table.md`
