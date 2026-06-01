"""Event database model mapping unexpected trip disruptions."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship

from backend.src.models.base import Base
from backend.src.domain.enums import EventType


class Event(Base):
    """Represents a disruption event impacting a planned trip."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type = Column(Enum(EventType), nullable=False)
    severity = Column(String(50), nullable=False)  # info, warning, critical
    description = Column(Text, nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    impact_analysis = Column(JSON, default=dict, nullable=False)

    # Relationships
    trip = relationship("Trip", back_populates="events")

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, type='{self.event_type}', severity='{self.severity}')>"
