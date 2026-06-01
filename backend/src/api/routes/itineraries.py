"""Itineraries API Router driving multi-agent compilation workflows."""

from __future__ import annotations

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.shared.database import get_db
from backend.src.schemas.itinerary import ItineraryResponse
from backend.src.services.itinerary_service import ItineraryService

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])


@router.post("/generate/{trip_id}", response_model=list[ItineraryResponse], status_code=201)
async def generate_itineraries(
    trip_id: int, db: AsyncSession = Depends(get_db)
) -> list[ItineraryResponse]:
    """Execute LangGraph workflows, compiling and saving Plan A, B, and C variants."""
    service = ItineraryService(db)
    res = await service.generate_itineraries(trip_id)
    # Simple mapping to match response model requirements
    return [ItineraryResponse.model_validate(r) for r in res]


@router.get("/active/{trip_id}", response_model=ItineraryResponse)
async def get_active_itinerary(
    trip_id: int, db: AsyncSession = Depends(get_db)
) -> ItineraryResponse:
    """Fetch active itinerary variant with complete day timeline activities."""
    service = ItineraryService(db)
    itinerary = await service.get_active_itinerary(trip_id)
    if not itinerary:
        from backend.src.exceptions.api_errors import NotFoundError
        raise NotFoundError(f"No active itinerary found for trip {trip_id}.")

    # Format day plans dynamically for API presentation
    day_map: dict[int, list] = {}
    for act in itinerary.activities:
        day_map.setdefault(act.day_number, []).append(act)

    days = []
    for day_num, acts in sorted(day_map.items()):
        days.append(
            {
                "day_number": day_num,
                "activities": acts,
                "daily_budget": sum(a.cost for a in acts),
                "weather_summary": "Sunny",
            }
        )

    return ItineraryResponse(
        id=itinerary.id,
        trip_id=itinerary.trip_id,
        variant=itinerary.variant,
        confidence_score=itinerary.confidence_score,
        total_cost=itinerary.total_cost,
        is_active=itinerary.is_active,
        days=days,
    )
