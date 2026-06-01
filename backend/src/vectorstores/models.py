"""pgvector-based vector store for hybrid retrieval."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from backend.src.models.base import Base
from backend.src.config.settings import get_settings


class DocumentChunk(Base):
    """Stores embedded document chunks for RAG retrieval."""

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(512), nullable=False, index=True)
    title = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
    metadata_ = Column("metadata", JSONB, default=dict)
    category = Column(String(128), index=True)
    bm25_tokens = Column(Text, nullable=True)
    relevance_score = Column(Float, default=0.0)

    def __repr__(self) -> str:
        return f"<DocumentChunk(id={self.id}, source='{self.source}')>"
