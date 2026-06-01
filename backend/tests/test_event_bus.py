"""Unit tests for the Asynchronous Event Bus and Dead Letter Queues."""

from __future__ import annotations

import pytest
from backend.src.domain.enums import EventType
from backend.src.notifications.event_bus import event_bus
from backend.src.notifications.events import WeatherChangedEvent


@pytest.mark.asyncio
async def test_event_bus_pub_sub() -> None:
    """Verifies that events are dispatched to subscribed handlers and tracked in history."""
    received_events = []

    async def mock_handler(event) -> None:
        received_events.append(event)

    # Subscribe handler
    event_bus.subscribe(EventType.RAIN, mock_handler)

    # Publish target event
    test_event = WeatherChangedEvent(trip_id=5, payload={"condition": "Rainy"})
    await event_bus.publish(test_event)

    assert len(received_events) == 1
    assert received_events[0].trip_id == 5
    assert received_events[0].payload["condition"] == "Rainy"
    
    # Check that event was recorded in history logs
    assert len(event_bus.event_history) >= 1
    assert event_bus.event_history[-1].event_id == test_event.event_id
