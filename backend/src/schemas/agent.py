"""Pydantic validation schemas to expose agent telemetry and execution logs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AgentStepResponse(BaseModel):
    """Telemetry capturing a single step in a multi-agent execution pipeline."""

    agent_name: str
    model_used: str
    tokens: dict = Field(default_factory=dict)  # {"prompt_tokens": int, "completion_tokens": int}
    latency_ms: float
    timestamp: str


class AgentTraceResponse(BaseModel):
    """Consolidated traces representing a full trip compilation session."""

    trace_id: str
    trip_id: int
    steps: list[AgentStepResponse] = []
    total_tokens: dict = Field(default_factory=dict)
    total_latency_ms: float
    estimated_cost_usd: float
