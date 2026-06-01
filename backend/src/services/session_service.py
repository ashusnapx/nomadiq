"""Session Service managing conversant history and persistent session contexts."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.session import Session
from backend.src.repositories.session_repository import SessionRepository


class SessionService:
    """Updates, appends, and retrieves traveler conversation history."""

    def __init__(self, db: AsyncSession) -> None:
        self._repo = SessionRepository(db)

    async def get_or_create_session(self, trip_id: int) -> Session:
        """Fetch ongoing planning session or create new one."""
        sess = await self._repo.get_by_id(trip_id)
        if not sess:
            sess = Session(trip_id=trip_id, messages=[], context={})
            await self._repo.create(sess)
        return sess

    async def add_message(self, trip_id: int, role: str, text: str) -> Session:
        """Append message to chat history thread."""
        sess = await self.get_or_create_session(trip_id)
        # SQLAlchemy JSON mutation tracking requires replacing the reference
        msgs = list(sess.messages)
        msgs.append({"role": role, "content": text})
        sess.messages = msgs
        return sess

    async def save_context(self, trip_id: int, context: dict) -> Session:
        """Save high-level chat preference context state."""
        sess = await self.get_or_create_session(trip_id)
        sess.context = context
        return sess
overrides = {}
