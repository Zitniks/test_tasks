# Aviasales Flight Search API

Веб-сервис для анализа данных о перелётах из XML файлов партнёров Aviasales.

## Описание

Сервис парсит XML файлы с данными о перелётах и предоставляет API для:
- Поиска вариантов перелёта по маршруту
- Поиска самого дорогого/дешёвого варианта
- Поиска самого быстрого/долгого варианта
- Поиска оптимального варианта (баланс цены и времени)
- Сравнения результатов двух запросов

## Реализация

### Архитектура

Проект организован по структуре, похожей на Go-проекты:

- `cmd/server/` - точка входа, FastAPI приложение
- `internal/parser/` - парсинг XML файлов
- `internal/models/` - модели данных для перелётов
- `pkg/utils/` - утилиты для работы с перелётами
- `api/schemas/` - схемы API
- `configs/` - конфигурация

### Основные компоненты

**FastAPI приложение** (`cmd/server/main.py`):
- `/api/v1/flights/dxb-bkk` - все варианты перелёта из DXB в BKK
- `/api/v1/flights/dxb-bkk/cheapest` - самый дешёвый вариант
- `/api/v1/flights/dxb-bkk/most-expensive` - самый дорогой вариант
- `/api/v1/flights/dxb-bkk/fastest` - самый быстрый вариант
- `/api/v1/flights/dxb-bkk/slowest` - самый долгий вариант
- `/api/v1/flights/dxb-bkk/optimal` - оптимальный вариант
- `/api/v1/flights/compare` - сравнение результатов двух запросов

**Парсер XML** (`internal/parser/xml_parser.py`):
- Парсит XML файлы с данными о перелётах
- Извлекает информацию о рейсах, ценах, маршрутах

**Модели данных** (`internal/models/flight.py`):
- `Flight` - информация об одном рейсе
- `Pricing` - информация о ценах
- `FlightItinerary` - полный маршрут (туда и обратно)

## Установка и запуск

### Локально

1. Установка зависимостей:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Или используйте скрипт:
```bash
./scripts/setup.sh
```

2. Запуск сервера:
```bash
uvicorn cmd.server.main:app --host 127.0.0.1 --port 8000 --reload
```

3. API будет доступен по адресу:
- http://127.0.0.1:8000
- Swagger документация: http://127.0.0.1:8000/docs
- ReDoc документация: http://127.0.0.1:8000/redoc
- OpenAPI схема: http://127.0.0.1:8000/openapi.json

### Docker

```bash
docker-compose up --build
```

## Тестирование

```bash
source venv/bin/activate
pytest
```

Или используйте скрипт:
```bash
./scripts/run_tests.sh
```

## Формат данных

### XML файлы

Сервис ожидает два XML файла:
- `RS_Via-3.xml` - запрос туда-обратно
- `RS_ViaOW.xml` - запрос в одну сторону

Файлы должны находиться в корне проекта.

### Формат ответа API

Все эндпоинты возвращают JSON с информацией о перелётах:
- Информация о рейсах (авиакомпания, номер рейса, время)
- Цена и валюта
- Длительность перелёта
- Маршрут (источник и назначение)

## Документация API

### Swagger UI

После запуска сервера интерактивная документация Swagger доступна по адресу:
- http://127.0.0.1:8000/docs

Swagger UI позволяет:
- Просматривать все доступные эндпоинты
- Видеть схемы запросов и ответов
- Тестировать API прямо в браузере
- Просматривать примеры данных

### ReDoc

Альтернативная документация в формате ReDoc доступна по адресу:
- http://127.0.0.1:8000/redoc

### Postman коллекция

В проекте включена готовая Postman коллекция:
- `Aviasales_API.postman_collection.json`

Для использования:
1. Откройте Postman
2. Импортируйте файл `Aviasales_API.postman_collection.json`
3. Убедитесь, что переменная `base_url` установлена на `http://127.0.0.1:8000` (или другой адрес вашего сервера)

Коллекция включает все эндпоинты API, организованные по категориям:
- **Health** - проверка состояния сервиса
- **Flights** - поиск и фильтрация перелётов
- **Comparison** - сравнение результатов запросов

## Примеры запросов

### cURL

```bash
# Все варианты DXB -> BKK
curl http://127.0.0.1:8000/api/v1/flights/dxb-bkk

# Самый дешёвый вариант
curl http://127.0.0.1:8000/api/v1/flights/dxb-bkk/cheapest

# Сравнение результатов
curl http://127.0.0.1:8000/api/v1/flights/compare
```

### Python (requests)

```python
import requests

base_url = "http://127.0.0.1:8000"

# Все варианты перелёта
response = requests.get(f"{base_url}/api/v1/flights/dxb-bkk")
flights = response.json()

# Самый дешёвый вариант
response = requests.get(f"{base_url}/api/v1/flights/dxb-bkk/cheapest")
cheapest = response.json()
```
