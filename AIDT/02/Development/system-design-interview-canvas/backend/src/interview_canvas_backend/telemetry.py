"""OpenTelemetry setup — service name, environment, deployed version."""

from __future__ import annotations

import os
from typing import Any

from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "interview-canvas")
ENVIRONMENT = os.getenv("APP_ENV", os.getenv("DEPLOYMENT_ENVIRONMENT", "dev"))
DEPLOYED_VERSION = os.getenv("DEPLOYED_VERSION", "local")


def _disabled() -> bool:
    return os.getenv("OTEL_SDK_DISABLED", "").strip().lower() in {"1", "true", "yes"}


def resource() -> Resource:
    return Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": DEPLOYED_VERSION,
            "deployment.environment": ENVIRONMENT,
        }
    )


def metric_attrs() -> dict[str, str]:
    return {
        "environment": ENVIRONMENT,
        "deployed_version": DEPLOYED_VERSION,
    }


_rooms: Any = None
_participants: Any = None
_elements: Any = None
_failures: Any = None


def setup_metrics() -> None:
    global _rooms, _participants, _elements, _failures
    if _disabled():
        return
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4318")
    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{endpoint.rstrip('/')}/v1/metrics"),
        export_interval_millis=5000,
    )
    provider = MeterProvider(resource=resource(), metric_readers=[reader])
    metrics.set_meter_provider(provider)
    meter = metrics.get_meter(SERVICE_NAME, DEPLOYED_VERSION)
    _rooms = meter.create_counter(
        "interview_rooms_created",
        description="Interview rooms created",
    )
    _participants = meter.create_up_down_counter(
        "active_interview_participants",
        description="Active interview participants",
    )
    _elements = meter.create_counter(
        "canvas_elements_created",
        description="Canvas elements created",
    )
    _failures = meter.create_counter(
        "component_creation_failures",
        description="Failures in component creation",
    )


def setup_tracing(app: Any) -> None:
    if _disabled():
        return
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry import trace

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4318")
    provider = TracerProvider(resource=resource())
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint.rstrip('/')}/v1/traces"))
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)


def record_room_created() -> None:
    if _rooms is not None:
        _rooms.add(1, metric_attrs())


def record_participant_delta(delta: int) -> None:
    if _participants is not None:
        _participants.add(delta, metric_attrs())


def record_element_created() -> None:
    if _elements is not None:
        _elements.add(1, metric_attrs())


def record_component_failure() -> None:
    if _failures is not None:
        _failures.add(1, metric_attrs())
