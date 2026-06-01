"""OpenTelemetry instrumentation setup for NomadIQ."""

import logging

from fastapi import FastAPI

from src.config import settings

logger = logging.getLogger(__name__)


def setup_telemetry(app: FastAPI) -> None:
    """Configure OpenTelemetry tracing and instrumentation."""
    if settings.environment == "testing":
        logger.info("Skipping telemetry setup in testing environment")
        return

    try:
        from opentelemetry import trace
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider

        resource = Resource.create(
            {"service.name": "nomadiq-backend", "service.version": "0.1.0"}
        )
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry instrumentation enabled")
    except ImportError:
        logger.warning("OpenTelemetry packages not installed, skipping")
