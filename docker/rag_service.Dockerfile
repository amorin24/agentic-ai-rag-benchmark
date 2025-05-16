FROM python:3.10-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_service/ /app/rag_service/
COPY utils/ /app/utils/

ENV PYTHONPATH=/app

CMD ["uvicorn", "rag_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
