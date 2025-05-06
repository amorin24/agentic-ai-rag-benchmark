FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_service/ /app/rag_service/
COPY utils/ /app/utils/

ENV PYTHONPATH=/app

CMD ["uvicorn", "rag_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
