FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ api/
COPY cmd/ cmd/
COPY configs/ configs/
COPY internal/ internal/
COPY migrations/ migrations/
COPY templates/ templates/

CMD ["uvicorn", "cmd.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
