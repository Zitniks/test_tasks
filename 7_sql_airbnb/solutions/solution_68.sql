-- #68: Для каждой комнаты, которую снимали хотя бы раз: имя последнего арендатора и дата выезда.

SELECT
    res.room_id AS room_id,
    u.name,
    res.end_date AS end_date
FROM reservations res
JOIN users u ON u.id = res.user_id
JOIN (
    SELECT room_id, MAX(end_date) AS max_end
    FROM reservations
    GROUP BY room_id
) last ON last.room_id = res.room_id AND last.max_end = res.end_date;
