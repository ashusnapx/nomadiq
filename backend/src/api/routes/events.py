"""Events API Router exposing disruption registration endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.shared.database import get_db
from backend.src.schemas.event import EventCreate, EventResponse
from backend.src.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Disruption Events"])


@router.post("/trigger/{trip_id}", response_model=EventResponse, status_code=201)
async def trigger_event(
    trip_id: int, payload: EventCreate, db: AsyncSession = Depends(get_db)
) -> EventResponse:
    """Register unexpected weather, delays or closures and trigger selective replanning."""
    service = EventService(db)
    event = await service.register_disruption(
        trip_id=trip_id,
        event_type=payload.event_type,
        severity=payload.severity,
        desc=payload.description,
    )
    return EventResponse.model_validate(event)
