"""Cache service using Redis for high-performance TTL caching."""

from __future__ import annotations

import json
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar, ParamSpec

from backend.src.shared.redis_client import redis_manager

logger = logging.getLogger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


class CacheService:
    """Provides structured GET/SET caching utilities over Redis with JSON formatting."""

    def __init__(self) -> None:
        self._client = redis_manager.get_client()

    async def get(self, key: str) -> Any | None:
        """Fetch and parse JSON cached item from Redis."""
        try:
            val = await self._client.get(key)
            if val is not None:
                return json.loads(val)
        except Exception as exc:
            logger.error(f"Error fetching cache key '{key}': {exc}")
        return None

    async def set(self, key: str, value: Any, ttl_sec: int = 3600) -> bool:
        """Persist serializable value to Redis with time-to-live parameter."""
        try:
            serialized = json.dumps(value)
            await self._client.set(key, serialized, ex=ttl_sec)
            return True
        except Exception as exc:
            logger.error(f"Error writing cache key '{key}': {exc}")
            return False

    async def delete(self, key: str) -> bool:
        """Invalidate cache key."""
        try:
            await self._client.delete(key)
            return True
        except Exception as exc:
            logger.error(f"Error invalidating cache key '{key}': {exc}")
            return False


cache_service = CacheService()


def cached_result(ttl_sec: int = 3600, key_prefix: str = "cache") -> Callable[
    [Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, T]]
]:
    """Decorator to transparently cache async coroutine returns in Redis."""

    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Construct deterministic cache key
            args_str = "-".join([str(a) for a in args[1:]])  # Skip self
            kwargs_str = "-".join(
                [f"{k}:{v}" for k, v in sorted(kwargs.items())]
            )
            key = f"{key_prefix}:{func.__name__}:{args_str}:{kwargs_str}"

            cached = await cache_service.get(key)
            if cached is not None:
                logger.debug(f"Cache Hit for key: {key}")
                return cached

            logger.debug(f"Cache Miss for key: {key}. Executing coroutine.")
            res = await func(*args, **kwargs)
            await cache_service.set(key, res, ttl_sec)
            return res

        return wrapper

    return decorator
overrides = {}
