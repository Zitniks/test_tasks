from unittest.mock import AsyncMock, patch

from tests.conftest import client


@patch('cmd.server.main.httpx.AsyncClient')
def test_proxy_request(mock_client_class):
    mock_response = AsyncMock()
    mock_response.text = '<html><body><p>The visual description</p></body></html>'
    mock_response.headers = {'content-type': 'text/html'}
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None

    async def mock_get(*args, **kwargs):
        return mock_response

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get = mock_get
    mock_client_class.return_value = mock_client

    response = client.get('/item?id=123')
    assert response.status_code == 200
    assert 'visual™' in response.text
    assert 'description™' in response.text
