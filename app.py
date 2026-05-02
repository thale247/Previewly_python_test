"""Minimal FastAPI app for Previewly Python preview + OTLP demos."""

from fastapi import FastAPI
from opentelemetry import trace

app = FastAPI()
tracer = trace.get_tracer(__name__)


@app.get("/")
async def root() -> dict[str, str]:
    with tracer.start_as_current_span("example-root-span"):
        return {"status": "ok"}
