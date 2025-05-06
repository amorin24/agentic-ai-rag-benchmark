# UI Viewer Architecture

This document provides a detailed architecture diagram and explanation for the UI Viewer component of the Agentic AI RAG Benchmark project.

## Overview

The UI Viewer is a React-based interface that allows users to compare the outputs of different agent frameworks side-by-side. It provides a visual representation of the agent outputs, execution steps, and metrics, making it easier to evaluate and compare the performance of different agent frameworks.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                           UI Viewer                                 │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │     React App       │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ contains                                               │
│            ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │                     Components                              │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Company    │    │  Agent      │    │  Comparison │     │    │
│  │  │  Selector   │    │  Outputs    │    │  View       │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │  Metrics    │    │  Execution  │    │  Settings   │     │    │
│  │  │  Display    │    │  Steps      │    │  Panel      │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │                                                             │    │
│  └────────┬──────────────────┬──────────────────┬─────────────┘    │
│           │                  │                  │                  │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │   State     │      │   API       │    │   Utilities │          │
│  │  Management │      │  Client     │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                  │                   │
│        │                    │                  │                   │
│        ▼                    ▼                  ▼                   │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │ Company     │      │ Fetch       │    │ Format      │          │
│  │ State       │      │ Agent       │    │ Output      │          │
│  └─────────────┘      │ Outputs     │    └─────────────┘          │
│  ┌─────────────┐      └─────────────┘    ┌─────────────┐          │
│  │ Agent       │      ┌─────────────┐    │ Calculate   │          │
│  │ Outputs     │      │ Trigger     │    │ Metrics     │          │
│  └─────────────┘      │ Agent Runs  │    └─────────────┘          │
│  ┌─────────────┐      └─────────────┘    ┌─────────────┐          │
│  │ UI          │                         │ Visualize   │          │
│  │ State       │                         │ Data        │          │
│  └─────────────┘                         └─────────────┘          │
│                                                                     │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ communicates with
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                         Backend Services                            │
│                                                                     │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐           │
│  │             │      │             │    │             │           │
│  │ RAG Service │      │ Agent       │    │ Evaluation  │           │
│  │             │      │ Runners     │    │ Service     │           │
│  └─────────────┘      └─────────────┘    └─────────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### React App

The React App is the main entry point for the UI Viewer. It is built using TypeScript and Tailwind CSS for styling.

### Components

The UI Viewer consists of several key components:

#### Company Selector

The Company Selector component allows users to:

1. Select a company or topic from a predefined list
2. Enter a custom company or topic
3. Trigger the agent runners to perform research on the selected company

#### Agent Outputs

The Agent Outputs component displays the final output of each agent framework. It includes:

1. A tabbed interface to switch between different agent frameworks
2. A formatted display of the agent's final output
3. Options to expand or collapse sections of the output

#### Comparison View

The Comparison View component allows users to compare the outputs of different agent frameworks side-by-side. It includes:

1. A grid layout with columns for each agent framework
2. Synchronized scrolling for easier comparison
3. Highlighting of differences between outputs

#### Metrics Display

The Metrics Display component shows performance metrics for each agent framework. It includes:

1. Token usage
2. Response time
3. Factual overlap with RAG context
4. Reasoning clarity score

#### Execution Steps

The Execution Steps component displays the steps taken by each agent framework during the research process. It includes:

1. A timeline of execution steps
2. Details of each step, including input and output
3. Timestamps for each step

#### Settings Panel

The Settings Panel component allows users to configure the UI Viewer. It includes:

1. Display options (e.g., light/dark mode, layout)
2. Comparison settings (e.g., metrics to display)
3. Agent framework selection

### State Management

The UI Viewer uses a state management system to store and update the application state. It includes:

1. **Company State**: Information about the selected company or topic
2. **Agent Outputs**: The outputs of each agent framework
3. **UI State**: The current state of the UI (e.g., selected tabs, expanded sections)

### API Client

The API Client is responsible for communicating with the backend services. It includes:

1. **Fetch Agent Outputs**: Retrieves the outputs of agent frameworks from the backend
2. **Trigger Agent Runs**: Triggers the agent runners to perform research on a selected company

### Utilities

The Utilities module provides helper functions for the UI Viewer. It includes:

1. **Format Output**: Formats the agent outputs for display
2. **Calculate Metrics**: Calculates performance metrics based on agent outputs
3. **Visualize Data**: Provides visualization utilities for metrics and comparisons

## Data Flow

1. **Company Selection**:
   - The user selects a company or topic using the Company Selector component
   - The company state is updated with the selected company
   - The API Client triggers the agent runners to perform research on the selected company

2. **Agent Execution**:
   - The agent runners perform research on the selected company
   - The outputs are sent back to the UI Viewer
   - The agent outputs state is updated with the new outputs

3. **Output Display**:
   - The Agent Outputs component displays the final output of each agent framework
   - The Metrics Display component shows performance metrics
   - The Execution Steps component displays the steps taken by each agent framework

4. **Comparison**:
   - The Comparison View component allows users to compare outputs side-by-side
   - The user can switch between different views and metrics
   - The UI state is updated based on user interactions

## Implementation Details

The UI Viewer is implemented using:

1. **React**: A JavaScript library for building user interfaces
2. **TypeScript**: A typed superset of JavaScript
3. **Tailwind CSS**: A utility-first CSS framework
4. **Axios**: A promise-based HTTP client for making API requests
5. **React Router**: A routing library for React applications
6. **React Query**: A data fetching library for React applications

The UI Viewer is designed to be:

1. **Responsive**: Works on different screen sizes
2. **Accessible**: Follows accessibility best practices
3. **Performant**: Optimized for performance
4. **Maintainable**: Well-structured and documented code

## Configuration

The UI Viewer is configured using environment variables:

- `REACT_APP_RAG_SERVICE_URL`: The URL of the RAG service
- `REACT_APP_AGENT_RUNNER_URL`: The URL of the agent runner service
- `REACT_APP_EVALUATION_SERVICE_URL`: The URL of the evaluation service

## Deployment

The UI Viewer can be deployed using Docker:

```bash
docker-compose up ui
```

For more details on deployment, see the [Docker Setup](../setup/docker_setup.md) documentation.
