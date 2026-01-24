import pytest
from fastapi import status


def test_create_short_url(client):
    response = client.post('/api/v1/shorten', json={'original_url': 'https://www.example.com'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert 'short_url' in data
    assert 'original_url' in data
    assert 'short_code' in data
    assert data['original_url'] == 'https://www.example.com'
    assert data['short_code'] in data['short_url']


def test_create_short_url_with_custom_code(client):
    response = client.post(
        '/api/v1/shorten',
        json={'original_url': 'https://www.example.com', 'custom_code': 'test-link'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['short_code'] == 'test-link'
    assert 'test-link' in data['short_url']


def test_create_short_url_invalid_url(client):
    response = client.post('/api/v1/shorten', json={'original_url': 'not-a-valid-url'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_short_url_duplicate_custom_code(client):
    client.post(
        '/api/v1/shorten',
        json={'original_url': 'https://www.example.com', 'custom_code': 'duplicate'},
    )

    response = client.post(
        '/api/v1/shorten',
        json={'original_url': 'https://www.another.com', 'custom_code': 'duplicate'},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_short_url_invalid_custom_code(client):
    response = client.post(
        '/api/v1/shorten',
        json={'original_url': 'https://www.example.com', 'custom_code': 'ab'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_redirect_to_original(client):
    create_response = client.post('/api/v1/shorten', json={'original_url': 'https://www.example.com'})
    short_code = create_response.json()['short_code']

    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers['location'] == 'https://www.example.com'


def test_redirect_not_found(client):
    response = client.get('/nonexistent', follow_redirects=False)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
