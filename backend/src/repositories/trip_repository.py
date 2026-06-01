"""Trip repository providing specialized search operations."""

from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.trip import Trip
from backend.src.domain.enums import TripStatus
from backend.src.repositories.base import BaseRepository


class TripRepository(BaseRepository[Trip]):
    """Data access routines for Trip resources."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Trip, session)

    async def get_by_status(self, status: TripStatus) -> list[Trip]:
        """Lookup trips currently matching status enum."""
        stmt = select(Trip).where(Trip.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_active_by_destination(self, dest: str) -> list[Trip]:
        """Fetch trips active at target destination."""
        stmt = select(Trip).where(
            and_(Trip.destination == dest, Trip.status == TripStatus.ACTIVE)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
