# How we learn official HW4 (you + Cursor + Gemini)

Same pattern as Module 02/03: **Cursor = structure & truth**, **you = run & decide**, **Gemini = Korean narration**.

## Rules

1. **One packet at a time.** Finish → note → permission → next.
2. **Materials first.** Official `materials/homework.md`. Starter: https://github.com/alexeygrigorev/order-tracker
3. **You participate.** Fork, `docker compose`, `curl`, Grafana, pick MCQ after you see it.
4. **E: only** for clone/caches: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`
5. **No AWS** for this homework.
6. Draft Agent Relay answers do **not** go on the form.

## Flow per packet

```text
packet (Cursor) → wrapper → Gemini Korean narrative
       ↓
you paste to Cursor for 타당성 점검
       ↓
you run the commands / click
       ↓
fill AIDT_04_HW.md
```

## Packet map

| # | File | Homework |
|---|------|----------|
| 01 | `packets/01-run-the-app.md` | Q1 |
| 02 | `packets/02-instrument-endpoint.md` | Q2 |
| 03 | `packets/03-telemetry-pipeline.md` | Q3 |
| 04 | `packets/04-configure-alert.md` | Q4 |
| 05 | `packets/05-automatic-responder.md` | Q5 |
| 06 | `packets/06-watch-agent-fix.md` | Q6 |

Gemini wrapper: [`gemini-prompt-wrapper.md`](gemini-prompt-wrapper.md)
