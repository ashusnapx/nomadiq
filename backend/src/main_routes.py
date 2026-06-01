"""Route registration for NomadIQ API."""

from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    """Register all API routers with the application.

    Routers are added here as they are built. Each router module
    defines its own prefix and tags.
    """
    # Future router registrations:
    # from src.api.trips import router as trips_router
    # app.include_router(trips_router, prefix="/api/v1")
    _ = app  # routes will be registered as API layer is built
