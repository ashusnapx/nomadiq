"""Integrations package exposing the Model Router, Plugin System and default providers."""

from __future__ import annotations

from backend.src.integrations.model_router import ModelRouter, TaskComplexity
from backend.src.integrations.plugin_system import (
    plugin_registry,
    WeatherProvider,
    TransportProvider,
    MapProvider,
)
from backend.src.integrations.providers.synthetic_weather import SyntheticWeatherProvider
from backend.src.integrations.providers.synthetic_transport import (
    SyntheticTransportProvider,
)
from backend.src.integrations.providers.synthetic_maps import SyntheticMapProvider

# Register default plugins at startup
plugin_registry.register("weather", SyntheticWeatherProvider())
plugin_registry.register("transport", SyntheticTransportProvider())
plugin_registry.register("maps", SyntheticMapProvider())

__all__ = [
    "ModelRouter",
    "TaskComplexity",
    "plugin_registry",
    "WeatherProvider",
    "TransportProvider",
    "MapProvider",
]
