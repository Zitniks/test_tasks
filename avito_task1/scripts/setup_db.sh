#!/bin/bash
set -e

DB_NAME="urlshortener"
DB_USER="urlshortener"
DB_PASSWORD="urlshortener"

if ! pg_isready -q; then
    echo "PostgreSQL не запущен"
    exit 1
fi

if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "База данных '$DB_NAME' уже существует"
else
    createdb $DB_NAME
fi

if psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "Пользователь '$DB_USER' уже существует"
else
    psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
fi

psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Готово!"
