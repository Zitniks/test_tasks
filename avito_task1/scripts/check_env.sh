#!/bin/bash

echo "Проверка окружения"
echo ""

echo "Python:"
python3 --version || echo "Python не найден"
echo ""

if [ -d "venv" ]; then
    echo "venv: OK"
else
    echo "venv: не найдено"
fi
echo ""

if command -v psql &> /dev/null; then
    echo "PostgreSQL: OK"
    psql --version
else
    echo "PostgreSQL: не найден"
fi
echo ""

if [ -f ".env" ]; then
    echo ".env: OK"
else
    echo ".env: не найден"
fi
