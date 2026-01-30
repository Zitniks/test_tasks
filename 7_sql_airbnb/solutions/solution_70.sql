-- #70: Категоризация жилья: economy <=100, comfort 100<x<200, premium >=200. Вывод: category, count.

SELECT
    CASE
        WHEN price <= 100 THEN 'economy'
        WHEN price < 200 THEN 'comfort'
        ELSE 'premium'
    END AS category,
    COUNT(*) AS count
FROM rooms
GROUP BY category
ORDER BY CASE category WHEN 'economy' THEN 1 WHEN 'comfort' THEN 2 ELSE 3 END;
