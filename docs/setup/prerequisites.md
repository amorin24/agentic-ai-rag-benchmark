# Prerequisites

This document outlines the prerequisites for setting up and running the Agentic AI RAG Benchmark project.

## System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **CPU**: 4+ cores recommended for running multiple agent frameworks simultaneously
- **RAM**: 8GB minimum, 16GB+ recommended
- **Storage**: 2GB+ free space for code, dependencies, and data

## Software Requirements

### Core Dependencies

- **Python**: 3.10 or higher
- **Node.js**: 16.x or higher
- **Docker**: 20.10.x or higher (for containerized deployment)
- **Docker Compose**: 2.x or higher

### Python Dependencies

The following Python packages are required:

- **FastAPI**: For the RAG service API
- **FAISS**: For vector storage and similarity search
- **Sentence Transformers**: For text embeddings
- **OpenAI**: For LLM integration
- **CrewAI**: For CrewAI agent framework
- **AutoGen**: For AutoGen agent framework
- **LangGraph**: For LangGraph agent framework
- **Google ADK**: For Google Agent Development Kit
- **SquidAI**: For SquidAI agent framework
- **LettaAI**: For LettaAI agent framework

For a complete list of Python dependencies with version numbers, see the [requirements.txt](../../requirements.txt) file.

### Node.js Dependencies

The following Node.js packages are required for the UI:

- **React**: 18.x or higher
- **TypeScript**: 4.x or higher
- **Tailwind CSS**: 3.x or higher

For a complete list of Node.js dependencies with version numbers, see the [package.json](../../ui/viewer/package.json) file.

## API Keys

The following API keys are required:

- **OpenAI API Key**: Required for LLM integration and embeddings
- **NewsAPI Key**: Required for fetching news articles
- **Financial Modeling Prep API Key**: Required for fetching financial data

## Environment Setup

### Python Environment

It's recommended to use a virtual environment for Python:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Node.js Environment

For the UI component:

```bash
# Navigate to the UI directory
cd ui/viewer

# Install dependencies
npm install
```

### Docker Environment

For containerized deployment:

```bash
# Verify Docker installation
docker --version
docker-compose --version

# Build and start containers
docker-compose up -d
```

## Next Steps

Once you have all the prerequisites installed, proceed to the [Installation](./installation.md) guide for detailed setup instructions.
