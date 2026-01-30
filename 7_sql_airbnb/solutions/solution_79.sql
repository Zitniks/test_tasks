-- #79: id, home_type, price. Если есть ТВ и интернет — цена со скидкой 10%.

SELECT
    id,
    home_type,
    CASE WHEN has_tv AND has_internet THEN CAST(price * 0.9 AS INT) ELSE price END AS price
FROM rooms;
