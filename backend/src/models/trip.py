"""Trip database model containing constraints and traveler information."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float, Enum, JSON
from sqlalchemy.orm import relationship

from backend.src.models.base import Base
from backend.src.domain.enums import TripStatus, TravelerPersona


class Trip(Base):
    """Represents a planned or active trip entity."""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False, index=True)
    start_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    end_date = Column(String(10), nullable=False)    # YYYY-MM-DD
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    status = Column(
        Enum(TripStatus), default=TripStatus.PLANNING, nullable=False
    )
    persona = Column(
        Enum(TravelerPersona), default=TravelerPersona.BALANCED, nullable=False
    )
    preferences = Column(JSON, default=dict, nullable=False)

    # Relationships
    itineraries = relationship(
        "Itinerary", back_populates="trip", cascade="all, delete-orphan"
    )
    events = relationship(
        "Event", back_populates="trip", cascade="all, delete-orphan"
    )
    sessions = relationship(
        "Session", back_populates="trip", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Trip(id={self.id}, title='{self.title}', destination='{self.destination}')>"
