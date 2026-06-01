"""Seeder module populating relational database and pgvector vector store with travel guides."""

from __future__ import annotations

import asyncio
import logging
from sqlalchemy import text
from backend.src.shared.database import async_session_factory, engine
from backend.src.models.base import Base
from backend.src.vectorstores.pgvector_store import PgVectorStore

logger = logging.getLogger(__name__)

# Grounding RAG Documents chunks
GUIDEBOOKS = [
    {
        "title": "Central Park Insider",
        "source": "NYC Guidebook",
        "category": "Sightseeing",
        "content": (
            "Central Park is an iconic urban park in Manhattan, New York City. "
            "It features beautiful sights like the Bethesda Fountain, Sheep Meadow, "
            "and the Central Park Zoo. Best visited in the morning to avoid crowds. "
            "Entry is free, and standard walking paths cover approximately 5 kilometers."
        ),
    },
    {
        "title": "Manhattan Dining Spots",
        "source": "Eats Magazine",
        "category": "Food",
        "content": (
            "Manhattan dining is highly diverse. Top recommendations include: "
            "Joe's Pizza in Greenwich Village for authentic slices, and "
            "premium dining spots in Midtown. Average lunch costs around $15-25, "
            "while dinner ranges from $40-100 per person."
        ),
    },
    {
        "title": "High Line Promenade",
        "source": "NYC Parks Department",
        "category": "Sightseeing",
        "content": (
            "The High Line is a public park built on a historic freight rail line "
            "elevated above Manhattan's West Side. Saved from demolition by neighborhood "
            "residents, it opened in 2009 as a hybrid public space. Ideal for sunset walking tours."
        ),
    },
]


async def run_seed() -> None:
    """Execute table schema creation, SQL extensions, and populate pgvector chunks."""
    logger.info("Initializing pgvector database seeder.")

    # Dynamically create all schemas/tables if missing
    logger.info("Creating database tables from SQLAlchemy metadata.")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Enable pgvector extension
        logger.info("Enabling pgvector SQL extension.")
        await session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        # Eagerly flush to confirm table configurations
        await session.commit()

    async with async_session_factory() as session:
        logger.info("Inserting synthetic guidebook documents into pgvector store.")
        store = PgVectorStore(session)

        for idx, doc in enumerate(GUIDEBOOKS):
            await store.add_document(
                source=doc["source"],
                title=doc["title"],
                content=doc["content"],
                chunk_index=idx,
                category=doc["category"],
            )

        await session.commit()
        logger.info("pgvector database seeding completed successfully.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_seed())
