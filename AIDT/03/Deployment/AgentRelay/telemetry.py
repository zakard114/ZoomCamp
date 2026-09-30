"""OpenTelemetry metrics, traces, and structured logs. Secrets stay out."""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "agent-relay")
ENVIRONMENT = os.getenv("APP_ENV", os.getenv("DEPLOYMENT_ENVIRONMENT", "dev"))
DEPLOYED_VERSION = os.getenv("DEPLOYED_VERSION", "local")

_SECRET_KEYS = {
    "authorization",
    "token",
    "claim_token",
    "x-enrollment-secret",
    "password",
    "secret",
    "api_key",
}

_agents: Any = None
_tasks: Any = None
_errors: Any = None
_log_handler: logging.Handler | None = None


def otel_enabled() -> bool:
    if os.getenv("OTEL_SDK_DISABLED", "").strip().lower() in {"1", "true", "yes"}:
        return False
    return os.getenv("OTEL_ENABLED", "").strip().lower() in {"1", "true", "yes"}


def metric_attrs(extra: dict[str, str] | None = None) -> dict[str, str]:
    attrs = {
        "environment": ENVIRONMENT,
        "deployed_version": DEPLOYED_VERSION,
        "service": SERVICE_NAME,
    }
    if extra:
        attrs.update(extra)
    return attrs


def _otlp_base() -> str:
    return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4318").rstrip("/")


def _resource():
    from opentelemetry.sdk.resources import Resource

    return Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": DEPLOYED_VERSION,
            "deployment.environment": ENVIRONMENT,
        }
    )


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT,
            "deployed_version": DEPLOYED_VERSION,
        }
        request_id = getattr(record, "request_id", None)
        if request_id:
            payload["request_id"] = request_id
        endpoint = getattr(record, "endpoint", None)
        if endpoint:
            payload["endpoint"] = endpoint
        status = getattr(record, "status", None)
        if status is not None:
            payload["status"] = status
        return json.dumps(payload, ensure_ascii=True)


def redact(value: str) -> str:
    return "[redacted]" if value else ""


def setup_structured_logging() -> None:
    root = logging.getLogger("agent_relay")
    root.setLevel(logging.INFO)
    if any(isinstance(h, logging.StreamHandler) and getattr(h, "_relay_json", False) for h in root.handlers):
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter())
    handler._relay_json = True  # type: ignore[attr-defined]
    root.addHandler(handler)
    root.propagate = False


def setup_metrics() -> None:
    global _agents, _tasks, _errors
    if not otel_enabled():
        return
    from opentelemetry import metrics
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{_otlp_base()}/v1/metrics"),
        export_interval_millis=5000,
    )
    metrics.set_meter_provider(MeterProvider(resource=_resource(), metric_readers=[reader]))
    meter = metrics.get_meter(SERVICE_NAME, DEPLOYED_VERSION)
    _agents = meter.create_counter("agent_relay_agents_registered", description="Successful agent registrations")
    _tasks = meter.create_counter("agent_relay_tasks_created", description="Tasks created")
    _errors = meter.create_counter("agent_relay_http_errors", description="HTTP errors on instrumented routes")


def setup_tracing(app: Any) -> None:
    if not otel_enabled():
        return
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    provider = TracerProvider(resource=_resource())
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{_otlp_base()}/v1/traces")))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)


def setup_otel_logs() -> None:
    if not otel_enabled():
        return
    global _log_handler
    try:
        from opentelemetry._logs import set_logger_provider
        from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    except ImportError:
        return
    provider = LoggerProvider(resource=_resource())
    provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=f"{_otlp_base()}/v1/logs"))
    )
    set_logger_provider(provider)
    _log_handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
    logging.getLogger("agent_relay").addHandler(_log_handler)


def record_agent_registered() -> None:
    if _agents is not None:
        _agents.add(1, metric_attrs({"endpoint": "/api/v1/agents"}))


def record_task_created() -> None:
    if _tasks is not None:
        _tasks.add(1, metric_attrs({"endpoint": "/api/v1/tasks"}))


def record_http_error(endpoint: str, status: int) -> None:
    if _errors is not None:
        _errors.add(1, metric_attrs({"endpoint": endpoint, "status": str(status)}))


def log_event(msg: str, *, request_id: str | None = None, endpoint: str | None = None, status: int | None = None) -> None:
    logger = logging.getLogger("agent_relay")
    extra: dict[str, Any] = {}
    if request_id:
        extra["request_id"] = request_id
    if endpoint:
        extra["endpoint"] = endpoint
    if status is not None:
        extra["status"] = status
    logger.info(msg, extra=extra)
