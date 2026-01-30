# SQL-задание Сбербанк #103

Вывод списка имён сотрудников, получающих большую заработную плату, чем у непосредственного руководителя.

## Задача

Даны таблицы **departments** (отделы) и **employees** (сотрудники с полем chief_id — руководитель). Нужно написать SQL-запрос, возвращающий имена сотрудников, у которых зарплата выше, чем у их непосредственного руководителя.

Подробное описание условия — в [Task.md](./Task.md).

## Структура проекта

```
6_sql_sber/
├── README.md        # этот файл
├── Task.md          # описание задания
├── SCREEN.md        # скриншоты выполнения
├── departments.sql  # схема и данные таблицы отделов
├── employees.sql    # схема и данные таблицы сотрудников
└── solution.sql     # решение запроса
```

## Локальный запуск

### Требования

- PostgreSQL (или любой клиент: DBeaver, pgAdmin, psql и т.п.)

### Шаги

1. Создайте базу и подключитесь к ней:

```bash
createdb sber_sql_103
psql -d sber_sql_103
```

2. Выполните скрипты в порядке: сначала таблицы и данные, затем решение:

```bash
# В psql или через клиент:
\i departments.sql
\i employees.sql
\i solution.sql
```

Или одной командой из корня папки задания:

```bash
cd 6_sql_sber
psql -d sber_sql_103 -f departments.sql
psql -d sber_sql_103 -f employees.sql
psql -d sber_sql_103 -f solution.sql
```

3. Результат запроса из `solution.sql` будет выведен в консоль (или в результате выполнения в GUI).

### Одной командой (Unix)

```bash
cd 6_sql_sber
createdb sber_sql_103 2>/dev/null || true
psql -d sber_sql_103 -f departments.sql -f employees.sql -f solution.sql
```

## Запуск в Docker

1. Запустите контейнер PostgreSQL:

```bash
docker run --name sber-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=sber_sql_103 -p 5432:5432 -d postgres:15
```

2. Дождитесь старта (2–3 секунды), затем выполните скрипты:

```bash
cd 6_sql_sber
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d sber_sql_103 -f departments.sql
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d sber_sql_103 -f employees.sql
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d sber_sql_103 -f solution.sql
```

3. Остановка и удаление контейнера (по желанию):

```bash
docker stop sber-pg
docker rm sber-pg
```

## Решение

Используется самосоединение таблицы `employees`: сотрудник соединяется со своим руководителем по `chief_id = chief.id`, в выборку попадают строки, где `e.salary > chief.salary`. Подробности — в [solution.sql](./solution.sql).

## Дополнительно

- **Task.md** — полное описание задания и формата результата.
- **SCREEN.md** — скриншоты выполнения запроса и результата.
