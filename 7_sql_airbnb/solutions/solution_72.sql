-- #72: Средняя цена бронирования за сутки по комнатам (которые бронировали хотя бы раз). Округление вверх.

SELECT
    room_id,
    (CAST(AVG(price) AS INT) + (AVG(price) > CAST(AVG(price) AS INT))) AS avg_price
FROM reservations
GROUP BY room_id;
