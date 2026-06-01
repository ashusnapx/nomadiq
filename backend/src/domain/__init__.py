"""Domain package grouping models, enums and custom type annotations."""

from __future__ import annotations

from backend.src.domain.enums import (
    TripStatus,
    ActivityType,
    TravelerPersona,
    EventType,
    RiskLevel,
    WeatherCondition,
    TransportMode,
    PlanVariant,
)
from backend.src.domain.types import Coordinates, BudgetRange, TimeSlot

__all__ = [
    "TripStatus",
    "ActivityType",
    "TravelerPersona",
    "EventType",
    "RiskLevel",
    "WeatherCondition",
    "TransportMode",
    "PlanVariant",
    "Coordinates",
    "BudgetRange",
    "TimeSlot",
]
