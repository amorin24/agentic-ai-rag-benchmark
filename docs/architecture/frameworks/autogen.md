# AutoGen Framework Architecture

This document provides a detailed architecture diagram and explanation for the AutoGen framework implementation in the Agentic AI RAG Benchmark project.

## Overview

AutoGen is a framework for building conversational agents with LLMs. In this implementation, AutoGen is used to create a multi-agent conversation system for company research, where different agents with specialized roles collaborate to gather and analyze information about a company.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       AutoGen Implementation                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   AutoGenRunner     │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ creates                                                │
│            ▼                                                        │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   AgentGroup        │                                            │
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
│  │  │  Researcher │    │   Analyst   │    │  Financial  │     │    │
│  │  │             │    │             │    │   Expert    │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │ Conversation│      │   Tools     │    │  Functions  │          │
│  │  Manager    │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Initiate    │      │ RAG Query   │    │ Query RAG   │          │
│  │ Conversation│      │ Tool        │    │ Service     │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Manage      │      │ Web Search  │    │ Format      │          │
│  │ Messages    │      │ Tool        │    │ Results     │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Generate    │                         │ Generate    │          │
│  │ Final Report│                         │ Report      │          │
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

### AutoGenRunner

The `AutoGenRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the AutoGen agents
2. Setting up the agent group for conversation
3. Initiating and managing the conversation
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### AgentGroup

The `AgentGroup` is a collection of agents that can communicate with each other. In this implementation, the agent group consists of three agents:

1. **Researcher**: Responsible for gathering information about the company
2. **Analyst**: Responsible for analyzing the gathered information
3. **Financial Expert**: Responsible for analyzing financial data and trends

### Agents

Each agent in the group has a specific role and is configured with:

- A name and role description
- A set of functions they can call
- A system message that defines their expertise and approach

### Conversation Manager

The conversation manager is responsible for:

1. Initiating the conversation with a specific task
2. Managing the message flow between agents
3. Determining when the conversation is complete
4. Generating the final report

### Tools

The tools are utilities that agents can use to accomplish their tasks. In this implementation, there are two main tools:

1. **RAG Query Tool**: Allows agents to query the RAG service for relevant information
2. **Web Search Tool**: Simulates a web search to find additional information

### Functions

The functions are callable methods that agents can use to perform specific tasks. In this implementation, there are three main functions:

1. **Query RAG Service**: Sends a query to the RAG service and returns the results
2. **Format Results**: Formats the results from the RAG service for better readability
3. **Generate Report**: Generates a structured report based on the conversation

## Data Flow

1. **Conversation Initiation**:
   - The `AutoGenRunner` creates an agent group with three agents
   - The conversation is initiated with a specific task (research a company)
   - The Researcher agent starts gathering information

2. **Information Gathering and Analysis**:
   - The Researcher agent uses the RAG Query Tool to retrieve information
   - The Analyst agent analyzes the information
   - The Financial Expert provides insights on financial data
   - Agents communicate with each other to share information and insights

3. **Report Generation**:
   - After sufficient information is gathered and analyzed
   - The agents collaborate to generate a final report
   - The report includes insights on the company's latest news, product updates, and financial trends

4. **Logging and Metrics**:
   - The `AutoGenRunner` logs the conversation steps
   - Metrics such as token usage and response time are tracked
   - The output is formatted according to the standardized schema

## Output Format

The output of the `AutoGenRunner` follows the standardized schema:

```json
{
  "agent_name": "autogen",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "agent": "Researcher",
      "message": "I'll gather information about the company...",
      "timestamp": "2023-05-06T14:30:00Z"
    },
    {
      "agent": "Analyst",
      "message": "Based on the information gathered...",
      "timestamp": "2023-05-06T14:35:00Z"
    },
    {
      "agent": "Financial Expert",
      "message": "Looking at the financial data...",
      "timestamp": "2023-05-06T14:40:00Z"
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The AutoGen implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agents
- `OPENAI_MODEL`: The OpenAI model to use for the agents
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The AutoGen implementation uses the following key features of the AutoGen framework:

1. **Multi-Agent Conversation**: Agents communicate with each other to share information and insights
2. **Function Calling**: Agents can call functions to perform specific tasks
3. **Tool Usage**: Agents can use tools to gather information
4. **Conversation Management**: The conversation is managed to ensure it stays on topic and reaches a conclusion

For more details on the implementation, see the [AutoGen runner.py](../../../agents/autogen/runner.py) file.
