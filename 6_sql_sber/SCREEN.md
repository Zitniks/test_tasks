# Скриншоты выполнения задания Сбербанк #103

## Задание

Вывести список имён сотрудников, получающих большую заработную плату, чем у непосредственного руководителя.

## Как воспроизвести результат

### 1. Подготовка БД

Выполните в порядке:

- `departments.sql` — создание и заполнение таблицы отделов
- `employees.sql` — создание и заполнение таблицы сотрудников
- `solution.sql` — запрос-решение

### 2. Запрос (solution.sql)

```sql
SELECT e.name
FROM employees e
INNER JOIN employees chief ON e.chief_id = chief.id
WHERE e.salary > chief.salary
ORDER BY e.name;
```

### 3. Выполненные запросы и результат

**Запуск (локально, SQLite):**

```bash
cd 6_sql_sber
sqlite3 sber.db ".read departments.sql" ".read employees.sql"
sqlite3 -header -column sber.db ".read solution.sql"
```

**Запрос из solution.sql:**

```sql
SELECT e.name
FROM employees e
INNER JOIN employees chief ON e.chief_id = chief.id
WHERE e.salary > chief.salary
ORDER BY e.name;
```

**Результат выполнения:**

| name             |
|------------------|
| Aaron Vaughan    |
| Adrian Zavala    |
| Amanda Rivera    |
| Angela Frye      |
| Belinda Anderson |
| Brian Hawkins    |
| Erik Lambert     |
| Gregory Young    |
| James Kim        |
| Jenna Carr       |
| Melody Henderson |
| Patrick Whitehead|
| Tyler Nelson     |

Всего **13** сотрудников получают зарплату выше, чем у непосредственного руководителя.

### 4. Скриншоты (папка images/)

- **Скрин 1:** Подключение к БД и выполнение скриптов `departments.sql` и `employees.sql` (или вывод об успешном выполнении).
- **Скрин 2:** Выполнение `solution.sql` и результирующая таблица с полем **name**.
- **Скрин 3 (по желанию):** Проверка на одном примере: сотрудник, его зарплата, руководитель, зарплата руководителя — видно, что зарплата сотрудника больше.

#### Результат выполнения запроса

![Результат запроса](images/Снимок%20экрана%202026-01-30%20в%2022.37.56.png)

## Проверка корректности

- В результате только один столбец: **name**.
- В списке только сотрудники, у которых заполнен **chief_id** и зарплата строго больше зарплаты руководителя.
- Сотрудники без руководителя (chief_id IS NULL) в результат не входят.
- Строки отсортированы по **name**.
