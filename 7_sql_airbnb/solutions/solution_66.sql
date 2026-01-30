-- #66: Комнаты со всеми удобствами (ТВ, интернет, кухня, кондиционер) + общее кол-во дней и сумма аренды.

SELECT
    r.home_type,
    r.address,
    CAST(COALESCE(SUM(ROUND(JULIANDAY(res.end_date) - JULIANDAY(res.start_date))), 0) AS INT) AS days,
    COALESCE(SUM(res.total), 0) AS total_fee
FROM rooms r
LEFT JOIN reservations res ON res.room_id = r.id
WHERE r.has_tv AND r.has_internet AND r.has_kitchen AND r.has_air_con
GROUP BY r.id, r.home_type, r.address;
