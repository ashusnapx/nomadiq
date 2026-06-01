"""Schemas package exporting validation and response contracts."""

from __future__ import annotations

from backend.src.schemas.common import HealthResponse, ErrorResponse, PaginatedResponse
from backend.src.schemas.trip import TripCreate, TripUpdate, TripResponse
from backend.src.schemas.itinerary import ItineraryResponse, ActivityResponse, DayPlan
from backend.src.schemas.event import EventCreate, EventResponse, ImpactAnalysis
from backend.src.schemas.agent import AgentTraceResponse, AgentStepResponse
from backend.src.schemas.evaluation import EvalMetrics, EvalReport, BenchmarkResult
from backend.src.schemas.whatif import WhatIfRequest, WhatIfResponse, ScenarioResult

__all__ = [
    "HealthResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "TripCreate",
    "TripUpdate",
    "TripResponse",
    "ItineraryResponse",
    "ActivityResponse",
    "DayPlan",
    "EventCreate",
    "EventResponse",
    "ImpactAnalysis",
    "AgentTraceResponse",
    "AgentStepResponse",
    "EvalMetrics",
    "EvalReport",
    "BenchmarkResult",
    "WhatIfRequest",
    "WhatIfResponse",
    "ScenarioResult",
]
