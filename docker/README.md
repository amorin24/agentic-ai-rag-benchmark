# Docker Configuration

Docker setup for local orchestration of all components.

## Components

- **RAG Service**: FastAPI service with FAISS
- **Agent Runners**: Containerized agent framework implementations
- **UI Viewer**: React frontend for comparison

## Usage

1. Build all containers: `docker-compose build`
2. Start all services: `docker-compose up`
3. Stop all services: `docker-compose down`

## Configuration

Configure Docker services using environment variables in the root `.env` file.
