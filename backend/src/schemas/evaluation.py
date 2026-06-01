"""Pydantic validation schemas representing AI quality evaluations and benchmarks."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvalMetrics(BaseModel):
    """Quality scores returned by the evaluation judge."""

    relevance: float = Field(..., ge=0.0, le=1.0)
    personalization: float = Field(..., ge=0.0, le=1.0)
    budget_adherence: float = Field(..., ge=0.0, le=1.0)
    time_feasibility: float = Field(..., ge=0.0, le=1.0)
    diversity: float = Field(..., ge=0.0, le=1.0)
    hallucination_rate: float = Field(..., ge=0.0, le=1.0)  # 0.0 means perfect grounding
    overall_score: float = Field(..., ge=0.0, le=1.0)


class EvalReport(BaseModel):
    """Complete evaluation report for an itinerary variant."""

    itinerary_id: int
    scores: EvalMetrics
    strengths: list[str] = []
    weaknesses: list[str] = []
    recommendations: list[str] = []
    timestamp: str


class BenchmarkResult(BaseModel):
    """Aggregate benchmark metrics tracking quality over time."""

    benchmark_run_id: str
    run_date: str
    dataset_name: str
    mean_scores: EvalMetrics
    pass_rate: float
