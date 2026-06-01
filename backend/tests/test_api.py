"""Integration tests verifying FastAPI application routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.src.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Fixture yielding a FastAPI TestClient instance."""
    app = create_app()
    return TestClient(app)


def test_api_root_endpoint(client: TestClient) -> None:
    """Verifies that the root path returns platform metadata."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "platform" in data
    assert "status" in data
    assert "NomadIQ" in data["platform"]


def test_api_health_endpoint(client: TestClient) -> None:
    """Verifies that the health check endpoint returns expected status keys."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "environment" in data
    assert "details" in data
