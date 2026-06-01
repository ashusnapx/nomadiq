"""Core Domain Type Aliases and structural helper types."""

from __future__ import annotations

from typing import NamedTuple, NewType

# Strongly typed database and operational references
TripId = NewType("TripId", int)
ItineraryId = NewType("ItineraryId", int)
ActivityId = NewType("ActivityId", int)


class Coordinates(NamedTuple):
    """Simple latitude/longitude geocoding pair."""

    latitude: float
    longitude: float


class BudgetRange(NamedTuple):
    """Valid range bounds for budget validations."""

    min_usd: float
    max_usd: float


class TimeSlot(NamedTuple):
    """Daily schedule time slot with start and end bounds (HH:MM)."""

    start_time: str
    end_time: str
