# Vector Stores

## Purpose
PostgreSQL + pgvector backed vector storage for RAG retrieval.
Production-grade alternative to ChromaDB — uses the same database as application data.

## Ownership
AI/ML Engineering Team

## Dependencies
- `pgvector` Python package
- PostgreSQL with `vector` extension enabled
- OpenAI Embeddings API (text-embedding-3-small)

## Components
| File | Responsibility |
|------|---------------|
| `models.py` | SQLAlchemy model with pgvector column |
| `embeddings.py` | OpenAI embedding generation with cost tracking |
| `pgvector_store.py` | Dense similarity search operations |

## Extension Strategy
1. Add new embedding models by updating `EmbeddingService`
2. Add new search strategies by extending `PgVectorStore`
3. Custom metadata filtering via additional WHERE clauses
