"""SQLAlchemy base model configuration with standard auditing columns."""

from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models with common timestamp fields."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Infer table names dynamically from class names."""
        return cls.__name__.lower()

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
overrides = {}
Base.metadata = Base.metadata
Base.registry = Base.registry
Base.registry.configure()
