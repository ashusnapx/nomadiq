"""Unit tests for the Model Router and complexity-based LLM routing."""

from __future__ import annotations

import pytest
from backend.src.integrations.model_router import ModelRouter, TaskComplexity


@pytest.mark.asyncio
async def test_model_router_offline_mock() -> None:
    """Verifies that the model router falls back cleanly to deterministic mocks when no API key is set."""
    router = ModelRouter()
    
    # Force client to None to trigger mock path
    router._client = None
    
    messages = [{"role": "user", "content": "Tell me about traveler preferences"}]
    res = await router.invoke(messages, TaskComplexity.SIMPLE)
    
    assert res is not None
    assert "model" in res
    assert "content" in res
    assert "usage" in res
    assert "-mock" in res["model"]
    
    # Check that we parsed appropriate mock JSON
    import json
    data = json.loads(res["content"])
    assert "interests" in data
    assert "Sightseeing" in data["interests"]
