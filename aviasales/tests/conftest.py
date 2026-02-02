"""Pytest fixtures for Aviasales API tests."""

import pytest
from fastapi.testclient import TestClient

from cmd.server.main import app


@pytest.fixture
def client():
    """Return TestClient; lifespan runs on first request, loading XML data."""
    return TestClient(app)
