FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agents/ /app/agents/
COPY utils/ /app/utils/

ENV PYTHONPATH=/app

CMD ["python", "-m", "agents.autogen.runner"]
