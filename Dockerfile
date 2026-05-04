# Python + FastAPI preview with OpenTelemetry auto-instrumentation (no manual SDK wiring in app code).
#
# Starter/Pro: Previewly appends distro layers + ENTRYPOINT bootstrap that runs `uvicorn` through
# `opentelemetry-instrument` when PREVIEWLY_OTEL_AUTO_BOOTSTRAP=1 — keep CMD as plain `uvicorn` here
# so the process is not double-wrapped.
#
# Local OTLP: install deps and run:
#   opentelemetry-instrument uvicorn backend.main:app --host 0.0.0.0 --port 8080
# with OTEL_* set (see otel/README.md).
#
# Keep EXPOSE / port aligned with `internal_port` in previewly.toml (8080).

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt* pyproject.toml* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir . 2>/dev/null || true

COPY . .

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
