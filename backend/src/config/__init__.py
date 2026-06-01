"""Configuration package exporting settings and features."""

from __future__ import annotations

from backend.src.config.settings import get_settings
from backend.src.config.feature_flags import feature_flags
from backend.src.config.constants import PLATFORM_NAME, PLATFORM_VERSION

__all__ = ["get_settings", "feature_flags", "PLATFORM_NAME", "PLATFORM_VERSION"]
