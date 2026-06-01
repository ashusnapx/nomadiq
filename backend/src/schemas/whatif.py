"""Pydantic validation schemas for What-If scenario simulations."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WhatIfRequest(BaseModel):
    """Scenario simulation parameters requested by traveler."""

    trip_id: int
    scenario_type: str = Field(
        ..., pattern="^(budget_cut|weather_disruption|closure|custom)$"
    )
    parameter_value: str  # E.g., "30%" budget cut, "Rain at 15:00", etc.


class ScenarioResult(BaseModel):
    """Itinerary variant changes resulting from hypothetical event application."""

    variant_name: str
    original_cost: float
    simulated_cost: float
    original_score: float
    simulated_score: float
    affected_activities: list[str] = []
    replacements: list[str] = []


class WhatIfResponse(BaseModel):
    """Comparison report showcasing simulated outcomes across variants."""

    trip_id: int
    scenario_description: str
    impact_assessment: str
    results: list[ScenarioResult] = []
    timestamp: str
