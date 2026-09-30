"""HW4 inject flag: registration 500, then recovery. No tokens asserted."""

from __future__ import annotations

import os
from pathlib import Path

os.environ["RELAY_DATABASE_URL"] = (
    "sqlite:///E:/IT_SPACES/AI/.cache/tmp/agent-relay-hw4-test.db"
)
os.environ["OTEL_ENABLED"] = "0"
os.environ["OTEL_SDK_DISABLED"] = "1"

from fastapi.testclient import TestClient

import main

FLAG = Path(__file__).resolve().parent / "observability" / ".inject-register-failure"


def test_register_inject_and_recover():
    FLAG.unlink(missing_ok=True)
    client = TestClient(main.app)
    assert client.post("/api/v1/agents", json={"name": "ok-hw4"}).status_code == 201
    FLAG.write_text("on\n", encoding="utf-8")
    try:
        failed = client.post("/api/v1/agents", json={"name": "fail-hw4"})
        assert failed.status_code == 500
        assert "token" not in failed.json()
    finally:
        FLAG.unlink(missing_ok=True)
    recovered = client.post("/api/v1/agents", json={"name": "rec-hw4"})
    assert recovered.status_code == 201
    body = recovered.json()
    assert "token" in body
    # Do not persist the token anywhere else in this test.