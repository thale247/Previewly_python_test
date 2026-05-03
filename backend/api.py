"""JSON API used by the static frontend — each handler records traces, metrics, and logs manually."""

from __future__ import annotations

import random

from fastapi import APIRouter, Query
from opentelemetry import trace
from opentelemetry.metrics import get_meter

from backend.telemetry import get_demo_logger

router = APIRouter()

logger = get_demo_logger()
tracer = trace.get_tracer(__name__)
meter = get_meter(__name__, "1.0.0")

dice_rolls = meter.create_counter(
    "previewly.demo.dice_rolls_total",
    unit="1",
    description="Count of dice rolls from the demo API",
)
dice_values = meter.create_histogram(
    "previewly.demo.dice_value",
    unit="1",
    description="Observed face values from the demo dice roller",
)


@router.get("/health")
async def health() -> dict[str, str]:
    with tracer.start_as_current_span("api.health"):
        logger.info("health check", extra={"http.route": "/api/health"})
        return {"status": "ok"}


@router.get("/roll")
async def roll(sides: int = Query(8, ge=2, le=100)) -> dict[str, int]:
    with tracer.start_as_current_span("api.roll_dice") as span:
        span.set_attribute("dice.sides", sides)
        value = random.randint(1, sides)
        span.set_attribute("dice.value", value)
        dice_rolls.add(1, {"sides": str(sides)})
        dice_values.record(value, {"sides": str(sides)})
        logger.info(
            "rolled dice",
            extra={"dice.sides": sides, "dice.value": value, "http.route": "/api/roll"},
        )
        return {"sides": sides, "value": value}
