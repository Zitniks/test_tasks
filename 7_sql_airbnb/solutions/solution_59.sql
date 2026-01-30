-- #59: Пользователи с белорусским номером телефона (+375).

SELECT *
FROM users
WHERE phone_number LIKE '+375%';
