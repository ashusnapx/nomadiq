"""Itinerary database model linking trip instances to specific cost variants."""

from __future__ import annotations

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship

from backend.src.models.base import Base
from backend.src.domain.enums import PlanVariant


class Itinerary(Base):
    """Itinerary variants associated with distinct cost models (A/B/C)."""

    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    variant = Column(
        Enum(PlanVariant), default=PlanVariant.A, nullable=False
    )
    confidence_score = Column(Float, default=1.0, nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

    # Relationships
    trip = relationship("Trip", back_populates="itineraries")
    activities = relationship(
        "Activity", back_populates="itinerary", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Itinerary(id={self.id}, trip_id={self.trip_id}, variant='{self.variant}')>"
