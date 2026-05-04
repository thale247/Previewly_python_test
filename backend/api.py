"""JSON API used by the static frontend — HTTP spans/metrics come from OpenTelemetry auto-instrumentation."""

from __future__ import annotations

import logging
import random

from fastapi import APIRouter, Query

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health() -> dict[str, str]:
    logger.info("health check")
    return {"status": "ok"}


@router.get("/roll")
async def roll(sides: int = Query(8, ge=2, le=100)) -> dict[str, int]:
    value = random.randint(1, sides)
    logger.info("rolled dice", extra={"dice.sides": sides, "dice.value": value})
    return {"sides": sides, "value": value}
