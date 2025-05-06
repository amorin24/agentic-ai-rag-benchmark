# Docker Setup

This document provides detailed instructions for deploying the Agentic AI RAG Benchmark project using Docker.

## Prerequisites

Before proceeding, ensure you have:

- Docker installed (version 20.10.x or higher)
- Docker Compose installed (version 2.x or higher)
- All required API keys (OpenAI, NewsAPI, Financial Modeling Prep)

## Docker Compose Configuration

The project includes a `docker-compose.yml` file at the root of the project that defines three main services:

1. **rag_service**: The FastAPI-based RAG service
2. **agent_runner**: A configurable agent framework runner
3. **ui**: The React-based UI for comparing agent outputs

### Docker Compose File

```yaml
version: '3.8'

services:
  rag_service:
    build:
      context: .
      dockerfile: docker/rag_service.Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  agent_runner:
    build:
      context: .
      dockerfile: docker/agent_runner.Dockerfile
    depends_on:
      rag_service:
        condition: service_healthy
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file:
      - .env
    environment:
      - RAG_SERVICE_HOST=rag_service
      - RAG_SERVICE_PORT=8000
      - AGENT_FRAMEWORK=${AGENT_FRAMEWORK:-crewai}

  ui:
    build:
      context: .
      dockerfile: docker/ui.Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - rag_service
      - agent_runner
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file:
      - .env
    environment:
      - REACT_APP_RAG_SERVICE_URL=http://rag_service:8000
      - REACT_APP_AGENT_RUNNER_URL=http://agent_runner:5000
```

## Building and Running with Docker Compose

### Starting All Services

To build and start all services:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Starting Individual Services

To start individual services:

```bash
# Start only the RAG service
docker-compose up -d rag_service

# Start only the UI
docker-compose up -d ui
```

### Running Different Agent Frameworks

The `agent_runner` service is configurable and can run any of the implemented agent frameworks. To specify which framework to use:

```bash
# Run with CrewAI (default)
AGENT_FRAMEWORK=crewai docker-compose up -d agent_runner

# Run with AutoGen
AGENT_FRAMEWORK=autogen docker-compose up -d agent_runner

# Run with LangGraph
AGENT_FRAMEWORK=langgraph docker-compose up -d agent_runner

# Run with Google ADK
AGENT_FRAMEWORK=googleadk docker-compose up -d agent_runner

# Run with SquidAI
AGENT_FRAMEWORK=squidai docker-compose up -d agent_runner

# Run with LettaAI
AGENT_FRAMEWORK=lettaai docker-compose up -d agent_runner
```

## Docker Images

The project includes several Dockerfiles for different components:

### RAG Service Dockerfile

The `docker/rag_service.Dockerfile` builds the RAG service:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "rag_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Agent Runner Dockerfile

The `docker/agent_runner.Dockerfile` builds a configurable agent runner:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV AGENT_FRAMEWORK=crewai

CMD ["python", "-m", "agents.runner"]
```

### UI Dockerfile

The `docker/ui.Dockerfile` builds the React UI:

```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY ui/viewer/package.json ui/viewer/package-lock.json ./

RUN npm install

COPY ui/viewer/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

## Volume Mapping

The Docker Compose configuration maps several volumes:

- **./data:/app/data**: Maps the data directory for storing processed documents and FAISS indexes
- **./logs:/app/logs**: Maps the logs directory for storing execution logs

## Environment Variables

The Docker Compose configuration uses the `.env` file for environment variables. Make sure this file is properly configured before starting the services. See the [Configuration](./configuration.md) documentation for details.

## Networking

The Docker Compose configuration creates a network for the services to communicate with each other:

- The RAG service is accessible at `http://rag_service:8000` within the network
- The agent runner is accessible at `http://agent_runner:5000` within the network
- The UI is accessible at `http://localhost:3000` from the host machine

## Health Checks

The RAG service includes a health check to ensure it's properly started before the agent runner tries to connect to it:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/status"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## Troubleshooting

### Common Issues

1. **Services not starting**: Check the logs with `docker-compose logs -f`
2. **RAG service not accessible**: Check if the RAG service is healthy with `docker-compose ps`
3. **Agent runner not connecting to RAG service**: Check if the RAG service is healthy and if the agent runner is configured correctly

### Viewing Logs

To view logs for a specific service:

```bash
# View RAG service logs
docker-compose logs -f rag_service

# View agent runner logs
docker-compose logs -f agent_runner

# View UI logs
docker-compose logs -f ui
```

## Next Steps

After setting up the Docker environment, proceed to the [Usage](../usage/README.md) documentation for instructions on using the project.
