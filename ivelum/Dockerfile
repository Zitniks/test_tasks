# Hacker News Proxy: только код приложения, без тестов и документации
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cmd/ ./cmd/
COPY configs/ ./configs/
COPY internal/ ./internal/
COPY pkg/ ./pkg/

CMD ["uvicorn", "cmd.server.main:app", "--host", "0.0.0.0", "--port", "8232"]
