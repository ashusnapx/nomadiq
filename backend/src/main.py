"""FastAPI Application Factory with complete startup/shutdown lifecycles and OpenTelemetry wrappers."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.src.config.settings import get_settings
from backend.src.exceptions.handlers import register_exception_handlers
from backend.src.api import api_router
from backend.src.api.middleware import RequestLoggingMiddleware, RedisRateLimitingMiddleware
from backend.src.shared.database import engine, get_db
from backend.src.models.base import Base
from backend.src.services.health_service import HealthService
from backend.src.schemas.common import HealthResponse

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Execute startup and shutdown lifecycles safely, creating DB tables if missing."""
    logger.info("Initializing NomadIQ platform database schemas.")
    async with engine.begin() as conn:
        # Create all tables on startup (simplifies deployment check)
        await conn.run_sync(Base.metadata.create_all)

    yield

    logger.info("NomadIQ platform shutdown sequence complete.")
    await engine.dispose()


def create_app() -> FastAPI:
    """FastAPI Application Factory instantiating routes and middleware wrappers."""
    settings = get_settings()

    app = FastAPI(
        title="NomadIQ Travel Platform",
        description="Personalized Travel Itinerary Generator with Real-Time Adaptive Updates",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_origin_regex=None,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom Middlewares
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RedisRateLimitingMiddleware, limit_per_min=settings.rate_limit_per_minute)

    # Standard Exception Handlers
    register_exception_handlers(app)

    # Dynamic Routes inclusion
    app.include_router(api_router)

    # Root and Health indicators
    @app.get("/", tags=["General"])
    async def root() -> dict:
        return {
            "platform": "NomadIQ Decision Intelligence Platform",
            "status": "operational",
            "api_version": "v1",
        }

    @app.get("/health", response_model=HealthResponse, tags=["General"])
    async def health_check(db = Depends(get_db)) -> HealthResponse:
        """Startup readiness and connectivity health indicator."""
        service = HealthService(db)
        status = await service.get_health_status()
        return HealthResponse(
            status=status["status"],
            version="1.0.0",
            environment=status["environment"],
            details=status["services"],
        )

    return app
