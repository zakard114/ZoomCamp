# Agent notes — Agent Relay (AIDT HW 03)

## Stack (expected)

- App: course **Agent Relay** starter (API + dashboard + workers)
- DB: SQLite first → PostgreSQL via Compose / kind
- Local K8s: **kind** + kubectl
- CI locally: **act** + `.github/workflows/ci.yml`

## Paths (Windows)

- Workspace: `E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay\`
- Caches: E: only — `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1` before uv/npm/docker
- Never put venv, caches, or images under `C:\Users\...`

## Workflow

1. Follow `_docs/guides/packets/` in order — one packet at a time
2. Prefer course `SPEC.md` / homework.md over improvising features
3. Starter: https://github.com/alexeygrigorev/agent-relay
4. Commit in small steps; no `Co-authored-by` / Cursor attribution

## Scope guard

HW3: containerize, Compose+Postgres, kind deploy, local CI with act. No AWS.
HW4: local OpenTelemetry + Docker telemetry stack in `observability/`. Do not Create stack.
