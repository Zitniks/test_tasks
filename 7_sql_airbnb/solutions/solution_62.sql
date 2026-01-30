-- #62: Доменные имена 2-го уровня из email в порядке убывания популярности, затем по возрастанию имени.

SELECT
    SUBSTR(email, INSTR(email, '@') + 1) AS domain,
    COUNT(*) AS count
FROM users
GROUP BY domain
ORDER BY count DESC, domain ASC;
