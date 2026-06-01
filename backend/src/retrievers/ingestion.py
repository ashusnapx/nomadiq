"""Document ingestion pipeline for the RAG knowledge base."""

from __future__ import annotations

from backend.src.config.settings import get_settings
from backend.src.vectorstores.pgvector_store import PgVectorStore


class DocumentChunker:
    """Split documents into overlapping chunks for embedding."""

    def __init__(self) -> None:
        settings = get_settings()
        self._chunk_size = settings.chunk_size
        self._overlap = settings.chunk_overlap

    def chunk_text(self, text: str, source: str, title: str, category: str = "general") -> list[dict]:
        """Split text into overlapping chunks with metadata."""
        words = text.split()
        chunks = []
        start = 0
        idx = 0

        while start < len(words):
            end = start + self._chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "source": source,
                "title": title,
                "content": chunk_text,
                "chunk_index": idx,
                "category": category,
                "metadata": {
                    "word_count": len(chunk_words),
                    "char_count": len(chunk_text),
                },
            })

            start = end - self._overlap
            idx += 1

        return chunks


class IngestionPipeline:
    """Ingest documents into the vector store."""

    def __init__(self, store: PgVectorStore) -> None:
        self._store = store
        self._chunker = DocumentChunker()

    async def ingest_document(
        self, text: str, source: str, title: str, category: str = "general"
    ) -> int:
        """Ingest a single document: chunk, embed, and store."""
        chunks = self._chunker.chunk_text(text, source, title, category)
        stored = await self._store.add_batch(chunks)
        return len(stored)

    async def ingest_batch(self, documents: list[dict]) -> int:
        """Ingest multiple documents."""
        total = 0
        for doc in documents:
            count = await self.ingest_document(
                text=doc["text"],
                source=doc["source"],
                title=doc["title"],
                category=doc.get("category", "general"),
            )
            total += count
        return total
