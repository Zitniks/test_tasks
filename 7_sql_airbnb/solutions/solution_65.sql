-- #65: Рейтинг комнат (хоть раз арендованных) как FLOOR(AVG(рейтинг отзывов)).

SELECT
    res.room_id,
    CAST(AVG(rev.rating) AS INT) AS rating
FROM reservations res
JOIN reviews rev ON rev.reservation_id = res.id
GROUP BY res.room_id;
