"""Trip Service handling validation and persistence layer logic for Trips."""

from __future__ import annotations

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.trip import Trip
from backend.src.domain.enums import TripStatus
from backend.src.schemas.trip import TripCreate, TripUpdate
from backend.src.repositories.trip_repository import TripRepository
from backend.src.exceptions.api_errors import NotFoundError


class TripService:
    """Provides business logic for Trip objects."""

    def __init__(self, db: AsyncSession) -> None:
        self._repo = TripRepository(db)

    async def create_trip(self, payload: TripCreate) -> Trip:
        """Create and persist a new trip with default planning status."""
        trip = Trip(
            title=payload.title,
            destination=payload.destination,
            start_date=payload.start_date,
            end_date=payload.end_date,
            budget_min=payload.budget_min,
            budget_max=payload.budget_max,
            status=TripStatus.PLANNING,
            persona=payload.persona,
            preferences=payload.preferences,
        )
        return await self._repo.create(trip)

    async def get_trip(self, trip_id: int) -> Trip:
        """Fetch single trip by primary key, raising NotFoundError if missing."""
        trip = await self._repo.get_by_id(trip_id)
        if not trip:
            raise NotFoundError(f"Trip with ID {trip_id} not found.")
        return trip

    async def list_trips(self, skip: int = 0, limit: int = 100) -> Sequence[Trip]:
        """Fetch all trips with pagination boundaries."""
        return await self._repo.get_all(skip, limit)

    async def update_trip(self, trip_id: int, payload: TripUpdate) -> Trip:
        """Modify existing trip preferences or status."""
        trip = await self.get_trip(trip_id)
        if payload.title is not None:
            trip.title = payload.title
        if payload.status is not None:
            trip.status = payload.status
        if payload.preferences is not None:
            trip.preferences = payload.preferences
        return trip
overrides = {}
