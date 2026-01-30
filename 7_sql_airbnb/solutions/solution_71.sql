-- #71: Процент пользователей, хоть раз арендовавших или сдававших жилье. Округление до сотых.

SELECT
    ROUND(100.0 * (
        SELECT COUNT(DISTINCT u.id)
        FROM users u
        WHERE u.id IN (SELECT user_id FROM reservations)
           OR u.id IN (SELECT owner_id FROM rooms)
    ) / (SELECT COUNT(*) FROM users), 2) AS percent;
