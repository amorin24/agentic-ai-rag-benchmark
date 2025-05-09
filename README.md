# Agentic AI RAG Benchmark

A framework for evaluating and comparing different agentic AI frameworks (CrewAI, AutoGen, LangGraph, Google ADK, SquidAI, and LettaAI) using a shared RAG (Retrieval-Augmented Generation) microservice.

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
│   ├── googleadk/        # Google ADK implementation
│   ├── squidai/          # SquidAI implementation
│   ├── lettaai/          # LettaAI implementation
│   └── common/           # Shared agent utilities
├── data/                 # Data for RAG and benchmarking
│   └── processed/        # Processed documents and vectors
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

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8+ (3.10+ recommended)
- Node.js 16+ and npm/yarn
- Docker and Docker Compose (for containerized setup)
- Git

You'll also need API keys for the following services:

- OpenAI API key (for embeddings and agent LLMs)
- NewsAPI key (optional, for news data ingestion)
- Financial Modeling Prep API key (optional, for financial data)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/amorin24/agentic-ai-rag-benchmark.git
   cd agentic-ai-rag-benchmark
   ```

2. Create and configure the `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your API keys and configuration:
   ```
   # API Keys
   OPENAI_API_KEY=your_openai_api_key
   NEWS_API_KEY=your_news_api_key
   FMP_API_KEY=your_financial_modeling_prep_api_key
   
   # RAG Service Configuration
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   CHUNK_SIZE=512
   CHUNK_OVERLAP=50
   
   # Agent Configuration
   DEFAULT_AGENT_FRAMEWORK=crewai
   
   # UI Configuration
   REACT_APP_API_URL=http://localhost:8000
   ```

## Setup and Running (with Docker)

The easiest way to run the entire system is using Docker Compose:

### Option 1: Simple Setup (All-in-One)

This setup runs the RAG service, a configurable agent runner, and the UI:

1. Start all services:
   ```bash
   docker-compose up -d
   ```

2. Access the services:
   - RAG Service API: http://localhost:8000
   - UI: http://localhost:3000

3. Run with a specific agent framework:
   ```bash
   AGENT_FRAMEWORK=autogen docker-compose up agent_runner
   ```

4. View logs:
   ```bash
   docker-compose logs -f
   ```

5. Stop all services:
   ```bash
   docker-compose down
   ```

### Option 2: Advanced Setup (All Frameworks Separately)

This setup runs each agent framework as a separate service:

1. Start all services:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

2. Access the services:
   - RAG Service API: http://localhost:8000
   - UI: http://localhost:3000
   - Each agent framework has its own service and logs

3. View logs for a specific service:
   ```bash
   docker-compose -f docker/docker-compose.yml logs -f crewai_agent
   ```

4. Stop all services:
   ```bash
   docker-compose -f docker/docker-compose.yml down
   ```

## Setup and Running (without Docker)

If you prefer to run the services directly on your machine:

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install UI dependencies
cd ui/viewer
npm install
cd ../..
```

### 2. Start the RAG Service

```bash
# Create necessary directories
mkdir -p data/processed data/vectors logs

# Start the FastAPI server
cd rag_service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The RAG service will be available at http://localhost:8000

### 3. Run an Agent Framework

You can run any of the implemented agent frameworks:

```bash
# Run CrewAI agent
python -m agents.crewai.runner --topic "Apple Inc"

# Run AutoGen agent
python -m agents.autogen.runner --topic "Tesla Inc"

# Run LangGraph agent
python -m agents.langgraph.runner --topic "Microsoft"

# Run Google ADK agent
python -m agents.googleadk.runner --topic "Amazon"

# Run SquidAI agent
python -m agents.squidai.runner --topic "Meta"

# Run LettaAI agent
python -m agents.lettaai.runner --topic "Netflix"
```

### 4. Start the UI

```bash
cd ui/viewer
npm start
```

The UI will be available at http://localhost:3000

## Running Individual Components

### RAG Service

The RAG service provides three main endpoints:

1. **Ingest data**:
   ```bash
   # Ingest text
   curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text content here", "metadata": {"source": "manual"}}'
   
   # Ingest from URL
   curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article", "metadata": {"source_type": "web"}}'
   ```

2. **Query the RAG service**:
   ```bash
   curl -X GET "http://localhost:8000/query?q=your%20query%20here&top_k=5"
   ```

3. **Check service status**:
   ```bash
   curl -X GET http://localhost:8000/status
   ```

### Agent Runners

Each agent runner can be executed individually:

```bash
# Run with Python
python -m agents.crewai.runner --topic "Company Name" --rag_url "http://localhost:8000"

# Or using the CLI wrapper
./run_agent.sh crewai "Company Name"
```

### Evaluation Script

To evaluate and compare all agent frameworks:

```bash
# Run evaluation on a specific company
python -m tests.evaluate_outputs --company "Apple Inc" --output "results.json"

# Run evaluation with custom parameters
python -m tests.evaluate_outputs --company "Tesla" --output "results.csv" --format csv --top_k 5
```

## Troubleshooting

### Common Issues

1. **RAG Service Connection Issues**:
   - Ensure the RAG service is running and accessible
   - Check that the correct URL is configured in the agent runners

2. **Missing API Keys**:
   - Verify all required API keys are set in the `.env` file
   - For non-Docker setup, ensure environment variables are loaded

3. **Docker Network Issues**:
   - If services can't communicate, check Docker network configuration
   - Use service names as hostnames within the Docker network

4. **Vector Store Errors**:
   - Ensure the data/vectors directory exists and is writable
   - Try ingesting some data before querying

### Logs

Logs are stored in the `logs/` directory:

- RAG service logs: `logs/rag_service/`
- Agent framework logs: `logs/{agent_name}/`
- Evaluation logs: `logs/evaluation/`

## License

[MIT License](LICENSE)
