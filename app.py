"""Minimal FastAPI app for Previewly Python preview + OTLP demos."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    logger.info(
        "python-preview OTLP demo log line",
        extra={"previewly.otlp_demo": "logs-via-http-protobuf"},
    )
    return {"status": "ok"}
