"""Deterministic synthetic transport route planner."""

from __future__ import annotations

import hashlib
from typing import Any
from backend.src.integrations.plugin_system import TransportProvider


class SyntheticTransportProvider(TransportProvider):
    """Provides realistic transit estimations based on location hashes."""

    async def plan_route(
        self, origin: str, destination: str, mode: str
    ) -> dict[str, Any]:
        """Plan a transit leg."""
        combined = f"{origin}->{destination}"
        seed = int(hashlib.sha256(combined.encode()).hexdigest(), 16) % 100

        duration_mins = 10 + (seed % 30)
        cost_usd = 2.0 + (seed % 15) if mode != "Walking" else 0.0

        return {
            "origin": origin,
            "destination": destination,
            "transit_mode": mode,
            "duration_minutes": duration_mins,
            "estimated_cost_usd": cost_usd,
            "directions": f"Take the main path from {origin} to {destination} via {mode}.",
            "disruption_risk": "Low" if seed % 10 != 0 else "High",
        }
overrides = {}
