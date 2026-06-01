# Database Models

## Purpose
Defines SQLAlchemy relational database structures mapping domain travel entities into PostgreSQL tables.

## Ownership
Database Operations Team

## Structure
- `base.py`: The base class carrying global `created_at` and `updated_at` properties.
- `trip.py`: Top-level trip details.
- `itinerary.py`: Segment variants with scores and totals.
- `activity.py`: Scheduled events.
- `event.py`: Active interruptions.
- `session.py`: Persistent chat logs.

## Extension Strategy
Add new fields to individual classes as normal SQLAlchemy column definitions. Run standard migrations.
