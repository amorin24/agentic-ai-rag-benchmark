# Portia AI Framework Architecture (Mock Implementation)

This document provides a detailed architecture diagram and explanation for the Portia AI framework implementation in the Agentic AI RAG Benchmark project. Note that this is a **mock implementation** as the Portia AI framework does not actually exist on PyPI.

## Overview

Portia AI is a simulated framework for building knowledge graph-enhanced agents. In this mock implementation, Portia AI is used to create a research agent that can gather and analyze information about a company using knowledge graph techniques, leveraging the RAG service for knowledge retrieval. The implementation simulates the behavior of a knowledge graph-enhanced agent framework without requiring the actual framework package.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       Portia AI Implementation                      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   PortiaAIRunner    │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Knowledge Graph    │◄───┤   RAG Service       │                │
│  │  Builder            │    │   Integration       │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────────────────┘                │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Entity Analysis    │◄───┤   Relationship      │                │
│  │  Component          │    │   Mapping           │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────────────────┘                │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │  Report Generator   │                                            │
│  │                     │                                            │
│  └─────────────────────┘                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### PortiaAIRunner

The `PortiaAIRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the Portia AI agent
2. Building a knowledge graph from retrieved information
3. Analyzing entities and relationships in the knowledge graph
4. Generating insights based on the knowledge graph analysis
5. Logging the execution steps and metrics

### Knowledge Graph Builder

The Knowledge Graph Builder component:

1. Processes information retrieved from the RAG service
2. Identifies entities (company, products, markets, etc.)
3. Creates a structured knowledge graph representation
4. Stores the graph for further analysis

### Entity Analysis Component

The Entity Analysis component:

1. Analyzes entities in the knowledge graph
2. Identifies important attributes and properties
3. Extracts insights about the company and its ecosystem
4. Provides structured analysis for the report

### Relationship Mapping

The Relationship Mapping component:

1. Identifies relationships between entities
2. Maps connections between the company and other entities
3. Analyzes the strength and nature of relationships
4. Provides context for entity analysis

### Report Generator

The Report Generator component:

1. Compiles insights from the knowledge graph analysis
2. Structures the information in a coherent format
3. Generates a comprehensive research report
4. Includes visualizations and structured data

## Data Flow

1. **Initialization**:
   - The `PortiaAIRunner` is initialized with the RAG service URL
   - The agent plans the research approach for the given company

2. **Information Retrieval**:
   - The agent queries the RAG service for different aspects of the company
   - Retrieved information is processed and structured

3. **Knowledge Graph Construction**:
   - Entities are extracted from the retrieved information
   - Relationships between entities are identified
   - A knowledge graph is constructed to represent the company ecosystem

4. **Analysis**:
   - The knowledge graph is analyzed to extract insights
   - Entity attributes and relationships are evaluated
   - Patterns and important connections are identified

5. **Report Generation**:
   - Insights from the knowledge graph analysis are compiled
   - A structured report is generated with sections for different aspects
   - The report includes knowledge graph-based insights

6. **Logging and Metrics**:
   - The execution steps and metrics are logged
   - Token usage and response time are tracked
   - The output is formatted according to the standardized schema

## Output Format

The output of the `PortiaAIRunner` follows the standardized schema:

```json
{
  "agent_name": "portiaai",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "step_id": 1,
      "step_type": "planning",
      "timestamp": "2023-05-01T10:00:00.000Z",
      "thought": "Planning research approach...",
      "plan": ["Step 1...", "Step 2..."]
    },
    {
      "step_id": 2,
      "step_type": "rag_query",
      "timestamp": "2023-05-01T10:01:00.000Z",
      "query": "Company information...",
      "results": [{"text": "..."}]
    },
    {
      "step_id": 3,
      "step_type": "knowledge_graph",
      "timestamp": "2023-05-01T10:02:00.000Z",
      "entities": ["Entity 1", "Entity 2"],
      "relations": ["Relation 1", "Relation 2"]
    }
  ],
  "token_usage": 1250,
  "response_time": 5.2
}
```

## Configuration

The Portia AI implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `PORTIAAI_ENTITY_THRESHOLD`: Threshold for entity extraction (default: 0.7)
- `PORTIAAI_RELATION_THRESHOLD`: Threshold for relationship mapping (default: 0.6)

## Implementation Details

The Portia AI implementation uses the following key features of the Portia AI framework:

1. **Knowledge Graph Construction**: Building a structured representation of entities and relationships
2. **Entity Recognition**: Identifying and categorizing entities in the retrieved information
3. **Relationship Mapping**: Identifying connections between entities
4. **Graph-Based Analysis**: Extracting insights from the knowledge graph structure

For more details on the implementation, see the [Portia AI runner.py](../../../agents/portiaai/runner.py) file.
