"""Deterministic synthetic geocoding map service."""

from __future__ import annotations

import hashlib
from backend.src.integrations.plugin_system import MapProvider


class SyntheticMapProvider(MapProvider):
    """Translates street addresses to deterministic lat/long geocodes."""

    async def geocode(self, location: str) -> tuple[float, float]:
        """Geocode text query to lat/long coordinates."""
        seed = int(hashlib.sha256(location.encode()).hexdigest(), 16)

        # NYC-centric coordinates by default for realistic mock displays
        lat = 40.7128 + ((seed % 1000) / 10000.0)
        lng = -74.0060 + (((seed >> 4) % 1000) / 10000.0)

        return (lat, lng)
overrides = {}
