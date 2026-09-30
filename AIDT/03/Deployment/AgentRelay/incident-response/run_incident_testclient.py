"""Incident without a long-lived server. OTel off so exporters cannot hang."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

os.environ["OTEL_ENABLED"] = "0"
os.environ["OTEL_SDK_DISABLED"] = "1"

ROOT = Path(__file__).resolve().parents[1]
FLAG = ROOT / "observability" / ".inject-register-failure"
OUT = ROOT / "incident-response" / "evidence" / "INC-20260925-001.json"

from fastapi.testclient import TestClient
import main


def prom(query: str):
    url = "http://127.0.0.1:9090/api/v1/query?query=" + urllib.request.quote(query)
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as exc:
        return {"error": str(exc)}


def main_run() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    FLAG.unlink(missing_ok=True)
    client = TestClient(main.app)
    before = client.post("/api/v1/agents", json={"name": "ok-hw4"}).status_code
    FLAG.write_text("on\n", encoding="utf-8")
    fail1 = client.post("/api/v1/agents", json={"name": "fail-hw4-a"}).status_code
    fail2 = client.post("/api/v1/agents", json={"name": "fail-hw4-b"}).status_code
    FLAG.unlink(missing_ok=True)
    after = client.post("/api/v1/agents", json={"name": "rec-hw4"}).status_code
    packet = {
        "incident_id": "INC-20260925-001",
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "queries": [
            "POST /api/v1/agents status only (TestClient, read response status, drop body)",
            "GET Prometheus up",
            "GET Prometheus agent_relay_http_errors_total",
        ],
        "register_status_before": before,
        "register_status_injected": [fail1, fail2],
        "register_status_after": after,
        "inject_flag_present_after_recovery": FLAG.exists(),
        "prom_up": prom("up"),
        "http_errors": prom("agent_relay_http_errors_total"),
        "notes": "Bodies discarded. Tokens not stored. OTel disabled for this collector run because the live uvicorn spawn hung on this host; pipeline compose is in observability/ and the already-running local collector still answers Prometheus up.",
    }
    OUT.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"before={before} fail={fail1},{fail2} after={after} wrote={OUT}")


if __name__ == "__main__":
    main_run()
