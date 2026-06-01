"""Reciprocal Rank Fusion for combining retrieval results."""

from __future__ import annotations

from backend.src.vectorstores.models import DocumentChunk


def reciprocal_rank_fusion(
    result_lists: list[list[tuple[DocumentChunk, float]]],
    k: int = 60,
) -> list[tuple[DocumentChunk, float]]:
    """Combine multiple ranked lists using Reciprocal Rank Fusion.

    RRF score = sum(1 / (k + rank_i)) across all lists.
    k=60 is the standard constant from the original RRF paper.
    """
    scores: dict[int, float] = {}
    chunk_map: dict[int, DocumentChunk] = {}

    for result_list in result_lists:
        for rank, (chunk, _score) in enumerate(result_list):
            chunk_id = chunk.id
            chunk_map[chunk_id] = chunk
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank + 1)

    sorted_ids = sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)
    return [(chunk_map[cid], scores[cid]) for cid in sorted_ids]


def normalize_scores(
    results: list[tuple[DocumentChunk, float]],
) -> list[tuple[DocumentChunk, float]]:
    """Normalize scores to 0.0-1.0 range."""
    if not results:
        return []

    max_score = max(score for _, score in results)
    min_score = min(score for _, score in results)
    spread = max_score - min_score

    if spread == 0:
        return [(chunk, 1.0) for chunk, _ in results]

    return [
        (chunk, (score - min_score) / spread)
        for chunk, score in results
    ]
