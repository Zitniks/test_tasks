-- #73: id комнат, которые арендовали нечётное количество раз.

SELECT
    room_id,
    COUNT(*) AS count
FROM reservations
GROUP BY room_id
HAVING COUNT(*) % 2 = 1;
