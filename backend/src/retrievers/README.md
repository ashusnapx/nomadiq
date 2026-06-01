# Retrievers

## Purpose
Hybrid retrieval pipeline combining multiple search strategies for production-grade RAG.

## Ownership
AI/ML Engineering Team

## Architecture
```
Query → [Dense Search (pgvector)] ──┐
                                     ├→ Reciprocal Rank Fusion → Re-ranking → Results
Query → [BM25 Search (PostgreSQL)] ─┘
```

## Components
| File | Responsibility |
|------|---------------|
| `hybrid_retriever.py` | Orchestrates the full pipeline |
| `bm25_retriever.py` | PostgreSQL full-text search (keyword) |
| `rank_fusion.py` | Reciprocal Rank Fusion algorithm |
| `reranker.py` | LLM-based re-ranking for precision |
| `ingestion.py` | Document chunking and ingestion |

## Dependencies
- `vectorstores/` — pgvector dense search
- `integrations/model_router` — LLM for re-ranking
- PostgreSQL full-text search indices

## Extension Strategy
1. Add new retrieval strategies by implementing search method
2. Swap re-ranker model via model router configuration
3. Add metadata filters in `hybrid_retriever.py`
4. Adjust fusion weights via settings
