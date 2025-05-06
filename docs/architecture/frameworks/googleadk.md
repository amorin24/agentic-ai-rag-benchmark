# Google ADK Framework Architecture

This document provides a detailed architecture diagram and explanation for the Google ADK framework implementation in the Agentic AI RAG Benchmark project.

## Overview

Google ADK (Agent Development Kit) is a framework for building AI agents. In this implementation, Google ADK is used to create a research agent that can gather and analyze information about a company, leveraging the RAG service for knowledge retrieval.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                      Google ADK Implementation                      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │  GoogleADKRunner    │                                            │
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
│  │                     Agent Components                        │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Research   │    │  Planning   │    │  Execution  │     │    │
│  │  │  Component  │    │  Component  │    │  Component  │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │   Tools     │      │   Memory    │    │  Callbacks  │          │
│  │             │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ RAG Query   │      │ Short-term  │    │ Log Steps   │          │
│  │ Tool        │      │ Memory      │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Web Search  │      │ Long-term   │    │ Track Time  │          │
│  │ Tool        │      │ Memory      │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Report      │                         │ Count Tokens│          │
│  │ Generator   │                         │             │          │
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

### GoogleADKRunner

The `GoogleADKRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the Google ADK agent
2. Setting up the agent components, tools, and memory
3. Running the agent to perform the company research task
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### Agent Builder

The Agent Builder is responsible for:

1. Creating the agent components
2. Configuring the tools and memory
3. Setting up the callbacks
4. Building the agent with the specified configuration

### Agent Components

The agent consists of three main components:

1. **Research Component**: Responsible for gathering information about the company
2. **Planning Component**: Responsible for planning the research and analysis process
3. **Execution Component**: Responsible for executing the plan and generating the report

### Tools

The tools are utilities that the agent can use to accomplish its tasks. In this implementation, there are three main tools:

1. **RAG Query Tool**: Allows the agent to query the RAG service for relevant information
2. **Web Search Tool**: Simulates a web search to find additional information
3. **Report Generator**: Generates a structured report based on the gathered information

### Memory

The memory system is used to store and retrieve information during the agent's execution. It consists of two main components:

1. **Short-term Memory**: Stores information that is relevant to the current task
2. **Long-term Memory**: Stores information that may be useful for future tasks

### Callbacks

The callbacks are used to track the execution of the agent and collect metrics:

1. **Log Steps**: Logs each step of the execution
2. **Track Time**: Tracks the time taken for each step
3. **Count Tokens**: Counts the number of tokens used in each step

## Data Flow

1. **Agent Execution**:
   - The `GoogleADKRunner` creates an agent with the specified components
   - The Planning Component creates a research plan
   - The Research Component gathers information about the company using the RAG service
   - The Execution Component analyzes the information and generates a report
   - The agent's memory is updated with the gathered information and analysis

2. **RAG Integration**:
   - The RAG Query Tool sends queries to the RAG service
   - The RAG service returns relevant documents
   - The agent uses the retrieved documents to gather information about the company

3. **Logging and Metrics**:
   - The callbacks track the execution steps, time, and token usage
   - The `GoogleADKRunner` logs the execution steps and metrics
   - The output is formatted according to the standardized schema

## Output Format

The output of the `GoogleADKRunner` follows the standardized schema:

```json
{
  "agent_name": "googleadk",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "component": "Planning",
      "action": "Create Research Plan",
      "output": "Research plan..."
    },
    {
      "component": "Research",
      "action": "Gather Information",
      "output": "Research findings..."
    },
    {
      "component": "Execution",
      "action": "Generate Report",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The Google ADK implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The Google ADK implementation uses the following key features of the Google ADK framework:

1. **Component-Based Architecture**: The agent is composed of specialized components
2. **Tool Integration**: The agent can use tools to accomplish its tasks
3. **Memory System**: The agent can store and retrieve information during execution
4. **Callback System**: Callbacks track the execution and collect metrics

For more details on the implementation, see the [Google ADK runner.py](../../../agents/googleadk/runner.py) file.
