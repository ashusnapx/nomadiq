"""API Middleware layer containing rate limiting and logging utilities."""

from __future__ import annotations

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.src.exceptions.api_errors import RateLimitError
from backend.src.shared.redis_client import redis_manager

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs latency, status code, and target pathways for incoming requests."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {duration:.2f}ms"
        )
        return response


class RedisRateLimitingMiddleware(BaseHTTPMiddleware):
    """Enforces client request limits using a sliding window in Redis."""

    def __init__(self, app: Any, limit_per_min: int = 60) -> None:
        super().__init__(app)
        self.limit = limit_per_min
        self.redis = redis_manager.get_client()

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        ip = request.client.host if request.client else "unknown-ip"
        key = f"ratelimit:{ip}"

        try:
            # Multi-command pipeline for atomic updates
            async with self.redis.pipeline(transaction=True) as pipe:
                now = time.time()
                window_start = now - 60
                await pipe.zremrangebyscore(key, 0, window_start)
                await pipe.zadd(key, {str(now): now})
                await pipe.zcard(key)
                await pipe.expire(key, 60)
                res = await pipe.execute()
                count = res[2]

            if count > self.limit:
                raise RateLimitError(
                    f"Too many requests. Limit is {self.limit} per minute."
                )
        except RateLimitError as exc:
            raise exc
        except Exception as exc:
            logger.error(f"Rate limiter bypass due to Redis error: {exc}")

        return await call_next(request)


from typing import Any
overrides = {}
