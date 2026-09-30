# Agent notes — AIDT HW 04 (official Order Tracker)

## Scope

- Working: `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\`
- App: `E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\` (fork of alexeygrigorev/order-tracker)
- Official text: `materials/homework.md` (untouched after sync)
- Draft Agent Relay HW4 is void for the form

## Workflow

1. One packet at a time (`_docs/guides/packets/`)
2. Gemini = Korean beginner narration from the packet
3. Cursor = packet + 타당성 점검 + code when asked
4. Learner = fork, compose, curl, Grafana clicks, form answers
5. E: caches only. No AWS Create stack

## Homework loop (this official set)

Run app → instrument lookups → Collector/Prom/Loki/Tempo/Grafana → 5xx alert → responder on :8001 → webhook + express-1002 fix
