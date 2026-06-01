"""Application startup and shutdown lifecycle handlers."""

import logging

from fastapi import FastAPI

from src.config import settings
from src.shared.database import engine
from src.shared.redis_client import redis_manager

logger = logging.getLogger(__name__)


async def run_startup(app: FastAPI) -> None:
    """Execute startup tasks: verify database and redis connections."""
    logging.basicConfig(level=getattr(logging, settings.log_level))
    logger.info("Starting NomadIQ in %s mode", settings.environment)

    app.state.db_engine = engine
    app.state.redis = await redis_manager.connect()
    logger.info("All services connected successfully")


async def run_shutdown(app: FastAPI) -> None:
    """Execute shutdown tasks: close database and redis connections."""
    logger.info("Shutting down NomadIQ")
    await redis_manager.disconnect()
    await engine.dispose()
    logger.info("All connections closed")
