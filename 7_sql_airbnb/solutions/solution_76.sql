-- #76: Все пользователи + признак is_owner (1/0) и is_tenant (1/0).

SELECT
    u.name,
    (SELECT COUNT(*) FROM rooms r WHERE r.owner_id = u.id) > 0 AS is_owner,
    (SELECT COUNT(*) FROM reservations res WHERE res.user_id = u.id) > 0 AS is_tenant
FROM users u;
