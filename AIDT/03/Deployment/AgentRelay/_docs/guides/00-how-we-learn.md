# How we learn HW3 (you + Cursor + Gemini)

Same pattern as Module 02 guides: **Cursor = structure & truth**, **you = run & decide**, **Gemini = Korean narration**.

## Rules

1. **One packet at a time.** Finish → note → permission → next.
2. **Materials first.** Prefer `../../materials/homework.md` and starter `SPEC.md`. Starter fork: https://github.com/alexeygrigorev/agent-relay
3. **You participate.** Click dashboard, run commands, pick MCQ answers yourself.
4. **E: drive only** for installs/caches: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`
5. **No AWS** for this homework (kind is local).

## Flow per packet

```text
packet (Cursor) → you follow steps → coding agent prompts if needed
       ↓
wrapper + packet → Gemini → Korean narrative
       ↓
save to _docs/notes/0N-....md → fill AIDT_03_HW.md row
```

## Packet map

| # | File | Homework |
|---|------|----------|
| 01 | `packets/01-understand-project.md` | Q1 |
| 02 | `packets/02-register-and-test.md` | Q2 |
| 03 | `packets/03-dockerfile.md` | Q3 |
| 04 | `packets/04-compose-postgres.md` | Q4 |
| 05 | `packets/05-kind-k8s.md` | Q5 |
| 06 | `packets/06-cicd-act.md` | Q6 |

Gemini wrapper: [`gemini-prompt-wrapper.md`](gemini-prompt-wrapper.md)
