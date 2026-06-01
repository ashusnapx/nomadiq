"""Asynchronous Event Bus for real-time pub/sub, event replays, and Dead Letter Queues."""

from __future__ import annotations

import logging
import asyncio
from typing import Any, Callable, Coroutine
from backend.src.domain.enums import EventType
from backend.src.notifications.events import BaseEvent

logger = logging.getLogger(__name__)


class EventBus:
    """Dispatches asynchronous event notifications to registered handlers with failure safety."""

    def __init__(self) -> None:
        self._handlers: dict[
            EventType, list[Callable[[BaseEvent], Coroutine[Any, Any, None]]]
        ] = {}
        self.event_history: list[BaseEvent] = []
        self.dead_letter_queue: list[tuple[BaseEvent, Exception]] = []

    def subscribe(
        self,
        event_type: EventType,
        handler: Callable[[BaseEvent], Coroutine[Any, Any, None]],
    ) -> None:
        """Register a coroutine listener for specific event category."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info(f"Subscribed handler {handler.__name__} to event: {event_type.value}")

    async def publish(self, event: BaseEvent) -> None:
        """Asynchronously dispatch events to registered handlers."""
        self.event_history.append(event)
        logger.info(
            f"Publishing event {event.event_id} ({event.event_type.value}) for trip: {event.trip_id}"
        )

        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            logger.debug(f"No active handlers registered for {event.event_type.value}")
            return

        tasks = []
        for handler in handlers:
            tasks.append(self._safe_dispatch(handler, event))

        await asyncio.gather(*tasks)

    async def _safe_dispatch(
        self,
        handler: Callable[[BaseEvent], Coroutine[Any, Any, None]],
        event: BaseEvent,
    ) -> None:
        try:
            await handler(event)
        except Exception as exc:
            logger.error(
                f"Handler {handler.__name__} failed processing event {event.event_id}: {exc}"
            )
            # Route failed events to Dead Letter Queue (DLQ)
            self.dead_letter_queue.append((event, exc))

    async def replay_history(self, trip_id: int) -> None:
        """Replay historical events matching trip ID for testing or restoration."""
        logger.info(f"Replaying event logs for trip: {trip_id}")
        for event in self.event_history:
            if event.trip_id == trip_id:
                await self.publish(event)

    async def retry_dlq(self) -> None:
        """Retry dispatching failed events currently stored in the DLQ."""
        if not self.dead_letter_queue:
            logger.info("Dead Letter Queue is empty.")
            return

        logger.info(f"Retrying {len(self.dead_letter_queue)} failed DLQ events.")
        dlq_copy = list(self.dead_letter_queue)
        self.dead_letter_queue.clear()

        for event, _ in dlq_copy:
            await self.publish(event)


event_bus = EventBus()
