# Usage Documentation

This section provides detailed instructions for using the Agentic AI RAG Benchmark project.

## Contents

- [RAG Service](./rag_service.md): Instructions for using the RAG service
- [Agent Frameworks](./agent_frameworks.md): Instructions for using the agent frameworks
- [UI Viewer](./ui_viewer.md): Instructions for using the UI viewer
- [Evaluation](./evaluation.md): Instructions for evaluating agent frameworks

## Quick Start

For a quick start, follow these steps:

1. Start the RAG service:

```bash
# Using Python
python -m rag_service.app.main

# Using Docker
docker-compose up -d rag_service
```

2. Ingest some data:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"content": "Text content to ingest", "metadata": {"source": "manual"}}'

# Using the UI
# Navigate to http://localhost:3000 and use the ingest form
```

3. Run an agent framework:

```bash
# Using Python
python -m agents.runner --topic "Tesla" --framework "crewai"

# Using Docker
AGENT_FRAMEWORK=crewai docker-compose up -d agent_runner
```

4. View the results in the UI:

```bash
# Start the UI
npm start --prefix ui/viewer

# Using Docker
docker-compose up -d ui

# Navigate to http://localhost:3000
```

For more detailed instructions, see the specific documentation pages.
