"""Application static constraints and business rule constants."""

from __future__ import annotations

# Platform Metadata
PLATFORM_NAME = "NomadIQ Decision Intelligence Platform"
PLATFORM_VERSION = "1.0.0"

# Routing Constraints
DEFAULT_WALKING_SPEED_KMPH = 4.5
RUSH_HOUR_START_HOUR = 8
RUSH_HOUR_END_HOUR = 18

# Caching Thresholds (TTL in seconds)
CACHE_TTL_WEATHER = 1800      # 30 mins
CACHE_TTL_TRANSPORT = 3600    # 1 hour
CACHE_TTL_RAG_CONTEXT = 7200  # 2 hours
CACHE_TTL_LLM_OUTPUT = 3600   # 1 hour

# Safety Limits
MIN_TRIP_DAYS = 1
MAX_TRIP_DAYS = 14
DEFAULT_PERSONA = "Balanced Traveler"
MIN_BUDGET_USD = 100.0

# Alert Levels
ALERT_SEVERITY_INFO = "info"
ALERT_SEVERITY_WARNING = "warning"
ALERT_SEVERITY_CRITICAL = "critical"
