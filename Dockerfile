# Example Python + Uvicorn preview for Previewly OTLP auto-instrumentation.
# Exec-form CMD keeps `uvicorn` as argv0 so Previewly can wrap with `opentelemetry-instrument`.
# Keep EXPOSE / --port aligned with `internal_port` in previewly.toml (8080).

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt* pyproject.toml* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir . 2>/dev/null || true

COPY . .

EXPOSE 8080

CMD ["opentelemetry-instrument", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
