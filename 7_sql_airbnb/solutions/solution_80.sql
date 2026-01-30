-- #80: Представление Verified_Users (id, name, email) — только пользователи с подтверждённой почтой.

CREATE VIEW IF NOT EXISTS Verified_Users AS
SELECT id, name, email
FROM users
WHERE email_verified_at IS NOT NULL;
