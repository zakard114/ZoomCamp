# Security audit brief

Pair Semgrep (deterministic) with model review, then human validation.

Scan root: Agent Relay (this repo). Do not send secrets to the model.

Rules of review:
- Flag leaked tokens, `Authorization` in logs, hardcoded secrets.
- The inject flag is a local homework fault — not a production backdoor to keep.
- Responder stays read-only except allowlisted runbooks.
