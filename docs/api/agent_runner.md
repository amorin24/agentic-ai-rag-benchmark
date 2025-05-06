# Agent Runner API

This document provides detailed documentation for the Agent Runner API endpoints.

## Base URL

The Agent Runner API is accessible at:

```
http://{AGENT_RUNNER_HOST}:{AGENT_RUNNER_PORT}
```

By default, this is `http://localhost:5000`.

## Authentication

The Agent Runner API does not require authentication for local development. For production deployments, authentication can be configured using API keys or other authentication mechanisms.

## Endpoints

### Run Agent

**Endpoint**: `/run`

**Method**: `POST`

**Description**: Runs an agent framework with a specific topic and returns the results.

**Request Body**:

```json
{
  "topic": "Tesla",
  "agent_framework": "crewai",
  "max_tokens": 4000,
  "timeout": 300
}
```

**Parameters**:

- `topic` (required): The topic or company to research
- `agent_framework` (optional): The agent framework to use (default: value from environment variable)
- `max_tokens` (optional): Maximum number of tokens to generate (default: 4000)
- `timeout` (optional): Maximum time in seconds to wait for the agent to complete (default: 300)

**Response**:

```json
{
  "agent_name": "crewai",
  "final_output": "Comprehensive company report...",
  "steps": [
    {
      "step": "Research Planning",
      "output": "Planning details..."
    },
    {
      "step": "Information Gathering",
      "output": "Gathered information..."
    },
    {
      "step": "Analysis",
      "output": "Analysis results..."
    },
    {
      "step": "Report Generation",
      "output": "Final report..."
    }
  ],
  "token_usage": 1234,
  "response_time": 5.67
}
```

**Status Codes**:

- `200 OK`: Agent ran successfully
- `400 Bad Request`: Invalid request parameters
- `408 Request Timeout`: Agent execution timed out
- `500 Internal Server Error`: Server error during agent execution

### List Frameworks

**Endpoint**: `/frameworks`

**Method**: `GET`

**Description**: Returns a list of available agent frameworks.

**Response**:

```json
{
  "frameworks": [
    {
      "name": "crewai",
      "description": "A framework for creating multi-agent systems with specialized roles"
    },
    {
      "name": "autogen",
      "description": "A framework for building conversational agents with LLMs"
    },
    {
      "name": "langgraph",
      "description": "A framework for building graph-based workflows with LLMs"
    },
    {
      "name": "googleadk",
      "description": "Google's Agent Development Kit for building AI agents"
    },
    {
      "name": "squidai",
      "description": "A framework for building tool-using agents"
    },
    {
      "name": "lettaai",
      "description": "A framework for building memory-augmented agents"
    }
  ]
}
```

**Status Codes**:

- `200 OK`: Frameworks retrieved successfully
- `500 Internal Server Error`: Server error during retrieval

### Compare Frameworks

**Endpoint**: `/compare`

**Method**: `POST`

**Description**: Runs multiple agent frameworks with the same topic and returns the results for comparison.

**Request Body**:

```json
{
  "topic": "Tesla",
  "frameworks": ["crewai", "autogen", "langgraph"],
  "max_tokens": 4000,
  "timeout": 300
}
```

**Parameters**:

- `topic` (required): The topic or company to research
- `frameworks` (optional): Array of agent frameworks to use (default: all available frameworks)
- `max_tokens` (optional): Maximum number of tokens to generate (default: 4000)
- `timeout` (optional): Maximum time in seconds to wait for each agent to complete (default: 300)

**Response**:

```json
{
  "topic": "Tesla",
  "results": [
    {
      "agent_name": "crewai",
      "final_output": "Comprehensive company report...",
      "steps": [...],
      "token_usage": 1234,
      "response_time": 5.67
    },
    {
      "agent_name": "autogen",
      "final_output": "Comprehensive company report...",
      "steps": [...],
      "token_usage": 1456,
      "response_time": 6.12
    },
    {
      "agent_name": "langgraph",
      "final_output": "Comprehensive company report...",
      "steps": [...],
      "token_usage": 1345,
      "response_time": 5.89
    }
  ],
  "metrics": {
    "factual_overlap": {
      "crewai": 0.85,
      "autogen": 0.82,
      "langgraph": 0.88
    },
    "reasoning_clarity": {
      "crewai": 0.78,
      "autogen": 0.81,
      "langgraph": 0.76
    }
  }
}
```

**Status Codes**:

- `200 OK`: Comparison completed successfully
- `400 Bad Request`: Invalid request parameters
- `408 Request Timeout`: One or more agent executions timed out
- `500 Internal Server Error`: Server error during comparison

### Get Status

**Endpoint**: `/status`

**Method**: `GET`

**Description**: Returns the status of the Agent Runner service.

**Response**:

```json
{
  "status": "healthy",
  "frameworks_available": 6,
  "current_framework": "crewai",
  "uptime_seconds": 3600
}
```

**Status Codes**:

- `200 OK`: Service is healthy
- `500 Internal Server Error`: Service is unhealthy

## Error Responses

All endpoints return a consistent error response format:

```json
{
  "status": "error",
  "message": "Error message",
  "error_code": "ERROR_CODE",
  "details": {
    "param": "value",
    "additional_info": "More details about the error"
  }
}
```

## Rate Limiting

The Agent Runner API implements rate limiting to prevent abuse. Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: The maximum number of requests allowed in a time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current time window
- `X-RateLimit-Reset`: The time when the current rate limit window resets

## Implementation Details

The Agent Runner API is implemented using Flask. The implementation can be found in the [agents/runner.py](../../agents/runner.py) file.

For more details on the agent frameworks, see the [Agent Frameworks Architecture](../architecture/frameworks/README.md) documentation.
