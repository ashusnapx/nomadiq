"""Rate limiting middleware for NomadIQ API."""

import time
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.config import settings
from src.exceptions.api_errors import RateLimitError


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Token-bucket rate limiter per client IP address."""

    def __init__(self, app: object) -> None:
        super().__init__(app)  # type: ignore[arg-type]
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._window: int = 60

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Check rate limit before processing the request."""
        if request.url.path == "/health":
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self._window

        self._requests[client_ip] = [
            ts for ts in self._requests[client_ip] if ts > window_start
        ]

        if len(self._requests[client_ip]) >= settings.rate_limit_per_minute:
            raise RateLimitError()

        self._requests[client_ip].append(now)
        return await call_next(request)
