"""Minimal FastAPI app for Previewly Python preview + OTLP demos."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Runs after Previewly/opentelemetry-instrument bootstraps the SDK + LoggerProvider.
    LoggingInstrumentor().instrument(set_logging_format=True)
    yield


app = FastAPI(lifespan=lifespan)
tracer = trace.get_tracer(__name__)


@app.get("/")
async def root() -> dict[str, str]:
    with tracer.start_as_current_span("example-root-span"):
        logger.info(
            "python-preview OTLP demo log line",
            extra={"previewly.otlp_demo": "logs-via-http-protobuf"},
        )
        return {"status": "ok"}
