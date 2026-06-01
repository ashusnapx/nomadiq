"""Exceptions raised by domain business logic layer."""

from __future__ import annotations

from backend.src.exceptions.base import NomadIQError


class BudgetExceededError(NomadIQError):
    """Raised when the calculated trip cost exceeds traveler constraints."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=400, error_code="BUDGET_EXCEEDED")


class ItineraryNotFoundError(NomadIQError):
    """Raised when requested itinerary record is not found."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=404, error_code="ITINERARY_NOT_FOUND")


class WeatherServiceError(NomadIQError):
    """Raised when external weather API failures occur."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=502, error_code="WEATHER_SERVICE_ERROR")


class TransportServiceError(NomadIQError):
    """Raised when transportation routes cannot be planned."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail, status_code=502, error_code="TRANSPORT_SERVICE_ERROR")
