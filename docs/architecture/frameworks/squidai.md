# SquidAI Framework Architecture

This document provides a detailed architecture diagram and explanation for the SquidAI framework implementation in the Agentic AI RAG Benchmark project.

## Overview

SquidAI is a framework for building tool-using agents. In this implementation, SquidAI is used to create a research agent that uses specialized tools to gather and analyze information about a company, leveraging the RAG service for knowledge retrieval.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       SquidAI Implementation                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   SquidAIRunner     │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ creates                                                │
│            ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   Agent Builder     │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ builds                                                 │
│            ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │                        Tools                                │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Company    │    │   News      │    │  Financial  │     │    │
│  │  │  Profiler   │    │   Analyzer  │    │  Analyzer   │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Product    │    │  Sentiment  │    │   Report    │     │    │
│  │  │  Researcher │    │  Analyzer   │    │  Generator  │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │ Tool Manager│      │   Memory    │    │  Callbacks  │          │
│  │             │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Tool        │      │ Working     │    │ Log Steps   │          │
│  │ Selection   │      │ Memory      │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Tool        │      │ Tool        │    │ Track Time  │          │
│  │ Execution   │      │ Results     │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Result      │                         │ Count Tokens│          │
│  │ Integration │                         │             │          │
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

### SquidAIRunner

The `SquidAIRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the SquidAI agent
2. Setting up the specialized tools for company research
3. Running the agent to perform the company research task
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### Agent Builder

The Agent Builder is responsible for:

1. Creating the specialized tools
2. Configuring the tool manager
3. Setting up the memory system
4. Configuring the callbacks

### Tools

The agent uses six specialized tools:

1. **Company Profiler**: Gathers basic information about the company (industry, size, location, etc.)
2. **News Analyzer**: Analyzes recent news articles about the company
3. **Financial Analyzer**: Analyzes financial data and trends
4. **Product Researcher**: Researches the company's products and services
5. **Sentiment Analyzer**: Analyzes sentiment around the company and its products
6. **Report Generator**: Generates a comprehensive report based on the gathered information

### Tool Manager

The Tool Manager is responsible for:

1. **Tool Selection**: Selecting the appropriate tool for each task
2. **Tool Execution**: Executing the selected tool with the appropriate parameters
3. **Result Integration**: Integrating the results from different tools

### Memory

The memory system is used to store and retrieve information during the agent's execution:

1. **Working Memory**: Stores the current state of the research
2. **Tool Results**: Stores the results from each tool execution

### Callbacks

The callbacks are used to track the execution of the agent and collect metrics:

1. **Log Steps**: Logs each step of the execution
2. **Track Time**: Tracks the time taken for each step
3. **Count Tokens**: Counts the number of tokens used in each step

## Data Flow

1. **Agent Execution**:
   - The `SquidAIRunner` creates an agent with the specialized tools
   - The agent selects the appropriate tool for each research task
   - Each tool queries the RAG service for relevant information
   - The tool processes the information and returns results
   - The agent integrates the results from different tools
   - The Report Generator tool creates a comprehensive report

2. **RAG Integration**:
   - Each tool sends queries to the RAG service
   - The RAG service returns relevant documents
   - The tools process the retrieved documents to extract specific information

3. **Logging and Metrics**:
   - The callbacks track the execution steps, time, and token usage
   - The `SquidAIRunner` logs the execution steps and metrics
   - The output is formatted according to the standardized schema

## Output Format

The output of the `SquidAIRunner` follows the standardized schema:

```json
{
  "agent_name": "squidai",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "tool": "Company Profiler",
      "input": "Company name",
      "output": "Company profile..."
    },
    {
      "tool": "News Analyzer",
      "input": "Company name",
      "output": "News analysis..."
    },
    {
      "tool": "Financial Analyzer",
      "input": "Company name",
      "output": "Financial analysis..."
    },
    {
      "tool": "Product Researcher",
      "input": "Company name",
      "output": "Product research..."
    },
    {
      "tool": "Sentiment Analyzer",
      "input": "Company name",
      "output": "Sentiment analysis..."
    },
    {
      "tool": "Report Generator",
      "input": "All previous results",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The SquidAI implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The SquidAI implementation uses the following key features of the SquidAI framework:

1. **Tool-Based Architecture**: The agent uses specialized tools for different research tasks
2. **Tool Selection**: The agent selects the appropriate tool for each task
3. **Memory System**: The agent stores and retrieves information during execution
4. **Callback System**: Callbacks track the execution and collect metrics

For more details on the implementation, see the [SquidAI runner.py](../../../agents/squidai/runner.py) file.
