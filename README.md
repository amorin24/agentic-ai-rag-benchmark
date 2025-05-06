# agentic-ai-rag-benchmark

A framework for evaluating and comparing different agentic AI frameworks (CrewAI, AutoGen, LangGraph, etc.) using a shared RAG (Retrieval-Augmented Generation) microservice.

## Overview

This project provides a standardized way to benchmark various agentic AI frameworks by using a common RAG service. The system allows for fair comparison of how different agent frameworks utilize retrieved information to complete tasks.

## Components

- **RAG Service**: A centralized FastAPI service with FAISS for vector retrieval
- **Agent Runners**: Modular implementations for different agent frameworks
- **UI Viewer**: React-based interface for comparing outputs side-by-side
- **Docker Support**: Local orchestration of all components

## Project Structure

```
.
├── agents/                # Agent framework implementations
│   ├── autogen/          # AutoGen implementation
│   ├── crewai/           # CrewAI implementation
│   ├── langgraph/        # LangGraph implementation
│   └── common/           # Shared agent utilities
├── data/                 # Data for RAG and benchmarking
├── docker/               # Docker configuration files
├── logs/                 # Log output directory
├── rag_service/          # Centralized RAG service
│   ├── app/              # FastAPI application
│   ├── models/           # Vector store and embedding models
│   └── utils/            # Utility functions
├── tests/                # Test suite
│   ├── agents/           # Agent tests
│   ├── rag_service/      # RAG service tests
│   └── ui/               # UI tests
├── ui/                   # User interface
│   └── viewer/           # React-based comparison viewer
└── utils/                # Shared utilities
```

## Getting Started

1. Clone the repository
2. Set up environment variables in `.env`
3. Install dependencies with `pip install -r requirements.txt`
4. Start the services with Docker Compose: `docker-compose up`

## Docker Setup

The project includes Docker support for easy deployment and testing:

### Root-level Docker Compose

The root-level `docker-compose.yml` provides a simplified setup with three services:

```bash
# Start all services
docker-compose up -d

# Run with a specific agent framework
AGENT_FRAMEWORK=autogen docker-compose up agent_runner

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Services

- **rag_service**: FastAPI application on port 8000
  - Provides RAG capabilities with FAISS vector store
  - Exposes /ingest, /query, and /status endpoints

- **agent_runner**: Configurable agent framework runner
  - Can run any of the implemented agent frameworks (CrewAI, AutoGen, LangGraph, etc.)
  - Configurable via AGENT_FRAMEWORK environment variable
  - Default framework is crewai if not specified

- **ui**: React-based UI on port 3000
  - Provides side-by-side comparison of agent outputs
  - Visualizes metrics and execution steps

### Extended Configuration

For more advanced setups with all agent frameworks running separately:

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## License

[MIT License](LICENSE)
