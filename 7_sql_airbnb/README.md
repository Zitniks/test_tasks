# SQL-задание Airbnb #74

Вывод идентификатора комнаты и признака наличия интернета в помещении (YES/NO).

## Задача

По таблице **rooms** (жильё сервиса бронирования) нужно вывести для каждой комнаты:
- **id** — идентификатор;
- **has_internet** — «YES», если в помещении есть интернет, иначе «NO».

Подробное условие — в [Task.md](./Task.md).

## Структура проекта

```
7_sql_airbnb/
├── README.md        # этот файл
├── Task.md          # описание задания #74
├── SCREEN.md        # скриншоты выполнения
├── rooms.sql        # схема и данные таблицы комнат
├── users.sql        # пользователи
├── reservations.sql # бронирования
├── reviews.sql      # отзывы
├── solution.sql     # решение #74 (признак интернета)
├── airbnb/          # исходный список заданий (airbnb_sql_tests.md, tests/58..80)
└── solutions/       # решения всех заданий Airbnb SQL (#58–#80)
    ├── README.md    # описание и список решений
    ├── solution_58.sql … solution_80.sql
```

В папке **solutions/** собраны решения всех заданий из [airbnb_sql_tests.md](airbnb/airbnb_sql_tests.md): #58–#80. Подробности — в [solutions/README.md](solutions/README.md).

Для задания #74 достаточно загрузить **rooms.sql** и выполнить **solution.sql** (или **solutions/solution_74.sql**).

## Локальный запуск

### Требования

- PostgreSQL, SQLite или любой SQL-клиент (DBeaver, pgAdmin, psql и т.п.).

### Шаги (SQLite)

1. Создайте БД и загрузите таблицы (для #74 достаточно rooms):

```bash
cd 7_sql_airbnb
sqlite3 airbnb.db ".read rooms.sql"
sqlite3 -header -column airbnb.db ".read solution.sql"
```

2. Полная схема (если нужны users, reservations, reviews):

```bash
sqlite3 airbnb.db ".read rooms.sql" ".read users.sql" ".read reservations.sql" ".read reviews.sql"
sqlite3 -header -column airbnb.db ".read solution.sql"
```

### Шаги (PostgreSQL)

```bash
createdb airbnb_74
psql -d airbnb_74 -f rooms.sql
psql -d airbnb_74 -f solution.sql
```

## Запуск в Docker

```bash
docker run --name airbnb-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=airbnb_74 -p 5432:5432 -d postgres:15
sleep 3
cd 7_sql_airbnb
PGPASSWORD=postgres psql -h localhost -U postgres -d airbnb_74 -f rooms.sql -f solution.sql
```

## Решение

Используется выражение **CASE WHEN has_internet THEN 'YES' ELSE 'NO' END AS has_internet** по таблице **rooms**. Подробности — в [solution.sql](./solution.sql).

## Дополнительно

- **Task.md** — полное описание задания и формата результата.
- **SCREEN.md** — скриншоты выполнения запроса.
- Исходные задания: [Hexlet ru-test-assignments / sql / airbnb](https://github.com/Hexlet/ru-test-assignments/tree/main/sql/airbnb).
