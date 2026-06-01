"""Database setup providing async engine and session dependencies."""

from __future__ import annotations

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.src.config.settings import get_settings

# Create asynchronous engine mapping pgvector support
settings = get_settings()
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_size=20,
    max_overflow=10,
)

# Async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding isolated database sessions."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
overrides = {}
