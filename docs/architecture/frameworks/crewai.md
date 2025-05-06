# CrewAI Framework Architecture

This document provides a detailed architecture diagram and explanation for the CrewAI framework implementation in the Agentic AI RAG Benchmark project.

## Overview

CrewAI is a framework for creating multi-agent systems with specialized roles. In this implementation, CrewAI is used to simulate a company research task with multiple agents working together to gather and analyze information about a company.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       CrewAI Implementation                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   CrewAIRunner      │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ creates                                                │
│            ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │       Crew          │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ contains                                               │
│            ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │                        Agents                               │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Researcher │    │   Analyst   │    │  Reporter   │     │    │
│  │  │             │    │             │    │             │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │   Tasks     │      │   Tools     │    │  Callbacks  │          │
│  │             │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Research    │      │ RAG Query   │    │ Log Steps   │          │
│  │ Company     │      │ Tool        │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Analyze     │      │ Web Search  │    │ Track Time  │          │
│  │ Information │      │ Tool        │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Create      │                         │ Count Tokens│          │
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

### CrewAIRunner

The `CrewAIRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the CrewAI agents
2. Defining the tasks for each agent
3. Running the crew to perform the company research task
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### Crew

The `Crew` is a collection of agents working together to accomplish a set of tasks. In this implementation, the crew consists of three agents:

1. **Researcher**: Responsible for gathering information about the company
2. **Analyst**: Responsible for analyzing the gathered information
3. **Reporter**: Responsible for creating a final report

### Agents

Each agent in the crew has a specific role and is configured with:

- A name and role description
- A set of tools they can use
- A goal they are trying to achieve
- A backstory that defines their expertise and approach

### Tasks

The tasks define what each agent needs to accomplish. In this implementation, there are three main tasks:

1. **Research Company**: Gather information about the company's latest news, product updates, and financial trends
2. **Analyze Information**: Analyze the gathered information to identify key insights
3. **Create Report**: Create a comprehensive report based on the analysis

### Tools

The tools are utilities that agents can use to accomplish their tasks. In this implementation, there are two main tools:

1. **RAG Query Tool**: Allows agents to query the RAG service for relevant information
2. **Web Search Tool**: Simulates a web search to find additional information

### Callbacks

The callbacks are used to track the execution of the crew and collect metrics. In this implementation, there are three main callbacks:

1. **Log Steps**: Logs each step of the execution
2. **Track Time**: Tracks the time taken for each step
3. **Count Tokens**: Counts the number of tokens used in each step

## Data Flow

1. **Task Execution**:
   - The `CrewAIRunner` creates a crew with three agents
   - Each agent is assigned a specific task
   - The crew executes the tasks in sequence
   - The Researcher gathers information using the RAG Query Tool
   - The Analyst analyzes the information
   - The Reporter creates a final report

2. **RAG Integration**:
   - The RAG Query Tool sends queries to the RAG service
   - The RAG service returns relevant documents
   - The agents use the retrieved documents to accomplish their tasks

3. **Logging and Metrics**:
   - The callbacks track the execution steps, time, and token usage
   - The `CrewAIRunner` logs the execution steps and metrics
   - The output is formatted according to the standardized schema

## Output Format

The output of the `CrewAIRunner` follows the standardized schema:

```json
{
  "agent_name": "crewai",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "agent": "Researcher",
      "task": "Research Company",
      "output": "Research findings..."
    },
    {
      "agent": "Analyst",
      "task": "Analyze Information",
      "output": "Analysis results..."
    },
    {
      "agent": "Reporter",
      "task": "Create Report",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The CrewAI implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agents
- `OPENAI_MODEL`: The OpenAI model to use for the agents
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The CrewAI implementation uses the following key features of the CrewAI framework:

1. **Agent Specialization**: Each agent has a specific role and expertise
2. **Sequential Task Execution**: Tasks are executed in a specific sequence
3. **Tool Usage**: Agents use tools to accomplish their tasks
4. **Callback Tracking**: Callbacks track the execution and collect metrics

For more details on the implementation, see the [CrewAI runner.py](../../../agents/crewai/runner.py) file.
