-- #74: id и признак наличия интернета (YES/NO).

SELECT
    id,
    CASE WHEN has_internet THEN 'YES' ELSE 'NO' END AS has_internet
FROM rooms
ORDER BY id;
