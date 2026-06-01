"""Notifications package exposing the Event Bus and Event definitions."""

from __future__ import annotations

from backend.src.notifications.event_bus import event_bus
from backend.src.notifications.events import (
    BaseEvent,
    WeatherChangedEvent,
    FlightDelayedEvent,
    AttractionClosedEvent,
    BudgetExceededEvent,
    TransportDisruptionEvent,
)

__all__ = [
    "event_bus",
    "BaseEvent",
    "WeatherChangedEvent",
    "FlightDelayedEvent",
    "AttractionClosedEvent",
    "BudgetExceededEvent",
    "TransportDisruptionEvent",
]
