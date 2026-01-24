# URL Shortener Service

HTTP сервис для сокращения URL с поддержкой кастомных ссылок и валидацией.

## Описание

Сервис позволяет создавать короткие ссылки из длинных URL и выполнять редирект на оригинальные адреса. Реализован на FastAPI с использованием PostgreSQL для хранения данных.

## Реализация

### Архитектура

Проект организован по структуре, похожей на Go-проекты:

- `cmd/server/` - точка входа приложения, FastAPI роуты
- `internal/` - внутренняя логика приложения
  - `models/` - SQLAlchemy модели
  - `db/` - подключение к БД, сессии
  - `crud/` - операции с БД
- `pkg/utils/` - утилиты (генерация кодов, валидация URL)
- `api/schemas/` - Pydantic схемы для валидации запросов/ответов
- `configs/` - конфигурация приложения

### Основные компоненты

**FastAPI приложение** (`cmd/server/main.py`):
- `POST /api/v1/shorten` - создание короткой ссылки
- `GET /{short_code}` - редирект на оригинальный URL
- `GET /api/v1/health` - проверка работоспособности

**Модель данных** (`internal/models/short_url.py`):
- `id` - первичный ключ
- `original_url` - оригинальный URL
- `short_code` - короткий код (уникальный)
- `created_at` - время создания

### Структура базы данных

**Таблица `short_urls`:**

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Первичный ключ | PRIMARY KEY, AUTO INCREMENT |
| `original_url` | VARCHAR | Оригинальный URL | NOT NULL, INDEXED |
| `short_code` | VARCHAR | Короткий код | NOT NULL, UNIQUE, INDEXED |
| `created_at` | TIMESTAMP | Время создания записи | DEFAULT CURRENT_TIMESTAMP |

**Индексы:**
- `ix_short_urls_id` - индекс по полю `id`
- `ix_short_urls_original_url` - индекс по полю `original_url` (для быстрого поиска)
- `ix_short_urls_short_code` - уникальный индекс по полю `short_code` (для быстрого поиска и обеспечения уникальности)

**SQL схема:**
```sql
CREATE TABLE short_urls (
    id INTEGER NOT NULL,
    original_url VARCHAR NOT NULL,
    short_code VARCHAR NOT NULL,
    created_at TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE INDEX ix_short_urls_id ON short_urls (id);
CREATE INDEX ix_short_urls_original_url ON short_urls (original_url);
CREATE UNIQUE INDEX ix_short_urls_short_code ON short_urls (short_code);
```

**CRUD операции** (`internal/crud/short_url.py`):
- `create_short_url()` - создание записи с проверкой уникальности кода
- `get_short_url_by_code()` - получение по коду

**Валидация** (`pkg/utils/url.py`):
- `validate_url()` - проверка формата и доступности URL через HTTP запрос
- `validate_short_code()` - проверка формата кастомного кода (3-50 символов, буквы/цифры/дефис/подчеркивание)
- `generate_short_code()` - генерация случайного 6-символьного кода

### Особенности реализации

1. **Валидация URL**: При создании короткой ссылки выполняется проверка доступности URL через HEAD/GET запрос с таймаутом 5 секунд.

2. **Кастомные коды**: Пользователь может задать свой короткий код. Проверяется уникальность и формат.

3. **Автогенерация кодов**: Если кастомный код не указан, генерируется случайный 6-символьный код из букв и цифр.

4. **Редирект**: Используется HTTP 302 для редиректа на оригинальный URL.

5. **База данных**: PostgreSQL с SQLAlchemy ORM. Используется Alembic для миграций. Миграции применяются автоматически при старте приложения.

## Технологии

- **Python 3.11+**
- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy 2.0** - ORM
- **Alembic** - миграции БД
- **Pydantic** - валидация данных
- **Pytest** - тестирование

## Установка и запуск

### Локально

1. Установка зависимостей:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Настройка БД:
```bash
createdb urlshortener
psql urlshortener -c "CREATE USER urlshortener WITH PASSWORD 'urlshortener';"
psql urlshortener -c "GRANT ALL PRIVILEGES ON DATABASE urlshortener TO urlshortener;"
```

Или используйте скрипт:
```bash
./scripts/setup_db.sh
```

3. Создание .env файла:
```bash
cat > .env << EOF
DATABASE_URL=postgresql://urlshortener:urlshortener@localhost:5432/urlshortener
BASE_URL=http://localhost:8000
SHORT_CODE_LENGTH=6
EOF
```

4. Запуск:
```bash
uvicorn cmd.server.main:app --reload
```

Приложение доступно на http://localhost:8000

### Docker

```bash
docker-compose up --build
```

Сервисы:
- Приложение: http://localhost:8000
- PostgreSQL: localhost:5432

## API

### Создать короткую ссылку

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com"}'
```

Ответ:
```json
{
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://www.example.com",
  "short_code": "abc123"
}
```

### Создать с кастомным кодом

```bash
curl -X POST "http://localhost:8000/api/v1/shorten" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com", "custom_code": "my-link"}'
```

### Редирект

```bash
curl -I http://localhost:8000/abc123
```

Или откройте в браузере: http://localhost:8000/abc123

### Health check

```bash
curl http://localhost:8000/api/v1/health
```

## Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Миграции БД

Миграции выполняются автоматически при старте приложения через Alembic.

Создать новую миграцию:
```bash
alembic -c migrations/alembic.ini revision --autogenerate -m "описание изменений"
```

Применить миграции вручную:
```bash
alembic -c migrations/alembic.ini upgrade head
```

Откатить миграцию:
```bash
alembic -c migrations/alembic.ini downgrade -1
```

Проверить текущую версию:
```bash
alembic -c migrations/alembic.ini current
```

## Тестирование

```bash
pytest
```

С покрытием:
```bash
pytest --cov=cmd --cov=internal --cov=pkg --cov-report=html
```

Отчет в `htmlcov/index.html`

## Структура проекта

```
avito_task1/
├── cmd/server/main.py      # FastAPI приложение
├── internal/
│   ├── models/short_url.py # Модель БД
│   ├── db/connection.py     # Подключение к БД
│   └── crud/short_url.py    # CRUD операции
├── pkg/utils/url.py         # Утилиты
├── api/schemas/short_url.py # Схемы Pydantic
├── configs/settings.py      # Конфигурация
├── migrations/              # Миграции Alembic
│   ├── versions/            # Файлы миграций
│   ├── env.py              # Конфигурация Alembic
│   └── alembic.ini         # Настройки Alembic
├── tests/                   # Тесты
├── scripts/                 # Скрипты
└── requirements.txt         # Зависимости
```

## Переменные окружения

- `DATABASE_URL` - строка подключения к PostgreSQL
- `BASE_URL` - базовый URL для коротких ссылок
- `SHORT_CODE_LENGTH` - длина автогенерируемого кода (по умолчанию 6)

## Дополнительно

- `Task.md` - описание задания
- `SCREEN.md` - скриншоты работающего приложения
