-- #69: Идентификаторы владельцев комнат и сумма, которую они заработали.

SELECT
    r.owner_id AS owner_id,
    COALESCE(SUM(res.total), 0) AS total_earn
FROM rooms r
LEFT JOIN reservations res ON res.room_id = r.id
GROUP BY r.owner_id;
