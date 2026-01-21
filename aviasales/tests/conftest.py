import pytest
from fastapi.testclient import TestClient

from cmd.server.main import app


@pytest.fixture
def client():
    return TestClient(app)
