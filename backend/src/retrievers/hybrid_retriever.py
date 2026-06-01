"""Hybrid retriever combining dense, BM25, RRF, and re-ranking."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.config.settings import get_settings
from backend.src.integrations.model_router import ModelRouter
from backend.src.retrievers.bm25_retriever import BM25Retriever
from backend.src.retrievers.rank_fusion import reciprocal_rank_fusion, normalize_scores
from backend.src.retrievers.reranker import LLMReranker
from backend.src.vectorstores.models import DocumentChunk
from backend.src.vectorstores.pgvector_store import PgVectorStore


class HybridRetriever:
    """Full hybrid retrieval pipeline: Dense + BM25 + RRF + Re-ranking."""

    def __init__(self, session: AsyncSession, router: ModelRouter) -> None:
        self._dense = PgVectorStore(session)
        self._bm25 = BM25Retriever(session)
        self._reranker = LLMReranker(router)
        settings = get_settings()
        self._dense_weight = settings.dense_retrieval_weight
        self._bm25_weight = settings.bm25_retrieval_weight

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: str | None = None,
        rerank: bool = True,
    ) -> list[RetrievalResult]:
        """Execute full hybrid retrieval pipeline."""
        dense_limit = top_k * 3
        dense_results = await self._dense.dense_search(query, limit=dense_limit)

        if category:
            bm25_results = await self._bm25.search_by_category(
                query, category, limit=dense_limit
            )
        else:
            bm25_results = await self._bm25.search(query, limit=dense_limit)

        fused = reciprocal_rank_fusion([dense_results, bm25_results])
        fused = normalize_scores(fused)

        if rerank and len(fused) > top_k:
            fused = await self._reranker.rerank(query, fused, top_k=top_k)

        return [
            RetrievalResult(
                chunk=chunk, score=score, source=chunk.source, title=chunk.title
            )
            for chunk, score in fused[:top_k]
        ]

    def format_context(self, results: list[RetrievalResult]) -> str:
        """Format retrieval results as context string for agents."""
        parts = []
        for i, result in enumerate(results, 1):
            parts.append(
                f"[Source {i}: {result.title}]\n{result.chunk.content}\n"
            )
        return "\n".join(parts)


class RetrievalResult:
    """Single retrieval result with metadata."""

    def __init__(
        self, chunk: DocumentChunk, score: float, source: str, title: str
    ) -> None:
        self.chunk = chunk
        self.score = score
        self.source = source
        self.title = title
        self.citation = f"[{title}] ({source})"
