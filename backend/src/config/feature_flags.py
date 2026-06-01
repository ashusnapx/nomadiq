"""Dynamic feature flag management framework."""

from __future__ import annotations

import json
from typing import Any
from backend.src.config.settings import get_settings


class FeatureFlagRegistry:
    """Feature flag system allowing overrides via settings and database/cache."""

    def __init__(self) -> None:
        self._defaults = {
            "ENABLE_WEATHER_AGENT": True,
            "ENABLE_REPLANNING": True,
            "ENABLE_RAG": True,
            "ENABLE_EVALUATION": True,
            "ENABLE_LANGSMITH": False,
            "ENABLE_COST_TRACKING": True,
            "ENABLE_WHAT_IF": True,
            "EXPERIMENTAL_PROMPTS": False,
            "HYBRID_SEARCH_RRF": True,
        }
        self._overrides: dict[str, bool] = {}

    def is_enabled(self, flag: str) -> bool:
        """Check if a specific feature flag is currently active."""
        if flag in self._overrides:
            return self._overrides[flag]

        # Read default
        return self._defaults.get(flag, False)

    def set_override(self, flag: str, value: bool) -> None:
        """Dynamically override a feature flag in-memory."""
        if flag in self._defaults:
            self._overrides[flag] = value

    def clear_overrides(self) -> None:
        """Clear all runtime flag overrides."""
        self._overrides.clear()

    def get_all_flags(self) -> dict[str, bool]:
        """Retrieve state of all registered feature flags."""
        return {k: self.is_enabled(k) for k in self._defaults}


feature_flags = FeatureFlagRegistry()
