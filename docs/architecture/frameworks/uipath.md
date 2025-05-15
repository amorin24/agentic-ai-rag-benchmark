# UiPath Framework Architecture

This document provides a detailed architecture diagram and explanation for the UiPath framework implementation in the Agentic AI RAG Benchmark project.

## Overview

UiPath is a framework for building process automation agents. In this implementation, UiPath is used to create a research agent that can gather and analyze information about a company using automated workflows, leveraging the RAG service for knowledge retrieval. The implementation uses the official UiPath Python SDK (version 2.0.54+) to interact with UiPath Cloud Platform services.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                       UiPath Implementation                         │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │   UiPathRunner      │                                            │
│  │  (AgentRunner)      │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Workflow Planner   │◄───┤   RAG Service       │                │
│  │                     │    │   Integration       │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────────────────┘                │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Data Collection    │◄───┤   Data Structuring  │                │
│  │  Process            │    │   Process           │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────┬───────────┘                │
│            │                          │                            │
│            └──────────────┬───────────┘                            │
│                           │                                         │
│                           ▼                                         │
│  ┌─────────────────────────────────────────┐                        │
│  │                                         │                        │
│  │        Comparative Analysis             │                        │
│  │                                         │                        │
│  └─────────────────────┬─────────────────────┘                      │
│                        │                                            │
│                        ▼                                            │
│  ┌─────────────────────────────────────────┐                        │
│  │                                         │                        │
│  │        Report Generator                 │                        │
│  │                                         │                        │
│  └─────────────────────────────────────────┘                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### UiPathRunner

The `UiPathRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the UiPath agent
2. Planning and executing automated workflows
3. Orchestrating the data collection and analysis processes
4. Generating insights based on the automated analysis
5. Logging the execution steps and metrics

### Workflow Planner

The Workflow Planner component:

1. Plans the research workflow for the given company
2. Defines the sequence of processes to execute
3. Sets parameters for each process
4. Monitors the execution of the workflow

### Data Collection Process

The Data Collection Process component:

1. Retrieves information from the RAG service
2. Collects data about different aspects of the company
3. Organizes the collected data
4. Prepares the data for structuring

### Data Structuring Process

The Data Structuring Process component:

1. Structures the collected data into a standardized format
2. Categorizes information by type and relevance
3. Identifies entities and relationships
4. Creates a structured dataset for analysis

### Comparative Analysis

The Comparative Analysis component:

1. Compares the company with competitors
2. Analyzes performance across different dimensions
3. Identifies strengths and weaknesses
4. Generates insights based on the comparative analysis

### Report Generator

The Report Generator component:

1. Compiles insights from the automated analysis
2. Structures the information in a coherent format
3. Generates a comprehensive research report
4. Includes visualizations and structured data

## Data Flow

1. **Initialization**:
   - The `UiPathRunner` is initialized with the RAG service URL
   - The agent plans the research workflow for the given company

2. **Information Retrieval**:
   - The agent queries the RAG service for different aspects of the company
   - Retrieved information is processed and structured

3. **Automated Workflow Execution**:
   - The data collection process gathers information
   - The data structuring process organizes the information
   - The comparative analysis process analyzes the company and its competitors
   - Each process logs its execution metrics

4. **Analysis**:
   - The structured data is analyzed to extract insights
   - Comparative analysis provides context and benchmarks
   - Automated processes identify patterns and trends

5. **Report Generation**:
   - Insights from the automated analysis are compiled
   - A structured report is generated with sections for different aspects
   - The report includes automated analysis insights

6. **Logging and Metrics**:
   - The execution steps and metrics are logged
   - Token usage and response time are tracked
   - The output is formatted according to the standardized schema

## Output Format

The output of the `UiPathRunner` follows the standardized schema:

```json
{
  "agent_name": "uipath",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "step_id": 1,
      "step_type": "workflow_planning",
      "timestamp": "2023-05-01T10:00:00.000Z",
      "thought": "Planning automation workflow...",
      "workflow": ["Step 1...", "Step 2..."]
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
      "step_type": "process_automation",
      "timestamp": "2023-05-01T10:02:00.000Z",
      "process": "Data Collection",
      "status": "Completed",
      "metrics": {"sources_processed": 4}
    }
  ],
  "token_usage": 1150,
  "response_time": 4.9
}
```

## Configuration

The UiPath implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `UIPATH_PROCESS_TIMEOUT`: Timeout for each process in seconds (default: 60)
- `UIPATH_MAX_SOURCES`: Maximum number of sources to process (default: 10)

## Implementation Details

The UiPath implementation uses the following key features of the UiPath framework:

1. **Workflow Automation**: Automating the research process with defined workflows
2. **Process Orchestration**: Coordinating multiple processes for data collection and analysis
3. **Structured Data Processing**: Processing and structuring data in a standardized format
4. **Comparative Analysis**: Comparing the company with competitors and benchmarks

For more details on the implementation, see the [UiPath runner.py](../../../agents/uipath/runner.py) file.
