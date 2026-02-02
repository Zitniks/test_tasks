-- #58: Добавить отзыв с рейтингом 5 на жилье по адресу "11218, Friel Place, New York" от имени "George Clooney".
-- id = количество записей в таблице + 1.

INSERT INTO reviews (id, reservation_id, rating)
SELECT
    (SELECT COUNT(*) FROM reviews) + 1,
    res.id,
    5
FROM reservations res
JOIN rooms r ON r.id = res.room_id
JOIN users u ON u.id = res.user_id
WHERE r.address = '11218, Friel Place, New York'
  AND u.name = 'George Clooney'
LIMIT 1;
