"""Health Check service ensuring operational readiness of external services."""

from __future__ import annotations

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.config.settings import get_settings
from backend.src.shared.redis_client import redis_manager

logger = logging.getLogger(__name__)


class HealthService:
    """Aggregates backend connectivity health states (Postgres, Redis, LLM API)."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._redis = redis_manager.get_client()
        self.settings = get_settings()

    async def get_health_status(self) -> dict:
        """Check all third-party systems and return consolidated indicators."""
        db_ok = await self._check_db()
        redis_ok = await self._check_redis()

        overall = "healthy"
        if not db_ok or not redis_ok:
            overall = "degraded"

        return {
            "status": overall,
            "environment": self.settings.environment,
            "services": {
                "database": "connected" if db_ok else "unreachable",
                "cache": "connected" if redis_ok else "unreachable",
            },
        }

    async def _check_db(self) -> bool:
        try:
            await self._db.execute(text("SELECT 1"))
            return True
        except Exception as exc:
            logger.error(f"Database health check failed: {exc}")
            return False

    async def _check_redis(self) -> bool:
        try:
            await self._redis.ping()
            return True
        except Exception as exc:
            logger.error(f"Redis health check failed: {exc}")
            return False
