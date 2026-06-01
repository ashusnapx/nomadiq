"""Unit tests for the AI Cost Governance tracking and budget alerts."""

from __future__ import annotations

import pytest
from backend.src.observability.cost_tracker import cost_tracker


def test_cost_tracker_accumulation() -> None:
    """Verifies that cost tracking aggregates prompt and completion tokens accurately."""
    cost_tracker.clear()
    
    # Record first invocation
    cost_tracker.record("gpt-4o-mini", prompt_tokens=1000, completion_tokens=500)
    summary = cost_tracker.get_summary()
    
    assert summary["total_prompt_tokens"] == 1000
    assert summary["total_completion_tokens"] == 500
    assert summary["request_count"] == 1
    assert summary["total_cost_usd"] > 0.0  # Verify non-zero cost calculated
    
    # Record second invocation
    cost_tracker.record("gpt-4o", prompt_tokens=500, completion_tokens=250)
    summary_updated = cost_tracker.get_summary()
    
    assert summary_updated["total_prompt_tokens"] == 1500
    assert summary_updated["total_completion_tokens"] == 750
    assert summary_updated["request_count"] == 2
    
    # Verify budget limit check
    assert not summary_updated["over_budget"]
    
    cost_tracker.clear()
