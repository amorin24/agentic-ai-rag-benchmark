# LettaAI Framework Architecture

This document provides a detailed architecture diagram and explanation for the LettaAI framework implementation in the Agentic AI RAG Benchmark project.

## Overview

LettaAI is a framework for building memory-augmented agents. In this implementation, LettaAI is used to create a research agent that can gather and analyze information about a company, with a focus on maintaining and utilizing memory for more coherent and contextual research.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       LettaAI Implementation                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   LettaAIRunner     │                                            │
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
│  │                     Memory System                           │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Episodic   │    │  Semantic   │    │ Procedural  │     │    │
│  │  │   Memory    │    │   Memory    │    │   Memory    │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │  Research   │      │  Analysis   │    │  Reporting  │          │
│  │  Workflow   │      │  Workflow   │    │  Workflow   │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Initialize  │      │ Analyze     │    │ Generate    │          │
│  │ Memory      │      │ Company     │    │ Report      │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Gather      │      │ Update      │    │ Consolidate │          │
│  │ Information │      │ Memory      │    │ Memory      │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│  ┌─────────────┐                         ┌─────────────┐          │
│  │ Update      │                         │ Finalize    │          │
│  │ Memory      │                         │ Report      │          │
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

### LettaAIRunner

The `LettaAIRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the LettaAI agent
2. Setting up the memory system
3. Running the agent to perform the company research task
4. Logging the execution steps and metrics
5. Formatting the output according to the standardized schema

### Agent Builder

The Agent Builder is responsible for:

1. Creating the memory system
2. Configuring the workflows
3. Setting up the callbacks
4. Building the agent with the specified configuration

### Memory System

The memory system is the core of the LettaAI framework and consists of three main components:

1. **Episodic Memory**: Stores specific events and experiences during the research process
2. **Semantic Memory**: Stores factual information about the company
3. **Procedural Memory**: Stores information about how to perform research tasks

### Workflows

The agent uses three main workflows:

1. **Research Workflow**: Responsible for gathering information about the company
2. **Analysis Workflow**: Responsible for analyzing the gathered information
3. **Reporting Workflow**: Responsible for generating the final report

### Research Workflow

The Research Workflow consists of three main steps:

1. **Initialize Memory**: Sets up the memory system with basic information about the company
2. **Gather Information**: Queries the RAG service for information about the company
3. **Update Memory**: Updates the memory system with the gathered information

### Analysis Workflow

The Analysis Workflow consists of two main steps:

1. **Analyze Company**: Analyzes the information in the memory system
2. **Update Memory**: Updates the memory system with the analysis results

### Reporting Workflow

The Reporting Workflow consists of three main steps:

1. **Generate Report**: Creates a draft report based on the memory system
2. **Consolidate Memory**: Consolidates the memory system for final report generation
3. **Finalize Report**: Creates the final report

## Data Flow

1. **Memory Initialization**:
   - The `LettaAIRunner` creates an agent with the memory system
   - The Research Workflow initializes the memory system with basic information about the company

2. **Information Gathering**:
   - The Research Workflow queries the RAG service for information about the company
   - The gathered information is stored in the memory system
   - The memory system is updated with the new information

3. **Analysis**:
   - The Analysis Workflow analyzes the information in the memory system
   - The analysis results are stored in the memory system
   - The memory system is updated with the analysis results

4. **Report Generation**:
   - The Reporting Workflow generates a draft report based on the memory system
   - The memory system is consolidated for final report generation
   - The final report is generated

5. **Logging and Metrics**:
   - The `LettaAIRunner` logs the execution steps, time, and token usage
   - The output is formatted according to the standardized schema

## Output Format

The output of the `LettaAIRunner` follows the standardized schema:

```json
{
  "agent_name": "lettaai",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "workflow": "Research",
      "step": "Initialize Memory",
      "output": "Memory initialized..."
    },
    {
      "workflow": "Research",
      "step": "Gather Information",
      "output": "Information gathered..."
    },
    {
      "workflow": "Research",
      "step": "Update Memory",
      "output": "Memory updated..."
    },
    {
      "workflow": "Analysis",
      "step": "Analyze Company",
      "output": "Analysis results..."
    },
    {
      "workflow": "Analysis",
      "step": "Update Memory",
      "output": "Memory updated..."
    },
    {
      "workflow": "Reporting",
      "step": "Generate Report",
      "output": "Draft report..."
    },
    {
      "workflow": "Reporting",
      "step": "Consolidate Memory",
      "output": "Memory consolidated..."
    },
    {
      "workflow": "Reporting",
      "step": "Finalize Report",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

## Configuration

The LettaAI implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `RAG_SERVICE_HOST`: The host of the RAG service
- `RAG_SERVICE_PORT`: The port of the RAG service

## Implementation Details

The LettaAI implementation uses the following key features of the LettaAI framework:

1. **Memory-Augmented Architecture**: The agent uses a sophisticated memory system to store and retrieve information
2. **Workflow-Based Execution**: The agent uses workflows to organize the research process
3. **Memory Consolidation**: The agent consolidates memory for more coherent report generation
4. **Contextual Understanding**: The agent uses memory to maintain context throughout the research process

For more details on the implementation, see the [LettaAI runner.py](../../../agents/lettaai/runner.py) file.
