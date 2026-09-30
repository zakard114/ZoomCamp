# Responder capability table

| Capability | Allowed | How enforced |
|---|---|---|
| Read /health, /ready | yes | autonomy-policy.yaml queries |
| Read Prometheus query/rules | yes | allowlisted GETs |
| Read last 5 git commits | yes | `git log -5` |
| Propose one action (JSON) | yes | response.schema.json |
| Use production admin credentials | no | not provided |
| Write to SQLite / change code | no | default_level: read_only |
| Disable inject flag | only if human runs allowlisted runbook | disable-inject.ps1 |
| AWS / cloud credentials | no | none on disk for this homework |

## Credentials inventory

| Item | Present | Notes |
|---|---|---|
| Agent registration tokens | runtime only | returned once by API; not logged |
| RELAY_ENROLLMENT_SECRET | optional env | not set for this incident |
| Grafana admin/admin | local Docker | localhost bind :3000 |
| AWS keys | no | stack not created for HW4 |
| Responder model API key | operator machine only | not in repo |
