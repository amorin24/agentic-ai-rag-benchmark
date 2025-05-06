# Architecture Documentation

This section provides detailed architecture diagrams and explanations for each component and framework in the Agentic AI RAG Benchmark project.

## Contents

- [System Overview](./system_overview.md): High-level overview of the entire system
- [RAG Service](./rag_service.md): Architecture of the centralized RAG service
- [Agent Frameworks](./frameworks/README.md): Architecture of the agent frameworks
  - [CrewAI](./frameworks/crewai.md)
  - [AutoGen](./frameworks/autogen.md)
  - [LangGraph](./frameworks/langgraph.md)
  - [Google ADK](./frameworks/googleadk.md)
  - [SquidAI](./frameworks/squidai.md)
  - [LettaAI](./frameworks/lettaai.md)
- [UI Viewer](./ui_viewer.md): Architecture of the UI viewer component

## System Architecture Overview

The Agentic AI RAG Benchmark project consists of three main components:

1. **RAG Service**: A centralized FastAPI service that provides RAG capabilities using FAISS for vector retrieval
2. **Agent Runners**: Modular implementations for different agent frameworks that use the RAG service
3. **UI Viewer**: A React-based interface for comparing outputs from different agent frameworks

These components interact with each other through well-defined APIs and data flows, as described in the [System Overview](./system_overview.md) documentation.
