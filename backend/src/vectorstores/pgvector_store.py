"""pgvector store: insert and dense retrieval operations."""

from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.vectorstores.models import DocumentChunk
from backend.src.vectorstores.embeddings import EmbeddingService


class PgVectorStore:
    """PostgreSQL + pgvector backed vector store."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._embedder = EmbeddingService()

    async def add_document(
        self,
        source: str,
        title: str,
        content: str,
        chunk_index: int,
        category: str = "general",
        metadata: dict | None = None,
    ) -> DocumentChunk:
        """Add a single document chunk with embedding."""
        embedding = await self._embedder.embed_text(content)
        bm25_tokens = " ".join(content.lower().split())
        chunk = DocumentChunk(
            source=source,
            title=title,
            content=content,
            chunk_index=chunk_index,
            embedding=embedding,
            category=category,
            metadata_=metadata or {},
            bm25_tokens=bm25_tokens,
        )
        self._session.add(chunk)
        await self._session.flush()
        return chunk

    async def dense_search(
        self, query: str, limit: int = 10
    ) -> list[tuple[DocumentChunk, float]]:
        """Semantic similarity search using cosine distance."""
        query_embedding = await self._embedder.embed_text(query)
        stmt = (
            select(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(query_embedding).label("distance"),
            )
            .order_by("distance")
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [(row[0], 1.0 - row[1]) for row in result.all()]

    async def add_batch(
        self, documents: list[dict]
    ) -> list[DocumentChunk]:
        """Add multiple documents with batch embedding."""
        texts = [doc["content"] for doc in documents]
        embeddings = await self._embedder.embed_batch(texts)
        chunks = []
        for doc, emb in zip(documents, embeddings):
            chunk = DocumentChunk(
                source=doc["source"],
                title=doc["title"],
                content=doc["content"],
                chunk_index=doc.get("chunk_index", 0),
                embedding=emb,
                category=doc.get("category", "general"),
                metadata_=doc.get("metadata", {}),
                bm25_tokens=" ".join(doc["content"].lower().split()),
            )
            self._session.add(chunk)
            chunks.append(chunk)
        await self._session.flush()
        return chunks
