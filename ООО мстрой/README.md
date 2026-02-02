# TreeStore

Класс для работы с деревом объектов с быстрым доступом к элементам.

## Описание

TreeStore принимает массив объектов с полями `id` и `parent` и предоставляет методы для работы с деревом. Реализован с использованием хеш-таблиц для O(1) доступа к элементам.

## Реализация

### Архитектура

Проект организован по структуре, похожей на Go-проекты:

- `internal/treestore/` - основной класс TreeStore
- `cmd/` - точка входа для демонстрации
- `tests/` - тесты
- `scripts/` - скрипты

### Основные компоненты

**TreeStore** (`internal/treestore/tree_store.py`):
- `getAll()` - возвращает исходный массив элементов
- `getItem(id)` - возвращает элемент по id (O(1))
- `getChildren(id)` - возвращает дочерние элементы (O(1))
- `getAllParents(id)` - возвращает цепочку родителей до корня

### Оптимизация производительности

Используются хеш-таблицы для быстрого доступа:
- `_items_by_id` - прямой доступ к элементам по id
- `_children_by_id` - прямой доступ к дочерним элементам
- `_parent_map` - карта родительских связей

Все операции выполняются за O(1) или O(h), где h - высота дерева.

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

2. Запуск примера:
```bash
python cmd/main.py
```

## Использование

```python
from internal.treestore.tree_store import TreeStore

items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

ts = TreeStore(items)

ts.getAll()
ts.getItem(7)
ts.getChildren(4)
ts.getAllParents(7)
```

## Примеры

### getAll()
Возвращает исходный массив:
```python
ts.getAll()
# [{"id":1,"parent":"root"}, {"id":2,"parent":1,"type":"test"}, ...]
```

### getItem(id)
Возвращает элемент по id:
```python
ts.getItem(7)
# {"id":7,"parent":4,"type":None}
```

### getChildren(id)
Возвращает дочерние элементы:
```python
ts.getChildren(4)
# [{"id":7,"parent":4,"type":None}, {"id":8,"parent":4,"type":None}]

ts.getChildren(5)
# []
```

### getAllParents(id)
Возвращает цепочку родителей:
```python
ts.getAllParents(7)
# [{"id":4,"parent":2,"type":"test"}, {"id":2,"parent":1,"type":"test"}, {"id":1,"parent":"root"}]
```

## Тестирование

```bash
pytest
```

С покрытием:
```bash
pytest --cov=internal --cov-report=html
```

## Структура проекта

```
ООО мстрой/
├── cmd/main.py              # Точка входа
├── internal/treestore/      # Класс TreeStore
├── tests/                   # Тесты
└── scripts/                 # Скрипты
```

## Производительность

- `getItem(id)` - O(1)
- `getChildren(id)` - O(1)
- `getAllParents(id)` - O(h), где h - высота дерева
- `getAll()` - O(1)

Все операции используют предварительно построенные индексы, что обеспечивает максимальную производительность.

## API

Доступен REST API для работы с TreeStore:

- `GET /api/v1/health` - проверка работоспособности
- `GET /api/v1/tree/getAll` - получить все элементы
- `POST /api/v1/tree/getItem` - получить элемент по id
- `POST /api/v1/tree/getChildren` - получить дочерние элементы
- `POST /api/v1/tree/getAllParents` - получить цепочку родителей
- `POST /api/v1/tree/init` - инициализировать дерево

Запуск API:
```bash
uvicorn cmd.server.main:app --host 127.0.0.1 --port 8000
```

## Дополнительно

- `Task.md` - описание задания
- `SCREEN.md` - скриншоты работающего приложения
