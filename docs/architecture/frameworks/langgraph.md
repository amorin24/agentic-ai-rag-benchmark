# LangGraph Framework Architecture

This document provides a detailed architecture diagram and explanation for the LangGraph framework implementation in the Agentic AI RAG Benchmark project.

## Overview

LangGraph is a framework for building graph-based workflows with LLMs. In this implementation, LangGraph is used to create a structured workflow for company research, where different nodes in the graph represent different stages of the research process.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                      LangGraph Implementation                       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │  LangGraphRunner    │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ creates                                                │
│            ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   Graph Builder     │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ builds                                                 │
│            ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │                     Graph Nodes                             │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Research   │    │  Analysis   │    │   Report    │     │    │
│  │  │    Node     │    │    Node     │    │    Node     │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │   State     │      │   Edges     │    │  Callbacks  │          │
│  │  Manager    │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Company     │      │ Research    │    │ Log Steps   │          │
│  │ Information │      │ -> Analysis │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Research    │      │ Analysis    │    │ Track Time  │          │
│  │ Results     │      │ -> Report   │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Final       │                         │ Count Tokens│          │
│  │ Report      │                         │             │          │
│  └─────────────┘                         └─────────────┘          │
│                                                                     │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ queries
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                           RAG Service                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### LangGraphRunner

The `LangGraphRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the LangGraph workflow
2. Defining the nodes and edges of the graph
3. Running the graph to perform the company research task
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### Graph Builder

The Graph Builder is responsible for:

1. Creating the nodes of the graph
2. Defining the edges between nodes
3. Configuring the state manager
4. Setting up the callbacks

### Graph Nodes

The graph consists of three main nodes:

1. **Research Node**: Responsible for gathering information about the company
2. **Analysis Node**: Responsible for analyzing the gathered information
3. **Report Node**: Responsible for creating a final report

### State Manager

The State Manager is responsible for:

1. Maintaining the state of the graph execution
2. Storing intermediate results between nodes
3. Providing access to the state for nodes and callbacks

The state includes:

1. **Company Information**: Basic information about the company
2. **Research Results**: Information gathered during the research phase
3. **Final Report**: The final output of the graph execution

### Edges

The edges define the flow of execution between nodes:

1. **Research -> Analysis**: After gathering information, proceed to analysis
2. **Analysis -> Report**: After analyzing information, proceed to report generation

### Callbacks

The callbacks are used to track the execution of the graph and collect metrics:

1. **Log Steps**: Logs each step of the execution
2. **Track Time**: Tracks the time taken for each step
3. **Count Tokens**: Counts the number of tokens used in each step

## Data Flow

1. **Graph Execution**:
   - The `LangGraphRunner` creates a graph with three nodes
   - The graph execution starts with the Research Node
   - The Research Node gathers information about the company using the RAG service
   - The state is updated with the research results
   - The execution proceeds to the Analysis Node
   - The Analysis Node analyzes the information in the state
   - The state is updated with the analysis results
   - The execution proceeds to the Report Node
   - The Report Node creates a final report based on the state
   - The state is updated with the final report

2. **RAG Integration**:
   - The Research Node sends queries to the RAG service
   - The RAG service returns relevant documents
   - The documents are stored in the state for use by other nodes

3. **Logging and Metrics**:
   - The callbacks track the execution steps, time, and token usage
   - The `LangGraphRunner` logs the execution steps and metrics
   - The output is formatted according to the standardized schema

## Output Format

The output of the `LangGraphRunner` follows the standardized schema:

```json
{
  "agent_name": "langgraph",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "node": "Research",
      "input": "Company name",
      "output": "Research findings..."
    },
    {
      "node": "Analysis",
      "input": "Research findings",
      "output": "Analysis results..."
    },
    {
      "node": "Report",
      "input": "Analysis results",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The LangGraph implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the nodes
- `OPENAI_MODEL`: The OpenAI model to use for the nodes
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The LangGraph implementation uses the following key features of the LangGraph framework:

1. **Graph-Based Workflow**: The research process is modeled as a graph with nodes and edges
2. **State Management**: The state is used to store and share information between nodes
3. **Conditional Execution**: The graph can include conditional edges for more complex workflows
4. **Callback System**: Callbacks track the execution and collect metrics

For more details on the implementation, see the [LangGraph runner.py](../../../agents/langgraph/runner.py) file.
