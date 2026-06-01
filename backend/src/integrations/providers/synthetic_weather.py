"""Deterministic synthetic weather provider for testing and graceful offline operations."""

from __future__ import annotations

import hashlib
from typing import Any
from backend.src.integrations.plugin_system import WeatherProvider


class SyntheticWeatherProvider(WeatherProvider):
    """Generates realistic, deterministic weather forecasts based on destination name hashes."""

    async def get_forecast(
        self, destination: str, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch weather data for target date ranges."""
        # Standard hash-seeding for consistency
        seed = int(hashlib.sha256(destination.encode()).hexdigest(), 16) % 100
        temp = 15 + (seed % 15)  # Range 15 to 30 C
        conditions = ["Sunny", "Cloudy", "Rainy", "Sunny", "Cloudy"]
        cond = conditions[seed % len(conditions)]

        return {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "forecast": [
                {
                    "day": 1,
                    "condition": cond,
                    "temperature_c": temp,
                    "precipitation_probability": 80 if cond == "Rainy" else 10,
                },
                {
                    "day": 2,
                    "condition": "Sunny",
                    "temperature_c": temp + 2,
                    "precipitation_probability": 5,
                },
            ],
            "overall_weather_favorability": 0.85 if cond != "Rainy" else 0.45,
        }
overrides = {}
