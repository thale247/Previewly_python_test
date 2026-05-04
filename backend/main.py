"""FastAPI entry: API under /api, static UI and assets for the browser."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api import router as api_router

_FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title="Previewly Python observability demo",
    description="OpenTelemetry via auto-instrumentation (FastAPI ASGI + stdlib logging → OTLP when enabled).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def serve_spa() -> FileResponse:
    return FileResponse(_FRONTEND_DIR / "index.html")


if _FRONTEND_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=_FRONTEND_DIR), name="static")
