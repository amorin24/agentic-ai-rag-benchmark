# Installation Guide

This document provides step-by-step instructions for installing the Agentic AI RAG Benchmark project.

## Clone the Repository

```bash
# Clone the repository
git clone https://github.com/amorin24/agentic-ai-rag-benchmark.git

# Navigate to the project directory
cd agentic-ai-rag-benchmark
```

## Python Setup

### Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### Install Python Dependencies

```bash
# Install dependencies
pip install -r requirements.txt
```

## Node.js Setup

### Install Node.js Dependencies

```bash
# Navigate to the UI directory
cd ui/viewer

# Install dependencies
npm install
```

## Docker Setup

If you prefer to use Docker for deployment, you can skip the Python and Node.js setup steps and use the Docker Compose configuration:

```bash
# Build and start containers
docker-compose up -d
```

For more details on Docker deployment, see the [Docker Setup](./docker_setup.md) documentation.

## Configuration

After installation, you need to configure the project by setting up the environment variables. See the [Configuration](./configuration.md) documentation for details.

## Directory Structure

The project has the following directory structure:

```
agentic-ai-rag-benchmark/
├── agents/                # Agent framework implementations
│   ├── autogen/          # AutoGen implementation
│   ├── crewai/           # CrewAI implementation
│   ├── googleadk/        # Google ADK implementation
│   ├── langgraph/        # LangGraph implementation
│   ├── lettaai/          # LettaAI implementation
│   ├── squidai/          # SquidAI implementation
│   └── base_agent_runner.py  # Base agent runner class
├── data/                 # Data storage
│   ├── processed/        # Processed documents
│   └── vectors/          # FAISS indexes
├── docs/                 # Documentation
├── external/             # External API integrations
│   ├── fmp_api.py        # Financial Modeling Prep API
│   └── news_api.py       # NewsAPI integration
├── logs/                 # Log files
├── rag_service/          # RAG service implementation
│   ├── app/              # FastAPI application
│   ├── embedder.py       # Embedding logic
│   ├── ingest.py         # Data ingestion
│   └── retriever.py      # FAISS retrieval
├── tests/                # Test files
├── ui/                   # User interface
│   └── viewer/           # React-based UI
├── utils/                # Utility functions
│   └── config.py         # Configuration utilities
├── .env                  # Environment variables
├── docker-compose.yml    # Docker Compose configuration
└── requirements.txt      # Python dependencies
```

## Verify Installation

To verify that the installation was successful, you can run the following commands:

```bash
# Verify RAG service
python -m rag_service.app.main

# Verify UI (in a separate terminal)
cd ui/viewer
npm start
```

If everything is set up correctly, you should be able to access:
- RAG service at http://localhost:8000
- UI at http://localhost:3000

## Next Steps

After installation, proceed to the [Configuration](./configuration.md) guide to set up the environment variables and configure the project.
