# RAG Service

A centralized Retrieval-Augmented Generation (RAG) service built with FastAPI and FAISS.

## Overview

This service provides a common interface for retrieving relevant context from a knowledge base. It uses FAISS for efficient vector similarity search and exposes a REST API for agent frameworks to query.

## Components

- **API**: FastAPI endpoints for querying the RAG service
- **Models**: Vector store and embedding models
- **Utils**: Utility functions for text processing and data management

## API Endpoints

- `POST /query`: Retrieve relevant documents based on a query
- `POST /ingest`: Add new documents to the knowledge base
- `GET /health`: Check service health

## Configuration

Configure the service using environment variables in the root `.env` file.
