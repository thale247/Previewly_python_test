# Python + FastAPI preview with manual OpenTelemetry (traces, metrics, logs).
# Exec-form CMD keeps `uvicorn` as argv0 — Previewly may still prepend `opentelemetry-instrument` on some tiers;
# this codebase never imports auto-instrumentors; globals are registered in `backend.telemetry.configure()` so
# auto-instrumentation can attach to the same providers if you choose to wrap the process.
# Keep EXPOSE / --port aligned with `internal_port` in previewly.toml (8080).

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt* pyproject.toml* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir . 2>/dev/null || true

COPY . .

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
