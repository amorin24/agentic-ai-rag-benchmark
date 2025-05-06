# API Documentation

This section provides detailed documentation for the APIs exposed by the Agentic AI RAG Benchmark project.

## Contents

- [RAG Service API](./rag_service.md): Documentation for the RAG service API endpoints
- [Agent Runner API](./agent_runner.md): Documentation for the agent runner API endpoints
- [External APIs](./external_apis.md): Documentation for the external API integrations

## Overview

The Agentic AI RAG Benchmark project exposes several APIs for interacting with the system:

### RAG Service API

The RAG service exposes a FastAPI-based REST API for:

- Ingesting documents and URLs
- Querying the vector store
- Checking the status of the service

For detailed documentation, see the [RAG Service API](./rag_service.md) page.

### Agent Runner API

The agent runner exposes a REST API for:

- Running agent frameworks with specific topics
- Retrieving agent outputs
- Comparing agent performance

For detailed documentation, see the [Agent Runner API](./agent_runner.md) page.

### External APIs

The project integrates with several external APIs:

- NewsAPI for retrieving news articles
- Financial Modeling Prep API for retrieving financial data
- Wikipedia API for retrieving encyclopedia articles

For detailed documentation, see the [External APIs](./external_apis.md) page.

## Authentication

API endpoints that require authentication use API keys passed in the request headers. See the specific API documentation for details on authentication requirements.

## Error Handling

All APIs follow a consistent error handling pattern:

- HTTP status codes indicate the success or failure of the request
- Error responses include a JSON body with error details
- Validation errors include details on the specific validation failures

## Rate Limiting

Some APIs may implement rate limiting to prevent abuse. Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: The maximum number of requests allowed in a time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current time window
- `X-RateLimit-Reset`: The time when the current rate limit window resets

## Next Steps

For detailed documentation on specific APIs, see the corresponding pages.
