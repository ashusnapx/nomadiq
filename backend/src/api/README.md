# API Layer

## Purpose
Exposes public REST pathways and websockets endpoints structured as clean OpenAPI resources, carrying logging and rate limiting middlewares.

## Ownership
Engineering Platform Team

## Structure
- `middleware.py`: Request logging and sliding window rate limiting.
- `routes/`: Decoupled routers for `trips`, `itineraries`, `events`, `simulations` and `observability`.

## Extension Strategy
Add standard path endpoints using APIRouter in target files inside `routes/`. Connect new routers to the core `api_router` inside `__init__.py`.
