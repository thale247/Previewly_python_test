"""Manual OpenTelemetry wiring (traces, metrics, logs) — no LoggingInstrumentor / framework auto-instrumentors.

`opentelemetry-instrument` can still wrap `uvicorn` for customers who want automatic HTTP spans; this module only registers
SDK providers so those globals exist. We do not import `opentelemetry.instrumentation.*` here.
"""

from __future__ import annotations

import atexit
import logging
import os
from typing import Final

from opentelemetry import metrics as otel_metrics
from opentelemetry import trace as otel_trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_LOG_NAMESPACE: Final = "previewly.demo"

_configured = False


def configure() -> None:
    """Idempotent: install global TracerProvider, MeterProvider, and LoggerProvider + OTLP HTTP exporters."""
    global _configured
    if _configured:
        return

    service_name = os.environ.get("OTEL_SERVICE_NAME", "previewly-python-demo")
    resource = Resource.create({SERVICE_NAME: service_name})

    trace_exporter = OTLPSpanExporter()
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    otel_trace.set_tracer_provider(tracer_provider)

    metric_exporter = OTLPMetricExporter()
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    otel_metrics.set_meter_provider(meter_provider)

    log_exporter = OTLPLogExporter()
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)

    otlp_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    app_logger = logging.getLogger(_LOG_NAMESPACE)
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(otlp_handler)
    app_logger.propagate = False

    def _shutdown() -> None:
        tracer_provider.shutdown()
        meter_provider.shutdown()
        logger_provider.shutdown()

    atexit.register(_shutdown)
    _configured = True


def get_demo_logger() -> logging.Logger:
    return logging.getLogger(_LOG_NAMESPACE)
