"""Фикстуры для тестов API (TestClient)."""

import pytest
from fastapi.testclient import TestClient

from cmd.server.main import app


@pytest.fixture
def client():
    """HTTP-клиент для запросов к приложению (без реального upstream)."""
    return TestClient(app)
