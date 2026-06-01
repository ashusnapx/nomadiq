"""Event repository mapping active trip disruption entities."""

from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.event import Event
from backend.src.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    """Data access routines for Event records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Event, session)

    async def get_by_trip(self, trip_id: int) -> list[Event]:
        """Fetch all events matched to trip ID."""
        stmt = select(Event).where(Event.trip_id == trip_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_unresolved(self, trip_id: int) -> list[Event]:
        """Fetch active, unresolved disruption events for trip ID."""
        stmt = select(Event).where(
            and_(Event.trip_id == trip_id, Event.resolved_at == None)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
