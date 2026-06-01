"""Common API response schemas including health, pagination, and standardized errors."""

from __future__ import annotations

from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Aggregated platform health status indicator."""

    status: str
    version: str
    environment: str
    details: dict[str, str]


class ErrorDetails(BaseModel):
    """Details of a request failure."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standardized API error response format."""

    success: bool = False
    error: ErrorDetails


class PaginatedResponse(BaseModel, Generic[T]):
    """Standardized pagination envelope."""

    items: list[T]
    total: int
    page: int
    size: int
    pages: int
