# H2O AI Framework Architecture

This document provides a detailed architecture diagram and explanation for the H2O AI framework implementation in the Agentic AI RAG Benchmark project.

## Overview

H2O AI is a framework for building predictive analytics and machine learning-powered agents. In this implementation, H2O AI is used to create a research agent that can gather and analyze information about a company using predictive analytics techniques, leveraging the RAG service for knowledge retrieval.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                        H2O AI Implementation                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │    H2OAIRunner      │                                            │
│  │   (AgentRunner)     │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Data Preprocessing │◄───┤   RAG Service       │                │
│  │  Component          │    │   Integration       │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────────────────┘                │
│            │                                                        │
│            ▼                                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                │
│  │                     │    │                     │                │
│  │  Time Series        │    │   Market            │                │
│  │  Analysis           │◄───┤   Segmentation      │                │
│  │                     │    │                     │                │
│  └─────────┬───────────┘    └─────────────────────┘                │
│            │                        │                               │
│            └────────────┬───────────┘                               │
│                         │                                           │
│                         ▼                                           │
│  ┌─────────────────────────────────────────┐                        │
│  │                                         │                        │
│  │        Predictive Modeling              │                        │
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

### H2OAIRunner

The `H2OAIRunner` class extends the base `AgentRunner` class and is responsible for:

1. Creating and configuring the H2O AI agent
2. Preprocessing data retrieved from the RAG service
3. Running predictive analytics on the company data
4. Generating insights based on the predictive models
5. Logging the execution steps and metrics

### Data Preprocessing Component

The Data Preprocessing component:

1. Cleans and structures the data retrieved from the RAG service
2. Performs feature engineering on the data
3. Normalizes and transforms the data for analysis
4. Prepares the data for predictive modeling

### Time Series Analysis

The Time Series Analysis component:

1. Analyzes financial and performance data over time
2. Identifies trends, seasonality, and patterns
3. Forecasts future performance based on historical data
4. Provides insights on growth trajectory and potential fluctuations

### Market Segmentation

The Market Segmentation component:

1. Identifies key market segments for the company
2. Analyzes the company's position in each segment
3. Compares performance across different segments
4. Identifies opportunities for growth in specific segments

### Predictive Modeling

The Predictive Modeling component:

1. Builds predictive models using the preprocessed data
2. Evaluates multiple model types (Random Forest, Gradient Boosting, etc.)
3. Selects the best-performing model for predictions
4. Generates forecasts and predictions for key metrics

### Report Generator

The Report Generator component:

1. Compiles insights from the predictive analytics
2. Structures the information in a coherent format
3. Generates a comprehensive research report
4. Includes data-driven insights and forecasts

## Data Flow

1. **Initialization**:
   - The `H2OAIRunner` is initialized with the RAG service URL
   - The agent plans the research approach for the given company

2. **Information Retrieval**:
   - The agent queries the RAG service for different aspects of the company
   - Retrieved information is processed and structured

3. **Data Preprocessing**:
   - The data is cleaned and normalized
   - Features are engineered for predictive modeling
   - The data is transformed into a suitable format for analysis

4. **Predictive Analytics**:
   - Time series analysis is performed on financial data
   - Market segmentation is applied to identify key segments
   - Predictive models are built and evaluated
   - Forecasts are generated for key metrics

5. **Report Generation**:
   - Insights from the predictive analytics are compiled
   - A structured report is generated with sections for different aspects
   - The report includes data-driven insights and forecasts

6. **Logging and Metrics**:
   - The execution steps and metrics are logged
   - Token usage and response time are tracked
   - The output is formatted according to the standardized schema

## Output Format

The output of the `H2OAIRunner` follows the standardized schema:

```json
{
  "agent_name": "h2oai",
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
      "step_type": "data_preprocessing",
      "timestamp": "2023-05-01T10:02:00.000Z",
      "preprocessing_steps": ["Data Cleaning", "Feature Engineering"]
    }
  ],
  "token_usage": 1350,
  "response_time": 5.8
}
```

## Configuration

The H2O AI implementation is configured using environment variables:

- `OPENAI_API_KEY`: The OpenAI API key for the agent
- `OPENAI_MODEL`: The OpenAI model to use for the agent
- `H2OAI_MODEL_TYPE`: The type of predictive model to use (default: "gradient_boosting")
- `H2OAI_FORECAST_HORIZON`: The forecast horizon in days (default: 90)

## Implementation Details

The H2O AI implementation uses the following key features of the H2O AI framework:

1. **Data Preprocessing**: Cleaning and transforming data for analysis
2. **Time Series Analysis**: Analyzing trends and patterns over time
3. **Predictive Modeling**: Building models to forecast future performance
4. **Market Segmentation**: Identifying key market segments and opportunities

For more details on the implementation, see the [H2O AI runner.py](../../../agents/h2oai/runner.py) file.
