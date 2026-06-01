"""Event Service coordinating real-time event detections, impact analyses, and selective replannings."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.event import Event
from backend.src.models.activity import Activity
from backend.src.domain.enums import EventType
from backend.src.notifications.event_bus import event_bus
from backend.src.notifications.events import (
    WeatherChangedEvent,
    FlightDelayedEvent,
    AttractionClosedEvent,
    TransportDisruptionEvent,
)
from backend.src.workflows.replanning_workflow import ReplanningWorkflow
from backend.src.integrations.model_router import ModelRouter
from backend.src.repositories.event_repository import EventRepository
from backend.src.repositories.itinerary_repository import ItineraryRepository

logger = logging.getLogger(__name__)


class EventService:
    """Ingests delay/closure/weather events, analyzes timeline impacts, and triggers selective replanning."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._event_repo = EventRepository(db)
        self._itinerary_repo = ItineraryRepository(db)
        self._router = ModelRouter()

    async def register_disruption(
        self, trip_id: int, event_type: EventType, severity: str, desc: str
    ) -> Event:
        """Create disruption event, write to DB, and publish to the async Event Bus."""
        # Find active itinerary to analyze impact
        active_plan = await self._itinerary_repo.get_active_variant(trip_id)
        affected_ids = []

        if active_plan:
            # Simple impact analysis heuristic
            keyword = desc.lower()
            for act in active_plan.activities:
                if (
                    keyword in act.name.lower()
                    or keyword in act.description.lower()
                    or (event_type == EventType.RAIN and act.category == "Nature")
                ):
                    affected_ids.append(act.id)

        impact = {
            "affected_activity_ids": affected_ids,
            "severity": severity,
            "description": desc,
            "replan_recommended": len(affected_ids) > 0,
        }

        event = Event(
            trip_id=trip_id,
            event_type=event_type,
            severity=severity,
            description=desc,
            detected_at=datetime.now(timezone.utc),
            impact_analysis=impact,
        )
        await self._event_repo.create(event)

        # Map to specific event bus message and publish
        bus_msg = self._map_to_event_payload(trip_id, event_type, impact)
        await event_bus.publish(bus_msg)

        # Trigger active selective replanning if recommended
        if impact["replan_recommended"] and active_plan:
            await self.trigger_replan(trip_id, event, active_plan, affected_ids)

        return event

    async def trigger_replan(
        self, trip_id: int, event: Event, itinerary: Any, affected_ids: list[int]
    ) -> None:
        """Surgically replace affected timeline activities using ReplanningWorkflow."""
        logger.info(f"Triggering selective replan for trip: {trip_id} on event: {event.id}")

        affected_acts = [a for a in itinerary.activities if a.id in affected_ids]
        current_itinerary_dict = {
            "activities": [
                {"id": a.id, "name": a.name, "day": a.day_number, "cost": a.cost}
                for a in itinerary.activities
            ]
        }

        replanner = ReplanningWorkflow(self._router)
        res = await replanner.execute(
            {
                "trip_id": trip_id,
                "event": {
                    "event_type": event.event_type.value,
                    "severity": event.severity,
                    "description": event.description,
                },
                "current_itinerary": current_itinerary_dict,
                "affected_activities": [
                    {"id": a.id, "name": a.name} for a in affected_acts
                ],
                "budget_remaining": itinerary.total_cost * 0.5,
            }
        )

        # Persist modifications
        replacements = res.get("replanned_activities", [])
        for idx, rep in enumerate(replacements):
            if idx < len(affected_acts):
                target = affected_acts[idx]
                target.name = rep.get("name", target.name)
                target.description = rep.get("description", target.description)
                target.cost = rep.get("cost", target.cost)
                target.explanation = f"Replanned due to event: {event.description}"

        event.resolved_at = datetime.now(timezone.utc)
        await self._db.flush()

    def _map_to_event_payload(
        self, trip_id: int, event_type: EventType, impact: dict
    ) -> Any:
        kwargs = {"trip_id": trip_id, "payload": impact}
        if event_type == EventType.RAIN:
            return WeatherChangedEvent(**kwargs)
        if event_type == EventType.FLIGHT_DELAY:
            return FlightDelayedEvent(**kwargs)
        if event_type == EventType.ATTRACTION_CLOSURE:
            return AttractionClosedEvent(**kwargs)
        return TransportDisruptionEvent(**kwargs)
overrides = {}
