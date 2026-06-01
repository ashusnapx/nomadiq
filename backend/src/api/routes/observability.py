"""Observability API Router exposing AI cost governance and feature flag states."""

from __future__ import annotations

from fastapi import APIRouter
from backend.src.observability.cost_tracker import cost_tracker
from backend.src.config.feature_flags import feature_flags

router = APIRouter(prefix="/observability", tags=["Observability"])


@router.get("/costs", response_model=dict)
async def get_costs() -> dict:
    """Retrieve aggregate AI token consumption and estimated request costs."""
    return cost_tracker.get_summary()


@router.post("/costs/reset", response_model=dict)
async def reset_costs() -> dict:
    """Clear recorded cost accumulations."""
    cost_tracker.clear()
    return {"message": "Cost records reset successfully."}


@router.get("/feature-flags", response_model=dict)
async def get_feature_flags() -> dict:
    """Retrieve state of active feature flags across the platform."""
    return feature_flags.get_all_flags()


@router.post("/feature-flags/override/{flag}", response_model=dict)
async def override_feature_flag(flag: str, value: bool) -> dict:
    """Dynamically modify feature flag state in-memory."""
    feature_flags.set_override(flag, value)
    return {
        "message": f"Feature flag '{flag}' successfully overridden to: {value}."
    }
