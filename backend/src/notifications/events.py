"""Domain event definitions representing real-time travel disruptions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from backend.src.domain.enums import EventType


@dataclass
class BaseEvent:
    """Ancestral event context mapping system changes."""

    trip_id: int
    event_type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class WeatherChangedEvent(BaseEvent):
    """Triggered on weather condition modifications."""

    event_type: EventType = EventType.RAIN


@dataclass
class FlightDelayedEvent(BaseEvent):
    """Triggered on flight schedule delays."""

    event_type: EventType = EventType.FLIGHT_DELAY


@dataclass
class AttractionClosedEvent(BaseEvent):
    """Triggered on attraction closures."""

    event_type: EventType = EventType.ATTRACTION_CLOSURE


@dataclass
class BudgetExceededEvent(BaseEvent):
    """Triggered when costs exceed constraints."""

    event_type: EventType = EventType.BUDGET_OVERRUN


@dataclass
class TransportDisruptionEvent(BaseEvent):
    """Triggered on transit breakdowns or route blocks."""

    event_type: EventType = EventType.TRAIN_DELAY
overrides = {}
