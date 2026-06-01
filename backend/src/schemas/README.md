# Schemas Layer

## Purpose
Defines strictly typed Pydantic structures acting as API contracts, preventing malformed payload delivery at application boundaries.

## Ownership
Engineering Platform Team

## Structure
- `common.py`: Standard pagination, error wrappers, and health models.
- `trip.py`: Inputs and outputs for trip creation and modification.
- `itinerary.py`: Daily plans and activities.
- `event.py`: Active disruptions.
- `agent.py`: Tracing structures.
- `evaluation.py`: Automated benchmarking and evaluation metrics.
- `whatif.py`: What-if simulation parameters.

## Extension Strategy
Add new schemas or fields directly to relevant files. Export classes via `__init__.py`. Ensure standard field validation rules are followed.
