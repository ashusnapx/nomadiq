"""Pydantic validation schemas for Trip resources."""

from __future__ import annotations

from pydantic import BaseModel, Field
from backend.src.domain.enums import TripStatus, TravelerPersona


class TripBase(BaseModel):
    """Shared base properties for trip entities."""

    title: str = Field(..., max_length=255)
    destination: str = Field(..., max_length=255)
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    end_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")    # YYYY-MM-DD
    budget_min: float = Field(..., gt=0.0)
    budget_max: float = Field(..., gt=0.0)
    persona: TravelerPersona = Field(default=TravelerPersona.BALANCED)
    preferences: dict = Field(default_factory=dict)


class TripCreate(TripBase):
    """Input payload for generating a new Trip resource."""

    pass


class TripUpdate(BaseModel):
    """Optional modification schema for existing trips."""

    title: str | None = None
    status: TripStatus | None = None
    preferences: dict | None = None


class TripResponse(TripBase):
    """Complete serialized Trip representation returned to API consumers."""

    id: int
    status: TripStatus
    created_at: Any = None
    updated_at: Any = None

    class Config:
        from_attributes = True
