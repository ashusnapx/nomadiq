"""Exceptions mapped to standard HTTP API status boundaries."""

from __future__ import annotations

from backend.src.exceptions.base import NomadIQError


class ValidationError(NomadIQError):
    """Raised when request payload or internal variables fail validation checks."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=400, error_code="VALIDATION_ERROR")


class NotFoundError(NomadIQError):
    """Raised when database or cache entities are missing."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=404, error_code="NOT_FOUND")


class RateLimitError(NomadIQError):
    """Raised when client exceeds rate limits."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=429, error_code="RATE_LIMIT_EXCEEDED")


class AuthenticationError(NomadIQError):
    """Raised when authentication credentials fail validation."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=401, error_code="UNAUTHORIZED")
