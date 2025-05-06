# Processed Data Directory

This directory contains processed documents ready for embedding and retrieval by the RAG service. The documents are stored as JSON files with the following naming convention:

## File Naming Conventions

- **News Articles**: `news_{hash}_{timestamp}.json`
- **Financial Data**: `financial_{ticker}_{timestamp}.json`
- **Wikipedia Articles**: `wiki_{hash}_{timestamp}.json`
- **URL Content**: `url_{hash}_{timestamp}.json`
- **Text Content**: `text_{hash}_{timestamp}.json`

## File Structure

Each JSON file contains:

```json
{
  "id": "unique_document_id",
  "chunks": [
    {
      "text": "chunk_text_content",
      "chunk_id": 0
    },
    ...
  ],
  "metadata": {
    "source": "source_type",
    "title": "document_title",
    "url": "source_url",
    "type": "document_type",
    ...
  }
}
```

## Document Types

### News Articles
News articles ingested from NewsAPI using `ingest_news_topic()` function.

**Metadata includes**:
- source: "newsapi_external"
- title: Article title
- url: Article URL
- author: Article author
- published_at: Publication date
- source_name: News source name
- type: "news"
- topic: Search topic

### Financial Data
Financial information ingested from Financial Modeling Prep API using `ingest_financial_data()` function.

**Metadata includes**:
- source: "financial_modeling_prep_external"
- ticker: Stock ticker symbol
- company_name: Company name
- sector: Company sector
- industry: Company industry
- type: "financial"

### Wikipedia Articles
Wikipedia articles ingested using `ingest_from_wikipedia()` function.

**Metadata includes**:
- source: "wikipedia"
- title: Article title
- url: Wikipedia URL
- type: "wiki"
- query: Search query

### URL Content
Web content ingested from URLs using `ingest_from_url()` function.

**Metadata includes**:
- source: "url"
- url: Source URL
- title: Page title
- type: "web"

### Text Content
Raw text ingested using `ingest_from_text()` function.

**Metadata includes**:
- source: "text"
- type: "text"
- title: Optional title

## Usage

These processed documents are used by the RAG service for embedding and retrieval. The documents are chunked and ready to be converted into vector embeddings for similarity search.

To list all processed documents:

```python
from rag_service.ingest import list_processed_documents

documents = list_processed_documents()
for doc in documents:
    print(f"- {doc['id']}: {doc['metadata'].get('title', 'Untitled')} ({doc['chunks']} chunks)")
```

To load a specific document:

```python
from rag_service.ingest import load_processed_document

document = load_processed_document("document_id")
```
