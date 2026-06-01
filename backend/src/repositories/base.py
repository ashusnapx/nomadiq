"""Generic async repository implementation containing standard CRUD operations."""

from __future__ import annotations

from typing import Any, Generic, Sequence, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Standard generic async data repository patterns."""

    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, record_id: int) -> T | None:
        """Find record by primary key."""
        return await self.session.get(self.model, record_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]:
        """Fetch records with pagination offsets."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, entity: T) -> T:
        """Persist a new entity instance."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity: T) -> None:
        """Remove a persisted entity from the database."""
        await self.session.delete(entity)
        await self.session.flush()
overrides = {}
