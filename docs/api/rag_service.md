# RAG Service API

This document provides detailed documentation for the RAG service API endpoints.

## Base URL

The RAG service API is accessible at:

```
http://{RAG_SERVICE_HOST}:{RAG_SERVICE_PORT}
```

By default, this is `http://localhost:8000`.

## Authentication

The RAG service API does not require authentication for local development. For production deployments, authentication can be configured using API keys or other authentication mechanisms.

## Endpoints

### Ingest

**Endpoint**: `/ingest`

**Method**: `POST`

**Description**: Ingests text or a URL, processes and embeds it, then adds it to the FAISS index.

**Request Body**:

```json
{
  "content": "Text content to ingest",
  "url": "https://example.com/article",
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "metadata": {
    "source": "manual",
    "author": "John Doe",
    "date": "2023-05-01"
  }
}
```

**Parameters**:

- `content` (optional): Text content to ingest
- `url` (optional): URL to crawl and ingest
- `chunk_size` (optional): Size of text chunks for embedding (default: 1000)
- `chunk_overlap` (optional): Overlap between chunks (default: 200)
- `metadata` (optional): Additional metadata to store with the document

**Note**: At least one of `content` or `url` must be provided.

**Response**:

```json
{
  "status": "success",
  "message": "Content ingested successfully",
  "document_id": "doc_123456",
  "chunks": 5,
  "vector_store_size": 1250
}
```

**Status Codes**:

- `200 OK`: Content ingested successfully
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server error during ingestion

### Query

**Endpoint**: `/query`

**Method**: `GET`

**Description**: Runs a query through the retriever and returns the top-k matching chunks.

**Query Parameters**:

- `q` (required): Query string
- `top_k` (optional): Number of results to return (default: 5)
- `threshold` (optional): Minimum similarity score threshold (default: 0.5)

**Example**:

```
GET /query?q=latest+company+news&top_k=3&threshold=0.6
```

**Response**:

```json
{
  "query": "latest company news",
  "results": [
    {
      "content": "The company announced a new product line yesterday...",
      "metadata": {
        "source": "https://example.com/news/article1",
        "author": "Jane Smith",
        "date": "2023-05-01"
      },
      "similarity": 0.89
    },
    {
      "content": "In recent news, the company's quarterly earnings exceeded expectations...",
      "metadata": {
        "source": "https://example.com/news/article2",
        "author": "John Doe",
        "date": "2023-04-28"
      },
      "similarity": 0.78
    },
    {
      "content": "The company's CEO announced a new strategic direction...",
      "metadata": {
        "source": "https://example.com/news/article3",
        "author": "Alice Johnson",
        "date": "2023-04-25"
      },
      "similarity": 0.72
    }
  ],
  "total_results": 3,
  "query_time_ms": 45
}
```

**Status Codes**:

- `200 OK`: Query executed successfully
- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Server error during query execution

### Status

**Endpoint**: `/status`

**Method**: `GET`

**Description**: Returns the status of the RAG service, including vector store size and last ingest timestamp.

**Response**:

```json
{
  "status": "healthy",
  "vector_store_size": 1250,
  "last_ingest_timestamp": "2023-05-01T14:30:45Z",
  "embedding_model": "sentence-transformers/all-mpnet-base-v2",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

**Status Codes**:

- `200 OK`: Service is healthy
- `500 Internal Server Error`: Service is unhealthy

## Additional Endpoints

### Ingest News Topic

**Endpoint**: `/ingest/news`

**Method**: `POST`

**Description**: Ingests news articles about a specific topic using the NewsAPI.

**Request Body**:

```json
{
  "topic": "Tesla",
  "max_articles": 10,
  "days_back": 7,
  "language": "en",
  "sort_by": "relevancy"
}
```

**Parameters**:

- `topic` (required): Topic to search for
- `max_articles` (optional): Maximum number of articles to ingest (default: 10)
- `days_back` (optional): Number of days to look back (default: 7)
- `language` (optional): Language of articles (default: "en")
- `sort_by` (optional): Sorting criteria (default: "relevancy")

**Response**:

```json
{
  "status": "success",
  "message": "News articles ingested successfully",
  "articles_ingested": 8,
  "vector_store_size": 1350
}
```

**Status Codes**:

- `200 OK`: News articles ingested successfully
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server error during ingestion

### Ingest Financial Data

**Endpoint**: `/ingest/financial`

**Method**: `POST`

**Description**: Ingests financial data about a specific company using the Financial Modeling Prep API.

**Request Body**:

```json
{
  "ticker": "AAPL",
  "include_profile": true,
  "include_financials": true,
  "include_news": true
}
```

**Parameters**:

- `ticker` (required): Company ticker symbol
- `include_profile` (optional): Include company profile (default: true)
- `include_financials` (optional): Include financial statements (default: true)
- `include_news` (optional): Include recent news (default: true)

**Response**:

```json
{
  "status": "success",
  "message": "Financial data ingested successfully",
  "data_points_ingested": 15,
  "vector_store_size": 1400
}
```

**Status Codes**:

- `200 OK`: Financial data ingested successfully
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server error during ingestion

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

The RAG service implements rate limiting to prevent abuse. Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: The maximum number of requests allowed in a time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current time window
- `X-RateLimit-Reset`: The time when the current rate limit window resets

## Implementation Details

The RAG service API is implemented using FastAPI. The implementation can be found in the [rag_service/app/api.py](../../rag_service/app/api.py) file.

For more details on the implementation, see the [RAG Service Architecture](../architecture/rag_service.md) documentation.
