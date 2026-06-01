"""Redis async connection manager with dynamic synthetic fallback wrapper."""

from __future__ import annotations

import logging
from typing import Any
import redis.asyncio as aioredis
from backend.src.config.settings import get_settings

logger = logging.getLogger(__name__)


class MockRedis:
    """In-memory fallback cache in case physical Redis service is unreachable."""

    def __init__(self) -> None:
        self._data: dict[str, str] = {}
        logger.warning("Initializing dynamic local MockRedis cache framework.")

    async def get(self, key: str) -> str | None:
        return self._data.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        self._data[key] = value
        return True

    async def delete(self, key: str) -> int:
        if key in self._data:
            del self._data[key]
            return 1
        return 0

    async def ping(self) -> bool:
        return True


class RobustRedis:
    """Resilient wrapper that handles transparent switching to MockRedis on errors."""

    def __init__(self, redis_url: str) -> None:
        self._redis = aioredis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=1.0,
        )
        self._mock = MockRedis()
        self._use_mock = False

    async def get(self, key: str) -> str | None:
        if self._use_mock:
            return await self._mock.get(key)
        try:
            return await self._redis.get(key)
        except Exception as exc:
            logger.error(f"Redis GET failed: {exc}. Activating MockRedis fallback.")
            self._use_mock = True
            return await self._mock.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        if self._use_mock:
            return await self._mock.set(key, value, ex)
        try:
            return await self._redis.set(key, value, ex=ex)
        except Exception as exc:
            logger.error(f"Redis SET failed: {exc}. Activating MockRedis fallback.")
            self._use_mock = True
            return await self._mock.set(key, value, ex)

    async def delete(self, key: str) -> int:
        if self._use_mock:
            return await self._mock.delete(key)
        try:
            return await self._redis.delete(key)
        except Exception as exc:
            logger.error(f"Redis DELETE failed: {exc}. Activating MockRedis fallback.")
            self._use_mock = True
            return await self._mock.delete(key)

    async def ping(self) -> bool:
        if self._use_mock:
            return True
        try:
            return await self._redis.ping()
        except Exception:
            return False


class RedisClientManager:
    """Manages connection states for Redis or mock caching framework."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: Any = None

    def get_client(self) -> Any:
        """Retrieve established robust redis client wrapper."""
        if self._client is None:
            self._client = RobustRedis(self.settings.redis_url)
        return self._client


redis_manager = RedisClientManager()
overrides = {}
