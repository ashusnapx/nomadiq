"""Pydantic validation schemas for Itinerary and Activity items."""

from __future__ import annotations

from pydantic import BaseModel, Field
from backend.src.domain.enums import PlanVariant


class ActivityResponse(BaseModel):
    """Details of a single timeline event."""

    id: int
    day_number: int
    time_slot: str
    name: str
    description: str
    location: str
    cost: float
    category: str
    explanation: str | None = None
    citations: list[str] = []
    risk_score: float

    class Config:
        from_attributes = True


class DayPlan(BaseModel):
    """Consolidated activities and properties for a single day of travel."""

    day_number: int
    activities: list[ActivityResponse]
    daily_budget: float
    weather_summary: str | None = None


class ItineraryResponse(BaseModel):
    """Complete multi-variant itinerary returned to clients."""

    id: int
    trip_id: int
    variant: PlanVariant
    confidence_score: float
    total_cost: float
    is_active: bool
    days: list[DayPlan] = []

    class Config:
        from_attributes = True
