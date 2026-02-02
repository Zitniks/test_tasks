"""Тесты API прокси (TestClient, мок upstream)."""

from unittest.mock import AsyncMock, patch

import httpx

from tests.conftest import client


@patch("cmd.server.main.httpx.AsyncClient")
def test_proxy_get_returns_modified_html(mock_client_class, client):
    """GET к прокси возвращает HTML с ™ и переписанными ссылками."""
    mock_response = AsyncMock()
    mock_response.text = (
        "<html><body><p>The visual description</p></body></html>"
    )
    mock_response.headers = {"content-type": "text/html"}
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None

    async def mock_get(*args, **kwargs):
        return mock_response

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    response = client.get("/item?id=123")
    assert response.status_code == 200
    assert "visual™" in response.text
    assert "description™" in response.text


@patch("cmd.server.main.httpx.AsyncClient")
def test_proxy_502_on_upstream_error(mock_client_class, client):
    """При ошибке upstream (HTTPError) возвращается 502."""
    async def mock_get(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "502",
            request=AsyncMock(),
            response=AsyncMock(status_code=502),
        )

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    response = client.get("/item?id=1")
    assert response.status_code == 502
    assert "upstream" in response.text.lower()


def test_proxy_405_method_not_allowed(client):
    """Метод, отличный от GET/POST, возвращает 405."""
    response = client.request("PUT", "/item?id=1")
    assert response.status_code == 405
