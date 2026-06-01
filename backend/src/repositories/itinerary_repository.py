"""Itinerary repository offering filters for variants and scheduled activities."""

from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.itinerary import Itinerary
from backend.src.domain.enums import PlanVariant
from backend.src.repositories.base import BaseRepository


class ItineraryRepository(BaseRepository[Itinerary]):
    """Data access routines for Itinerary resources."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Itinerary, session)

    async def get_by_trip(self, trip_id: int) -> list[Itinerary]:
        """Fetch all itinerary variants registered to trip ID."""
        stmt = (
            select(Itinerary)
            .where(Itinerary.trip_id == trip_id)
            .options(selectinload(Itinerary.activities))
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_active_variant(self, trip_id: int) -> Itinerary | None:
        """Fetch primary active variant for trip ID."""
        stmt = (
            select(Itinerary)
            .where(and_(Itinerary.trip_id == trip_id, Itinerary.is_active == True))
            .options(selectinload(Itinerary.activities))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_variant_by_type(
        self, trip_id: int, variant: PlanVariant
    ) -> Itinerary | None:
        """Get specific itinerary variant by category."""
        stmt = (
            select(Itinerary)
            .where(and_(Itinerary.trip_id == trip_id, Itinerary.variant == variant))
            .options(selectinload(Itinerary.activities))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
overrides = {}
