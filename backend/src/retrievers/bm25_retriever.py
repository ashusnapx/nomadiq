"""BM25 keyword search implementation using PostgreSQL full-text search."""

from __future__ import annotations

from sqlalchemy import select, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.vectorstores.models import DocumentChunk


class BM25Retriever:
    """BM25-style keyword retrieval via PostgreSQL ts_rank."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def search(
        self, query: str, limit: int = 10
    ) -> list[tuple[DocumentChunk, float]]:
        """Full-text search with BM25-style ranking."""
        ts_query = func.plainto_tsquery("english", query)
        ts_vector = func.to_tsvector("english", DocumentChunk.content)
        rank = func.ts_rank_cd(ts_vector, ts_query).label("rank")

        stmt = (
            select(DocumentChunk, rank)
            .where(ts_vector.op("@@")(ts_query))
            .order_by(rank.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        if not rows:
            return []

        max_rank = max(row[1] for row in rows) or 1.0
        return [(row[0], float(row[1]) / max_rank) for row in rows]

    async def search_by_category(
        self, query: str, category: str, limit: int = 10
    ) -> list[tuple[DocumentChunk, float]]:
        """Full-text search filtered by document category."""
        ts_query = func.plainto_tsquery("english", query)
        ts_vector = func.to_tsvector("english", DocumentChunk.content)
        rank = func.ts_rank_cd(ts_vector, ts_query).label("rank")

        stmt = (
            select(DocumentChunk, rank)
            .where(ts_vector.op("@@")(ts_query))
            .where(DocumentChunk.category == category)
            .order_by(rank.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        if not rows:
            return []

        max_rank = max(row[1] for row in rows) or 1.0
        return [(row[0], float(row[1]) / max_rank) for row in rows]
