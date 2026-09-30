"""One-shot HW4 incident: break register, collect evidence, recover."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLAG = ROOT / "observability" / ".inject-register-failure"
EVIDENCE = ROOT / "incident-response" / "evidence"
INCIDENT = "INC-20260925-001"
PY = ROOT / ".venv" / "Scripts" / "python.exe"


def http_json(url: str, data: bytes | None = None, timeout: float = 5.0):
    req = urllib.request.Request(url, data=data, method="GET" if data is None else "POST")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return int(resp.status), body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return int(exc.code), body
    except Exception as exc:
        return None, str(exc)


def register(name: str) -> int | None:
    status, _body = http_json(
        "http://127.0.0.1:8000/api/v1/agents",
        data=json.dumps({"name": name}).encode(),
    )
    return status


def wait_health(tries: int = 40) -> bool:
    for _ in range(tries):
        status, _ = http_json("http://127.0.0.1:8000/health", timeout=2)
        if status == 200:
            return True
        time.sleep(1)
    return False


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["OTEL_ENABLED"] = "1"
    env["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://127.0.0.1:4318"
    env["OTEL_SERVICE_NAME"] = "agent-relay"
    env["APP_ENV"] = "dev"
    env["DEPLOYED_VERSION"] = "hw4-local"
    env.pop("OTEL_SDK_DISABLED", None)
    env["PYTHONUNBUFFERED"] = "1"

    log = (ROOT / "observability" / "uvicorn-hw4.err.log").open("ab")
    proc = subprocess.Popen(
        [str(PY), "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(ROOT),
        env=env,
        stdout=log,
        stderr=log,
    )
    try:
        if not wait_health():
            packet = {
                "incident_id": INCIDENT,
                "error": "uvicorn never became ready",
                "pid": proc.pid,
            }
            (EVIDENCE / f"{INCIDENT}.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")
            return 1

        FLAG.unlink(missing_ok=True)
        before = register("ok-hw4")
        FLAG.write_text("on\n", encoding="utf-8")
        fail1 = register("fail-hw4-a")
        fail2 = register("fail-hw4-b")
        time.sleep(18)
        prom_up = http_json("http://127.0.0.1:9090/api/v1/query?query=up")
        prom_err = http_json("http://127.0.0.1:9090/api/v1/query?query=agent_relay_http_errors_total")
        prom_reg = http_json("http://127.0.0.1:9090/api/v1/query?query=agent_relay_agents_registered_total")
        rules = http_json("http://127.0.0.1:9090/api/v1/rules")
        FLAG.unlink(missing_ok=True)
        after = register("rec-hw4")

        packet = {
            "incident_id": INCIDENT,
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "queries": [
                "GET /health",
                "POST /api/v1/agents (status only)",
                "GET Prometheus up / agent_relay_http_errors_total / rules",
            ],
            "health": http_json("http://127.0.0.1:8000/health")[0],
            "register_status_before": before,
            "register_status_injected": [fail1, fail2],
            "register_status_after": after,
            "inject_flag_present_after_recovery": FLAG.exists(),
            "prom_up": prom_up,
            "http_errors": prom_err,
            "agents_registered": prom_reg,
            "rules": rules[0],
            "notes": "Read-only packet. Response bodies omitted so tokens never land in evidence.",
        }
        (EVIDENCE / f"{INCIDENT}.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")
        print(f"before={before} fail={fail1},{fail2} after={after}")
        return 0 if before == 201 and fail1 == 500 and after == 201 else 2
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()


if __name__ == "__main__":
    sys.exit(main())
