"""LLM-based re-ranker for retrieval result quality improvement."""

from __future__ import annotations

import json

from backend.src.integrations.model_router import ModelRouter, TaskComplexity
from backend.src.vectorstores.models import DocumentChunk

_RERANK_PROMPT = (
    "You are a relevance judge. Given a query and document passages, "
    "score each passage 0.0-1.0 for relevance to the query.\n\n"
    "Query: {query}\n\nPassages:\n{passages}\n\n"
    "Respond with a JSON array of objects: "
    '[{{"index": 0, "score": 0.85}}, ...]'
)


class LLMReranker:
    """Re-rank retrieval results using an LLM judge."""

    def __init__(self, router: ModelRouter) -> None:
        self._router = router

    async def rerank(
        self,
        query: str,
        results: list[tuple[DocumentChunk, float]],
        top_k: int = 5,
    ) -> list[tuple[DocumentChunk, float]]:
        """Re-rank results using LLM scoring."""
        if len(results) <= 1:
            return results[:top_k]

        passages = "\n".join(
            f"[{i}] {chunk.content[:300]}"
            for i, (chunk, _) in enumerate(results)
        )
        prompt = _RERANK_PROMPT.format(query=query, passages=passages)
        messages = [{"role": "user", "content": prompt}]

        response = await self._router.invoke(
            messages=messages,
            complexity=TaskComplexity.SIMPLE,
            response_format={"type": "json_object"},
        )

        try:
            scores = json.loads(response["content"])
            if isinstance(scores, dict) and "scores" in scores:
                scores = scores["scores"]
        except (json.JSONDecodeError, KeyError):
            return results[:top_k]

        scored = []
        for item in scores:
            idx = item.get("index", 0)
            score = item.get("score", 0.0)
            if 0 <= idx < len(results):
                scored.append((results[idx][0], score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
