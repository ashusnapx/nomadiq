"""Session database model to capture persistent traveler context and logs."""

from __future__ import annotations

from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.src.models.base import Base


class Session(Base):
    """Stores the conversational and context history of a trip planning session."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    messages = Column(JSON, default=list, nullable=False)
    context = Column(JSON, default=dict, nullable=False)

    # Relationships
    trip = relationship("Trip", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, trip_id={self.trip_id})>"
