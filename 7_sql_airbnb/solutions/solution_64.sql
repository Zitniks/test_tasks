-- #64: Количество бронирований по каждому месяцу каждого года. Сортировка по возрастанию даты.

SELECT
    CAST(strftime('%Y', start_date) AS INT) AS year,
    CAST(strftime('%m', start_date) AS INT) AS month,
    COUNT(*) AS amount
FROM reservations
GROUP BY year, month
ORDER BY year, month;
