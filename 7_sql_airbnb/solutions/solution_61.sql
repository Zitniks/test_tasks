-- #61: Комнаты, зарезервированные хотя бы на одни сутки в 12-ю неделю 2020 года (16–22 марта).

SELECT DISTINCT r.*
FROM rooms r
JOIN reservations res ON r.id = res.room_id
WHERE res.start_date < '2020-03-23'
  AND res.end_date > '2020-03-16';
