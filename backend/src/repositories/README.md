# Repositories Layer

## Purpose
Decouples data access and query mechanics from the high-level business service layer using standard Generic Repository patterns.

## Ownership
Database Operations Team

## Structure
- `base.py`: Shared generic generic database actions.
- `trip_repository.py`: Custom trip lookup routines.
- `itinerary_repository.py`: Itinerary sub-selection and eager loading queries.
- `event_repository.py`: Disruption filtering.
- `session_repository.py`: Message thread retrievals.

## Extension Strategy
Add specialized queries to relevant repository classes, utilizing async select constructs. Export via `__init__.py`. Keep database sessions bound to FastAPI requests.
