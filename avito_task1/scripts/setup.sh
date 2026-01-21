#!/bin/bash
set -e

echo "Настройка окружения..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cat > .env << EOF
DATABASE_URL=postgresql://urlshortener:urlshortener@localhost:5432/urlshortener
BASE_URL=http://localhost:8000
SHORT_CODE_LENGTH=6
EOF
fi

echo "Готово!"
