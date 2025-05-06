# Configuration Guide

This document provides detailed information on configuring the Agentic AI RAG Benchmark project.

## Environment Variables

The project uses environment variables for configuration. These can be set in a `.env` file at the root of the project or directly in the environment.

### Core Configuration

```
# Core Configuration
DEBUG=True
LOG_LEVEL=INFO
```

### RAG Service Configuration

```
# RAG Service Configuration
RAG_SERVICE_HOST=localhost
RAG_SERVICE_PORT=8000
VECTOR_STORE_PATH=data/vectors
PROCESSED_DATA_PATH=data/processed
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Embedding Configuration

```
# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
EMBEDDING_DIMENSION=768
USE_OPENAI_EMBEDDINGS=False
```

### OpenAI Configuration

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o
```

### External API Configuration

```
# NewsAPI Configuration
NEWS_API_KEY=your_newsapi_key
NEWS_API_MAX_ARTICLES=10
NEWS_API_SORT_BY=relevancy

# Financial Modeling Prep API Configuration
FMP_API_KEY=your_fmp_api_key
```

### Agent Configuration

```
# Agent Configuration
DEFAULT_AGENT_FRAMEWORK=crewai
AGENT_TIMEOUT=300
MAX_TOKENS=4000
```

### UI Configuration

```
# UI Configuration
UI_PORT=3000
UI_HOST=localhost
```

## Configuration File

The project uses a centralized configuration module in `utils/config.py` that loads and exposes these environment variables. This module provides:

1. Type conversion and validation
2. Default values for optional variables
3. Grouping of related variables
4. Safe printing of configuration (masking API keys)

Example usage:

```python
# Import specific constants
from utils.config import OPENAI_API_KEY, OPENAI_MODEL, RAG_SERVICE_URL

# Or import the entire CONFIG dictionary
from utils.config import CONFIG

# Access nested configuration
news_api_key = CONFIG["data_sources"]["news_api"]["api_key"]
```

## Docker Configuration

When using Docker, environment variables can be passed to containers in several ways:

1. Using the `env_file` directive in `docker-compose.yml`:

```yaml
services:
  rag_service:
    env_file:
      - .env
```

2. Using environment variables in `docker-compose.yml`:

```yaml
services:
  rag_service:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RAG_SERVICE_PORT=8000
```

3. Using Docker environment files:

```bash
docker-compose --env-file .env up
```

## Agent Framework Configuration

Each agent framework can be configured with specific parameters:

### CrewAI Configuration

```
CREWAI_AGENT_COUNT=3
CREWAI_MEMORY_ENABLED=True
```

### AutoGen Configuration

```
AUTOGEN_AGENT_COUNT=3
AUTOGEN_MAX_ROUNDS=10
```

### LangGraph Configuration

```
LANGGRAPH_NODE_COUNT=3
LANGGRAPH_MAX_ITERATIONS=5
```

### Google ADK Configuration

```
GOOGLEADK_TOOL_COUNT=5
GOOGLEADK_MEMORY_ENABLED=True
```

### SquidAI Configuration

```
SQUIDAI_TOOL_COUNT=6
SQUIDAI_MEMORY_ENABLED=True
```

### LettaAI Configuration

```
LETTAAI_MEMORY_TYPES=3
LETTAAI_WORKFLOW_COUNT=3
```

## Next Steps

After configuring the project, proceed to the [Docker Setup](./docker_setup.md) guide for instructions on deploying the project using Docker.
