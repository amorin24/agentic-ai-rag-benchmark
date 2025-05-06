# External APIs

This document provides detailed documentation for the external API integrations used in the Agentic AI RAG Benchmark project.

## Overview

The project integrates with several external APIs to fetch data for the RAG service:

1. **NewsAPI**: For retrieving news articles about companies and topics
2. **Financial Modeling Prep API**: For retrieving financial data about companies
3. **Wikipedia API**: For retrieving encyclopedia articles about topics

## NewsAPI

### Overview

The NewsAPI integration allows the system to fetch news articles about companies and topics. It is implemented in the [external/news_api.py](../../external/news_api.py) file.

### Configuration

The NewsAPI integration is configured using the following environment variables:

```
NEWS_API_KEY=your_newsapi_key
NEWS_API_MAX_ARTICLES=10
NEWS_API_SORT_BY=relevancy
```

### Functions

#### fetch_news

```python
def fetch_news(topic: str, max_articles: int = 10, days_back: int = 7, language: str = "en", sort_by: str = "relevancy") -> List[Dict]
```

**Description**: Fetches news articles about a specific topic.

**Parameters**:
- `topic` (required): The topic to search for
- `max_articles` (optional): Maximum number of articles to fetch (default: 10)
- `days_back` (optional): Number of days to look back (default: 7)
- `language` (optional): Language of articles (default: "en")
- `sort_by` (optional): Sorting criteria (default: "relevancy")

**Returns**: A list of dictionaries containing news articles with the following fields:
- `title`: Article title
- `description`: Article description
- `content`: Article content
- `url`: Article URL
- `source`: Source name
- `published_at`: Publication date
- `author`: Article author

**Example**:

```python
from external.news_api import fetch_news

# Fetch news articles about Tesla
articles = fetch_news("Tesla", max_articles=5, days_back=3)

# Process articles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']}")
    print(f"Published: {article['published_at']}")
    print(f"Content: {article['content'][:100]}...")
    print("---")
```

### Error Handling

The NewsAPI integration includes comprehensive error handling:

- **API Key Errors**: If the API key is invalid or missing, the function logs an error and returns an empty list
- **Rate Limiting**: If the API rate limit is exceeded, the function logs an error and returns an empty list
- **Network Errors**: If there are network issues, the function logs an error and returns an empty list
- **Parsing Errors**: If there are issues parsing the API response, the function logs an error and returns an empty list

### Logging

The NewsAPI integration logs all API requests and responses to the `logs/external/news_api.log` file.

## Financial Modeling Prep API

### Overview

The Financial Modeling Prep API integration allows the system to fetch financial data about companies. It is implemented in the [external/fmp_api.py](../../external/fmp_api.py) file.

### Configuration

The Financial Modeling Prep API integration is configured using the following environment variables:

```
FMP_API_KEY=your_fmp_api_key
```

### Functions

#### fetch_financials

```python
def fetch_financials(ticker: str, include_profile: bool = True, include_financials: bool = True, include_news: bool = True) -> Dict
```

**Description**: Fetches financial data about a specific company.

**Parameters**:
- `ticker` (required): Company ticker symbol
- `include_profile` (optional): Include company profile (default: True)
- `include_financials` (optional): Include financial statements (default: True)
- `include_news` (optional): Include recent news (default: True)

**Returns**: A dictionary containing financial data with the following fields:
- `profile`: Company profile information
- `financials`: Financial statements
- `news`: Recent news articles
- `ticker`: Company ticker symbol

**Example**:

```python
from external.fmp_api import fetch_financials

# Fetch financial data for Apple
financials = fetch_financials("AAPL")

# Process financial data
print(f"Company: {financials['profile']['companyName']}")
print(f"Industry: {financials['profile']['industry']}")
print(f"Market Cap: {financials['profile']['mktCap']}")
print(f"Revenue: {financials['financials']['income']['revenue']}")
print(f"Net Income: {financials['financials']['income']['netIncome']}")
```

### Error Handling

The Financial Modeling Prep API integration includes comprehensive error handling:

- **API Key Errors**: If the API key is invalid or missing, the function logs an error and returns an empty dictionary
- **Rate Limiting**: If the API rate limit is exceeded, the function logs an error and returns an empty dictionary
- **Network Errors**: If there are network issues, the function logs an error and returns an empty dictionary
- **Parsing Errors**: If there are issues parsing the API response, the function logs an error and returns an empty dictionary

### Logging

The Financial Modeling Prep API integration logs all API requests and responses to the `logs/external/fmp_api.log` file.

## Wikipedia API

### Overview

The Wikipedia API integration allows the system to fetch encyclopedia articles about topics. It is implemented in the [rag_service/ingest.py](../../rag_service/ingest.py) file.

### Configuration

The Wikipedia API integration does not require any API keys, but it can be configured using the following environment variables:

```
WIKIPEDIA_LANGUAGE=en
WIKIPEDIA_MAX_SECTIONS=10
```

### Functions

#### ingest_from_wikipedia

```python
def ingest_from_wikipedia(topic: str, language: str = "en", max_sections: int = 10) -> str
```

**Description**: Fetches and processes Wikipedia articles about a specific topic.

**Parameters**:
- `topic` (required): The topic to search for
- `language` (optional): Language of the Wikipedia article (default: "en")
- `max_sections` (optional): Maximum number of sections to fetch (default: 10)

**Returns**: A string containing the processed Wikipedia article content.

**Example**:

```python
from rag_service.ingest import ingest_from_wikipedia

# Fetch Wikipedia article about Tesla
content = ingest_from_wikipedia("Tesla", language="en", max_sections=5)

# Process content
print(f"Content length: {len(content)}")
print(f"Content preview: {content[:200]}...")
```

### Error Handling

The Wikipedia API integration includes comprehensive error handling:

- **Not Found Errors**: If the topic is not found, the function logs an error and returns an empty string
- **Disambiguation Errors**: If the topic is ambiguous, the function logs a warning and tries to fetch the most relevant article
- **Network Errors**: If there are network issues, the function logs an error and returns an empty string
- **Parsing Errors**: If there are issues parsing the API response, the function logs an error and returns an empty string

### Logging

The Wikipedia API integration logs all API requests and responses to the `logs/rag_service/ingest.log` file.

## Integration with RAG Service

The external API integrations are used by the RAG service to ingest data from various sources. The following functions in the [rag_service/ingest.py](../../rag_service/ingest.py) file use these integrations:

### ingest_news_topic

```python
def ingest_news_topic(topic: str, max_articles: int = 10, days_back: int = 7, language: str = "en", sort_by: str = "relevancy") -> List[str]
```

**Description**: Ingests news articles about a specific topic using the NewsAPI integration.

### ingest_financial_data

```python
def ingest_financial_data(ticker: str, include_profile: bool = True, include_financials: bool = True, include_news: bool = True) -> List[str]
```

**Description**: Ingests financial data about a specific company using the Financial Modeling Prep API integration.

## Implementation Details

For more details on the implementation of these integrations, see the following files:

- [external/news_api.py](../../external/news_api.py): NewsAPI integration
- [external/fmp_api.py](../../external/fmp_api.py): Financial Modeling Prep API integration
- [rag_service/ingest.py](../../rag_service/ingest.py): Wikipedia API integration and integration with the RAG service
