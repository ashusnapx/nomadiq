"""Unit tests for the Caching layer and Redis serialization."""

from __future__ import annotations

import pytest
from backend.src.services.cache_service import cache_service


@pytest.mark.asyncio
async def test_cache_set_and_get() -> None:
    """Verifies that items are successfully written to and retrieved from cache."""
    test_key = "test_run:cache_key"
    test_data = {"test_value": 42, "status": "active"}

    # Set value
    success = await cache_service.set(test_key, test_data, ttl_sec=60)
    assert success

    # Get value back
    retrieved = await cache_service.get(test_key)
    assert retrieved is not None
    assert retrieved["test_value"] == 42
    assert retrieved["status"] == "active"

    # Delete value
    deleted = await cache_service.delete(test_key)
    assert deleted

    # Confirm deleted
    cleared = await cache_service.get(test_key)
    assert cleared is None
