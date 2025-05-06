# RAG Service Usage Guide

This document provides detailed instructions for using the RAG service in the Agentic AI RAG Benchmark project.

## Starting the RAG Service

### Using Python

To start the RAG service using Python:

```bash
# Activate your virtual environment
source venv/bin/activate

# Start the RAG service
python -m rag_service.app.main
```

The service will start on the port specified in the `.env` file (default: 8000).

### Using Docker

To start the RAG service using Docker:

```bash
# Start only the RAG service
docker-compose up -d rag_service

# View logs
docker-compose logs -f rag_service
```

## Ingesting Data

The RAG service provides several methods for ingesting data:

### Ingesting Text

To ingest text content:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Text content to ingest",
    "metadata": {
      "source": "manual",
      "author": "John Doe",
      "date": "2023-05-01"
    }
  }'
```

### Ingesting URLs

To ingest content from a URL:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "metadata": {
      "source": "web",
      "author": "Jane Smith",
      "date": "2023-05-01"
    }
  }'
```

### Ingesting News Articles

To ingest news articles about a specific topic:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest/news" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Tesla",
    "max_articles": 10,
    "days_back": 7,
    "language": "en",
    "sort_by": "relevancy"
  }'
```

### Ingesting Financial Data

To ingest financial data about a specific company:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest/financial" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "include_profile": true,
    "include_financials": true,
    "include_news": true
  }'
```

### Ingesting Wikipedia Articles

To ingest Wikipedia articles about a specific topic:

```bash
# Using Python
from rag_service.ingest import ingest_from_wikipedia

# Ingest Wikipedia article
content = ingest_from_wikipedia("Tesla", language="en", max_sections=5)
```

## Querying the RAG Service

To query the RAG service:

```bash
# Using curl
curl -X GET "http://localhost:8000/query?q=latest+company+news&top_k=3&threshold=0.6"
```

The response will include the top-k matching chunks with their similarity scores and metadata.

## Checking Service Status

To check the status of the RAG service:

```bash
# Using curl
curl -X GET "http://localhost:8000/status"
```

The response will include information about the vector store size, last ingest timestamp, and other service metrics.

## Programmatic Usage

### Python Client

You can use the RAG service programmatically using the Python client:

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Ingest text
def ingest_text(content, metadata=None):
    url = f"{base_url}/ingest"
    payload = {
        "content": content,
        "metadata": metadata or {}
    }
    response = requests.post(url, json=payload)
    return response.json()

# Query
def query(q, top_k=5, threshold=0.5):
    url = f"{base_url}/query"
    params = {
        "q": q,
        "top_k": top_k,
        "threshold": threshold
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
content = "This is a sample text to ingest."
metadata = {"source": "example", "author": "John Doe"}

# Ingest content
ingest_result = ingest_text(content, metadata)
print(f"Ingest result: {json.dumps(ingest_result, indent=2)}")

# Query
query_result = query("sample text", top_k=3)
print(f"Query result: {json.dumps(query_result, indent=2)}")
```

## Advanced Usage

### Customizing Chunk Size and Overlap

You can customize the chunk size and overlap when ingesting content:

```bash
# Using curl
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Text content to ingest",
    "chunk_size": 500,
    "chunk_overlap": 100,
    "metadata": {
      "source": "manual"
    }
  }'
```

### Using Different Embedding Models

You can configure the RAG service to use different embedding models by setting the appropriate environment variables in the `.env` file:

```
# OpenAI Embeddings
USE_OPENAI_EMBEDDINGS=True
OPENAI_API_KEY=your_openai_api_key

# Sentence Transformers
USE_OPENAI_EMBEDDINGS=False
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### Batch Ingestion

For large-scale ingestion, you can use the batch ingestion functionality:

```python
from rag_service.ingest import batch_ingest

# List of documents to ingest
documents = [
    {"content": "Document 1 content", "metadata": {"source": "batch", "id": 1}},
    {"content": "Document 2 content", "metadata": {"source": "batch", "id": 2}},
    {"content": "Document 3 content", "metadata": {"source": "batch", "id": 3}}
]

# Batch ingest
results = batch_ingest(documents, chunk_size=1000, chunk_overlap=200)
print(f"Ingested {len(results)} documents")
```

## Troubleshooting

### Service Not Starting

If the RAG service fails to start:

1. Check if the required environment variables are set in the `.env` file
2. Verify that the required dependencies are installed
3. Check the logs for error messages

### Ingestion Failures

If ingestion fails:

1. Check if the content is valid
2. Verify that the metadata is properly formatted
3. Check if the vector store directory exists and is writable
4. Check the logs for error messages

### Query Failures

If queries fail:

1. Check if the vector store has been populated with data
2. Verify that the query parameters are valid
3. Check the logs for error messages

## Next Steps

For more information on the RAG service API, see the [RAG Service API](../api/rag_service.md) documentation.
