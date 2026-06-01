# Services Layer

## Purpose
Exposes modular transactional APIs coordinates workflows, database operations, caching mechanisms, dynamic event responses, and simulations.

## Ownership
Engineering Platform Team

## Structure
- `trip_service.py`: Trip CRUD.
- `itinerary_service.py`: Multi-variant itinerary compilers.
- `budget_service.py`: Allocations and optimizations.
- `event_service.py`: Active disruptions handler.
- `session_service.py`: Context and conversation management.
- `whatif_service.py`: Travel Simulation engine.
- `cache_service.py`: Redis wrappers and cache decorators.
- `health_service.py`: Liveness diagnostics checks.

## Extension Strategy
Introduce business logic methods to target service classes, keeping them under 100-150 lines. Inject repositories using request-scoped db sessions. Export via `__init__.py`.
