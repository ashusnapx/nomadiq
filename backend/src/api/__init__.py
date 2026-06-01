"""API package exporting routers and middleware setups."""

from __future__ import annotations

from fastapi import APIRouter
from backend.src.api.routes.trips import router as trips_router
from backend.src.api.routes.itineraries import router as itineraries_router
from backend.src.api.routes.events import router as events_router
from backend.src.api.routes.simulations import router as simulations_router
from backend.src.api.routes.observability import router as observability_router

# Aggregated api router
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(trips_router)
api_router.include_router(itineraries_router)
api_router.include_router(events_router)
api_router.include_router(simulations_router)
api_router.include_router(observability_router)

__all__ = ["api_router"]
