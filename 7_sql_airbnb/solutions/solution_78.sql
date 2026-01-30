-- #78: Пользователи с электронной почтой в домене hotmail.com.

SELECT *
FROM users
WHERE email LIKE '%@hotmail.com';
