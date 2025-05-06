FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agents/ /app/agents/
COPY utils/ /app/utils/
COPY external/ /app/external/

ENV PYTHONPATH=/app

# Default to crewai, but can be overridden with environment variable
ARG AGENT_FRAMEWORK=crewai
ENV AGENT_FRAMEWORK=${AGENT_FRAMEWORK}

# The command will be provided in docker-compose.yml
# This allows for dynamic selection of the agent framework
CMD ["python", "-m", "agents.${AGENT_FRAMEWORK}.runner"]
