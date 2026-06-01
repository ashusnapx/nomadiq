"""Plugin System defining swappable API provider contracts."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class WeatherProvider(ABC):
    """Abstract contract for weather updates."""

    @abstractmethod
    async def get_forecast(
        self, destination: str, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch weather forecasts."""
        pass


class TransportProvider(ABC):
    """Abstract contract for route planning."""

    @abstractmethod
    async def plan_route(
        self, origin: str, destination: str, mode: str
    ) -> dict[str, Any]:
        """Fetch transport routing options."""
        pass


class MapProvider(ABC):
    """Abstract contract for location geocoding."""

    @abstractmethod
    async def geocode(self, location: str) -> tuple[float, float]:
        """Map city names to geographic coordinates."""
        pass


class PluginRegistry:
    """Manages active third-party provider instances dynamically."""

    def __init__(self) -> None:
        self._providers: dict[str, Any] = {}

    def register(self, key: str, provider: Any) -> None:
        """Bind a concrete provider instance to target key."""
        self._providers[key] = provider
        logger.info(f"Registered plugin provider: {key} -> {provider.__class__.__name__}")

    def get(self, key: str) -> Any:
        """Fetch registered provider instance by key."""
        if key not in self._providers:
            raise KeyError(f"Plugin provider '{key}' not found.")
        return self._providers[key]


plugin_registry = PluginRegistry()
