"""Activity database model defining single scheduled timeline events."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.src.models.base import Base


class Activity(Base):
    """Represents a scheduled item in an itinerary."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    itinerary_id = Column(
        Integer,
        ForeignKey("itineraries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    day_number = Column(Integer, nullable=False)
    time_slot = Column(String(50), nullable=False)  # Morning, Lunch, Afternoon, etc.
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    cost = Column(Float, default=0.0, nullable=False)
    category = Column(String(100), nullable=False)
    explanation = Column(Text, nullable=True)
    citations = Column(JSON, default=list, nullable=False)
    risk_score = Column(Float, default=1.0, nullable=False)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, name='{self.name}', cost={self.cost})>"
