# RAG Service Architecture

This document provides a detailed architecture diagram and explanation for the RAG service component of the Agentic AI RAG Benchmark project.

## Overview

The RAG (Retrieval-Augmented Generation) service is a centralized FastAPI service that provides RAG capabilities to the agent frameworks. It is responsible for:

1. Ingesting data from various sources
2. Processing and chunking the data
3. Embedding the chunks using various embedding models
4. Storing the embeddings in a FAISS vector store
5. Retrieving relevant documents based on queries
6. Providing a RESTful API for agent frameworks to interact with

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                           RAG Service                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐                                            │
│  │                     │                                            │
│  │     FastAPI App     │                                            │
│  │                     │                                            │
│  └─────────┬───────────┘                                            │
│            │                                                        │
│            │ routes                                                 │
│            ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                                                             │    │
│  │                      API Endpoints                          │    │
│  │                                                             │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │    │
│  │  │             │    │             │    │             │     │    │
│  │  │   /ingest   │    │   /query    │    │   /status   │     │    │
│  │  │             │    │             │    │             │     │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │    │
│  │        │                  │                  │             │    │
│  └────────┼──────────────────┼──────────────────┼─────────────┘    │
│           │                  │                  │                  │
│           ▼                  ▼                  ▼                  │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐          │
│  │             │      │             │    │             │          │
│  │  ingest.py  │      │ retriever.py│    │  status.py  │          │
│  │             │      │             │    │             │          │
│  └─────────────┘      └─────────────┘    └─────────────┘          │
│        │                    │                                      │
│        │                    │                                      │
│        ▼                    ▼                                      │
│  ┌─────────────┐      ┌─────────────┐                             │
│  │             │      │             │                             │
│  │ embedder.py │      │  FAISS Index│                             │
│  │             │      │             │                             │
│  └─────────────┘      └─────────────┘                             │
│        │                    │                                      │
│        │                    │                                      │
│        ▼                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │                      Data Sources                           │   │
│  │                                                             │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │   │
│  │  │             │    │             │    │             │     │   │
│  │  │  Wikipedia  │    │   NewsAPI   │    │Financial API│     │   │
│  │  │             │    │             │    │             │     │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘     │   │
│  │                                                             │   │
│  │  ┌─────────────┐    ┌─────────────┐                        │   │
│  │  │             │    │             │                        │   │
│  │  │    URLs     │    │    Text     │                        │   │
│  │  │             │    │             │                        │   │
│  │  └─────────────┘    └─────────────┘                        │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### FastAPI App

The FastAPI app is the main entry point for the RAG service. It defines the API endpoints and routes requests to the appropriate handlers.

### API Endpoints

#### /ingest (POST)

The `/ingest` endpoint accepts a POST request with either text or a URL, processes and embeds it, then adds it to the FAISS index. It supports the following parameters:

- `text`: The text content to ingest
- `url`: The URL to crawl and ingest
- `chunk_size`: The size of the chunks to create
- `chunk_overlap`: The overlap between chunks

#### /query (GET)

The `/query` endpoint accepts a GET request with a query parameter. It runs the query through the retriever and returns the top-k matching chunks in JSON format. It supports the following parameters:

- `query`: The query to search for
- `top_k`: The number of results to return (default: 5)

#### /status (GET)

The `/status` endpoint is a simple healthcheck that returns a JSON object with the vector store size and last ingest timestamp.

### ingest.py

The `ingest.py` module is responsible for ingesting data from various sources, processing it, and preparing it for embedding. It includes the following functions:

- `ingest_from_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]`: Ingests text content
- `ingest_from_url(url: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]`: Ingests content from a URL
- `ingest_from_wikipedia(query: str, max_articles: int = 5, language: str = "en") -> List[Dict]`: Ingests content from Wikipedia
- `ingest_news_topic(topic: str, max_articles: int = 10) -> List[str]`: Ingests news articles about a topic
- `ingest_financial_data(ticker: str) -> str`: Ingests financial data for a company

### embedder.py

The `embedder.py` module is responsible for converting text chunks into vector embeddings. It supports both OpenAI embeddings and Hugging Face sentence transformers. It includes the following functions:

- `embed_text(text: str) -> List[float]`: Embeds a single text chunk
- `embed_texts(texts: List[str]) -> List[List[float]]`: Embeds multiple text chunks
- `get_embedding_model() -> Any`: Returns the current embedding model
- `set_embedding_model(model_name: str) -> None`: Sets the embedding model to use

### retriever.py

The `retriever.py` module is responsible for storing and searching vectorized document chunks using FAISS. It includes the following functions:

- `add_documents(documents: List[Dict]) -> None`: Adds documents to the FAISS index
- `search(query: str, top_k: int = 5) -> List[Dict]`: Searches the FAISS index for similar documents
- `load_index() -> Any`: Loads the FAISS index from disk
- `save_index() -> None`: Saves the FAISS index to disk

### Data Sources

The RAG service supports ingesting data from various sources:

- **Wikipedia**: Using the Wikipedia API
- **NewsAPI**: Using the NewsAPI for news articles
- **Financial API**: Using the Financial Modeling Prep API for financial data
- **URLs**: Crawling and extracting content from web pages
- **Text**: Directly ingesting text content

## Data Flow

1. **Ingestion**:
   - Data is ingested from various sources using the `ingest.py` module
   - The data is processed, cleaned, and chunked
   - The chunks are embedded using the `embedder.py` module
   - The embeddings are stored in the FAISS index using the `retriever.py` module

2. **Querying**:
   - A query is received through the `/query` endpoint
   - The query is embedded using the `embedder.py` module
   - The embedded query is used to search the FAISS index using the `retriever.py` module
   - The top-k matching chunks are returned in JSON format

3. **Status**:
   - A status request is received through the `/status` endpoint
   - The vector store size and last ingest timestamp are retrieved
   - The information is returned in JSON format

## Configuration

The RAG service is configured using environment variables:

- `RAG_SERVICE_HOST`: The host to bind the FastAPI app to
- `RAG_SERVICE_PORT`: The port to bind the FastAPI app to
- `VECTOR_DB_PATH`: The path to store the FAISS index
- `OPENAI_API_KEY`: The OpenAI API key for embeddings
- `OPENAI_MODEL`: The OpenAI model to use for embeddings
- `WIKIPEDIA_MAX_ARTICLES`: The maximum number of Wikipedia articles to retrieve
- `WIKIPEDIA_LANGUAGE`: The language for Wikipedia articles
- `NEWS_API_KEY`: The NewsAPI key
- `NEWS_API_MAX_ARTICLES`: The maximum number of news articles to retrieve
- `NEWS_API_SORT_BY`: The sorting method for news articles
- `FMP_API_KEY`: The Financial Modeling Prep API key

## Deployment

The RAG service can be deployed using Docker:

```bash
docker-compose up rag_service
```

For more details on deployment, see the [Docker Setup](../setup/docker_setup.md) documentation.
