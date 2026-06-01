"""Pydantic validation schemas for real-time disruption events."""

from __future__ import annotations

from pydantic import BaseModel, Field
from backend.src.domain.enums import EventType


class ImpactAnalysis(BaseModel):
    """Impact analysis model detailing which itinerary aspects are impacted."""

    affected_activity_ids: list[int] = []
    severity: str
    description: str
    replan_recommended: bool


class EventCreate(BaseModel):
    """Payload representing a newly triggered event disruption."""

    event_type: EventType
    severity: str = Field(default="warning", pattern="^(info|warning|critical)$")
    description: str
    payload: dict = Field(default_factory=dict)


class EventResponse(BaseModel):
    """Serialized representations of active or historical disruptions."""

    id: int
    trip_id: int
    event_type: EventType
    severity: str
    description: str
    detected_at: Any
    resolved_at: Any | None = None
    impact_analysis: ImpactAnalysis

    class Config:
        from_attributes = True
