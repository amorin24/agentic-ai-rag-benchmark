# System Overview

The Agentic AI RAG Benchmark is a framework for evaluating and comparing different agentic AI frameworks using a shared RAG (Retrieval-Augmented Generation) microservice. This document provides a high-level overview of the system architecture.

## System Components

The system consists of the following main components:

1. **RAG Service**: A centralized FastAPI service that provides RAG capabilities
2. **Agent Runners**: Modular implementations for different agent frameworks
3. **UI Viewer**: A React-based interface for comparing outputs
4. **External APIs**: Integration with external data sources
5. **Evaluation Tools**: Tools for evaluating and comparing agent outputs

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                        Agentic AI RAG Benchmark                     │
│                                                                     │
├─────────────┬─────────────────────────────────┬───────────────────┐ │
│             │                                 │                   │ │
│  RAG Service│         Agent Runners           │    UI Viewer      │ │
│             │                                 │                   │ │
├─────────────┤ ┌───────────┐  ┌───────────┐   │ ┌───────────────┐ │ │
│             │ │           │  │           │   │ │               │ │ │
│  ┌─────────┐│ │  CrewAI   │  │  AutoGen  │   │ │  React UI     │ │ │
│  │ FastAPI ││ │  (real)   │  │  (real)   │   │ │               │ │ │
│  └─────────┘│ └───────────┘  └───────────┘   │ └───────────────┘ │ │
│             │                                 │                   │ │
│  ┌─────────┐│ ┌───────────┐  ┌───────────┐   │ ┌───────────────┐ │ │
│  │ FAISS   ││ │ LangGraph │  │Google ADK │   │ │ Comparison    │ │ │
│  └─────────┘│ │  (real)   │  │  (real)   │   │ │ Visualization │ │ │
│             │ └───────────┘  └───────────┘   │ └───────────────┘ │ │
│  ┌─────────┐│ ┌───────────┐  ┌───────────┐   │                   │ │
│  │Embedders││ │  SquidAI  │  │  LettaAI  │   │                   │ │
│  └─────────┘│ │  (mock)   │  │  (mock)   │   │                   │ │
│             │ └───────────┘  └───────────┘   │                   │ │
│             │                                 │                   │ │
│             │ ┌───────────┐  ┌───────────┐   │                   │ │
│             │ │ Portia AI │  │  H2O AI   │   │                   │ │
│             │ │  (mock)   │  │  (mock)   │   │                   │ │
│             │ └───────────┘  └───────────┘   │                   │ │
│             │                                 │                   │ │
│             │ ┌───────────┐                   │                   │ │
│             │ │  UiPath   │                   │                   │ │
│             │ │  (real)   │                   │                   │ │
│             │ └───────────┘                   │                   │ │
│             │                                 │                   │ │
└─────────────┴─────────────────────────────────┴───────────────────┘ │
│                                                                     │
│                         External Data Sources                       │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Wikipedia  │  │   NewsAPI   │  │Financial API│  │    URLs     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Data Ingestion**:
   - External data sources (Wikipedia, NewsAPI, Financial API, URLs) are ingested into the RAG service
   - Data is processed, chunked, and embedded using the embedder module
   - Embeddings are stored in the FAISS vector store

2. **Agent Execution**:
   - Agent runners receive a task (e.g., research a company)
   - Agents query the RAG service to retrieve relevant information
   - Agents process the information and generate a response
   - Execution logs, steps, and metrics are recorded

3. **Evaluation and Comparison**:
   - The evaluation script runs all agent frameworks with the same input
   - Outputs are collected and evaluated based on various metrics
   - Results are stored in a structured format for visualization

4. **Visualization**:
   - The UI viewer displays the outputs and metrics from all agent frameworks
   - Users can compare the results side-by-side
   - Detailed logs and execution steps can be viewed for each agent

## Component Interactions

- **RAG Service ↔ Agent Runners**: Agent runners query the RAG service via HTTP API calls to retrieve relevant information
- **Agent Runners ↔ UI Viewer**: The UI viewer displays the outputs and metrics from the agent runners
- **RAG Service ↔ External Data Sources**: The RAG service ingests data from external sources via API calls or direct file access
- **Evaluation Script ↔ Agent Runners**: The evaluation script runs all agent frameworks and collects their outputs
- **Evaluation Script ↔ UI Viewer**: The UI viewer displays the evaluation results

## Deployment

The system can be deployed using Docker Compose, which orchestrates the following containers:

- **rag_service**: The FastAPI app on port 8000
- **agent_runner**: A Python service that runs one of the agent frameworks on command
- **ui**: React app on port 3000

For more details on deployment, see the [Docker Setup](../setup/docker_setup.md) documentation.
