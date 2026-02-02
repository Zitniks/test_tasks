"""Тесты API экспериментов и статистики."""


def test_get_experiments_new_device(client, db):
    """Новое устройство получает назначения по эксперименту (button_color, price)."""
    response = client.get("/api/v1/experiments", headers={"Device-Token": "test-device-1"})
    assert response.status_code == 200
    data = response.json()
    assert "button_color" in data
    assert "price" in data
    assert data["button_color"] in ["#FF0000", "#00FF00", "#0000FF"]
    assert data["price"] in ["10", "20", "50", "5"]


def test_get_experiments_same_device(client, db):
    """Один и тот же device_token получает одинаковые значения при повторных запросах."""
    device_token = "test-device-2"

    response1 = client.get("/api/v1/experiments", headers={"Device-Token": device_token})
    assert response1.status_code == 200
    data1 = response1.json()

    response2 = client.get("/api/v1/experiments", headers={"Device-Token": device_token})
    assert response2.status_code == 200
    data2 = response2.json()

    assert data1["button_color"] == data2["button_color"]
    assert data1["price"] == data2["price"]


def test_get_experiments_missing_header(client, db):
    """Без заголовка Device-Token возвращается 422."""
    response = client.get("/api/v1/experiments")
    assert response.status_code == 422


def test_statistics_api(client, db):
    """Статистика по экспериментам возвращает button_color и price с распределением."""
    for i in range(10):
        client.get("/api/v1/experiments", headers={"Device-Token": f"device-{i}"})

    response = client.get("/api/v1/statistics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(stat["experiment_key"] == "button_color" for stat in data)
    assert any(stat["experiment_key"] == "price" for stat in data)


def test_statistics_page(client, db):
    """HTML-страница /statistics отдаёт статистику с button_color и price."""
    for i in range(5):
        client.get("/api/v1/experiments", headers={"Device-Token": f"device-{i}"})

    response = client.get("/statistics")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "button_color" in response.text
    assert "price" in response.text
