# Решения заданий Airbnb SQL

Все задания из [airbnb_sql_tests.md](../airbnb/airbnb_sql_tests.md) (Hexlet ru-test-assignments).

## Как запустить

1. Загрузите схему и данные (из корня `7_sql_airbnb`):

```bash
cd 7_sql_airbnb
sqlite3 airbnb.db ".read rooms.sql" ".read users.sql" ".read reservations.sql" ".read reviews.sql"
```

2. Выполните нужное решение:

```bash
sqlite3 airbnb.db ".read solutions/solution_59.sql"
```

**Важно:** задание **#58** (INSERT) и **#80** (CREATE VIEW) изменяют БД. #58 выполнять один раз после загрузки данных. #80 создаёт представление Verified_Users.

## Список решений

| №  | Файл             | Описание |
|----|------------------|----------|
| 58 | solution_58.sql  | INSERT отзыва (рейтинг 5) на жильё по адресу от George Clooney |
| 59 | solution_59.sql  | Пользователи с белорусским номером (+375) |
| 61 | solution_61.sql  | Комнаты, зарезервированные в 12-ю неделю 2020 |
| 62 | solution_62.sql  | Домены 2-го уровня из email по популярности |
| 64 | solution_64.sql  | Количество бронирований по году и месяцу |
| 65 | solution_65.sql  | Рейтинг комнат (FLOOR(AVG(рейтинг отзывов))) |
| 66 | solution_66.sql  | Комнаты со всеми удобствами + дни и сумма аренды |
| 68 | solution_68.sql  | Последний арендатор и дата выезда по комнатам |
| 69 | solution_69.sql  | Владельцы и сумма заработка |
| 70 | solution_70.sql  | Категории жилья (economy/comfort/premium) по цене |
| 71 | solution_71.sql  | Процент пользователей, арендовавших или сдававших |
| 72 | solution_72.sql  | Средняя цена за сутки по комнатам (округление вверх) |
| 73 | solution_73.sql  | Комнаты с нечётным числом бронирований |
| 74 | solution_74.sql  | id и признак интернета (YES/NO) |
| 76 | solution_76.sql  | Все пользователи + is_owner, is_tenant |
| 78 | solution_78.sql  | Пользователи с hotmail.com |
| 79 | solution_79.sql  | id, home_type, price (скидка 10% при ТВ+интернет) |
| 80 | solution_80.sql  | CREATE VIEW Verified_Users |

## Проверка всех SELECT-решений

```bash
cd 7_sql_airbnb
for n in 59 61 62 64 65 66 68 69 70 71 72 73 74 76 78 79; do
  echo "=== #$n ===" && sqlite3 -header -column airbnb.db ".read solutions/solution_$n.sql" | head -5
done
```

После загрузки схемы: `sqlite3 airbnb.db ".read solutions/solution_58.sql"` и `sqlite3 airbnb.db ".read solutions/solution_80.sql"` для #58 и #80.
