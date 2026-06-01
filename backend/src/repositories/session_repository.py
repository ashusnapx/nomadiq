"""Session repository providing lookups for conversational history."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.session import Session
from backend.src.repositories.base import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """Data access routines for conversational logs."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Session, session)

    async def get_by_trip(self, trip_id: int) -> Session | None:
        """Fetch persistent conversational session matched to trip ID."""
        stmt = select(Session).where(Session.trip_id == trip_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
