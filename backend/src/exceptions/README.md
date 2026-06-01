# Exception Layer

## Purpose
Establishes clear application error boundaries and maps custom failures to standardized JSON API response schemas.

## Ownership
Engineering Platform Team

## Structure
- `base.py`: The root `NomadIQError` model.
- `agent_errors.py`: Faults relating to AI orchestration or templates.
- `api_errors.py`: Typical client-side errors (4xx validation/limits).
- `service_errors.py`: Concrete business rules violations.
- `handlers.py`: Global handlers wired to FastAPI.

## Extension Strategy
Inherit from `NomadIQError` in `base.py`, provide a unique default `error_code` string and map it to an appropriate HTTP status code. Register in relevant files.
