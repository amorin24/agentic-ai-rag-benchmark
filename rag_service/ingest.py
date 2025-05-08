"""
Ingest module for the RAG service.

This module provides functionality to upload or crawl public datasets,
clean and process the text, and prepare documents for embedding.
"""

import os
import re
import json
import time
import logging
import requests
from typing import List, Dict, Any, Optional, Union, Callable
from pathlib import Path
from bs4 import BeautifulSoup
import wikipedia
from datetime import datetime, timedelta
from dotenv import load_dotenv

from external.news_api import fetch_news
from external.fmp_api import fetch_financials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

PROCESSED_DIR = Path(os.getenv('PROCESSED_DOCS_DIR', 'data/processed'))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
FMP_API_KEY = os.getenv('FMP_API_KEY', '')  # Financial Modeling Prep API key
WIKIPEDIA_MAX_ARTICLES = int(os.getenv('WIKIPEDIA_MAX_ARTICLES', '5'))
WIKIPEDIA_LANGUAGE = os.getenv('WIKIPEDIA_LANGUAGE', 'en')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')  # NewsAPI key
NEWS_API_MAX_ARTICLES = int(os.getenv('NEWS_API_MAX_ARTICLES', '10'))
NEWS_API_SORT_BY = os.getenv('NEWS_API_SORT_BY', 'relevancy')  # Options: relevancy, popularity, publishedAt

wikipedia.set_lang(WIKIPEDIA_LANGUAGE)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    text = re.sub(r'\n+', '\n', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to split into chunks
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        if end < len(text):
            last_sentence_end = max(
                text.rfind('. ', start, end),
                text.rfind('? ', start, end),
                text.rfind('! ', start, end)
            )
            
            if last_sentence_end > start:
                end = last_sentence_end + 1  # Include the period
            else:
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
        
        chunks.append(text[start:end].strip())
        start = end - chunk_overlap if end - chunk_overlap > start else end
    
    return chunks


def save_processed_document(doc_id: str, chunks: List[str], metadata: Dict[str, Any]) -> str:
    """
    Save processed document chunks to disk.
    
    Args:
        doc_id: Unique identifier for the document
        chunks: List of text chunks
        metadata: Document metadata
        
    Returns:
        Path to the saved document
    """
    document = {
        "id": doc_id,
        "chunks": chunks,
        "metadata": metadata,
        "processed_at": time.time()
    }
    
    file_path = PROCESSED_DIR / f"{doc_id}.json"
    with open(file_path, 'w') as f:
        json.dump(document, f, indent=2)
    
    logger.info(f"Saved processed document to {file_path}")
    return str(file_path)


def process_document(text: str, doc_id: str, metadata: Dict[str, Any]) -> str:
    """
    Process a document: clean text, chunk it, and save it.
    
    Args:
        text: Raw text to process
        doc_id: Document identifier
        metadata: Document metadata
        
    Returns:
        Path to the saved document
    """
    text = clean_text(text)
    chunks = chunk_text(text)
    return save_processed_document(doc_id, chunks, metadata)


def extract_text_from_url(url: str) -> Dict[str, Any]:
    """
    Extract text content from a URL.
    
    Args:
        url: URL to extract text from
        
    Returns:
        Dictionary with text content and metadata
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "Untitled"
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        
        text = clean_text(text)
        
        return {
            "text": text,
            "metadata": {
                "source": url,
                "title": title,
                "type": "web"
            }
        }
    except Exception as e:
        logger.error(f"Failed to extract text from URL {url}: {str(e)}")
        raise


def ingest_from_url(url: str) -> str:
    """
    Ingest content from a URL.
    
    Args:
        url: URL to ingest
        
    Returns:
        Path to the processed document
    """
    result = extract_text_from_url(url)
    
    doc_id = f"url_{hash(url)}_{int(time.time())}"
    
    return process_document(result["text"], doc_id, result["metadata"])


def ingest_from_text(text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Ingest content from raw text.
    
    Args:
        text: Text to ingest
        metadata: Optional metadata
        
    Returns:
        Path to the processed document
    """
    if metadata is None:
        metadata = {"source": "direct_input", "type": "text"}
    
    doc_id = f"text_{hash(text[:100])}_{int(time.time())}"
    
    return process_document(text, doc_id, metadata)


def process_wikipedia_article(title: str, original_query: Optional[str] = None) -> Optional[str]:
    """
    Process a single Wikipedia article.
    
    Args:
        title: Article title
        original_query: Original query if this is an alternative article
        
    Returns:
        Path to the processed document or None if processing failed
    """
    try:
        logger.info(f"Retrieving Wikipedia article: {title}")
        page = wikipedia.page(title)
        
        text = page.content
        
        doc_id = f"wiki_{hash(title)}_{int(time.time())}"
        
        metadata = {
            "source": "wikipedia",
            "title": title,
            "url": page.url,
            "type": "wikipedia",
            "language": WIKIPEDIA_LANGUAGE
        }
        
        if original_query:
            metadata["original_query"] = original_query
        
        file_path = process_document(text, doc_id, metadata)
        logger.info(f"Successfully processed Wikipedia article: {title}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to process Wikipedia article {title}: {str(e)}")
        return None


def ingest_from_wikipedia(topic: str, max_articles: int = WIKIPEDIA_MAX_ARTICLES) -> List[str]:
    """
    Ingest content from Wikipedia.
    
    Args:
        topic: Topic to search for
        max_articles: Maximum number of articles to ingest (defaults to WIKIPEDIA_MAX_ARTICLES from env)
        
    Returns:
        List of paths to processed documents
    """
    try:
        logger.info(f"Searching Wikipedia for '{topic}' (max articles: {max_articles})")
        search_results = wikipedia.search(topic, results=max_articles)
        
        processed_docs = []
        for title in search_results:
            try:
                file_path = process_wikipedia_article(title)
                if file_path:
                    processed_docs.append(file_path)
                    
            except wikipedia.exceptions.DisambiguationError as e:
                logger.warning(f"Disambiguation error for '{title}': {str(e)}")
                if e.options:
                    alt_title = e.options[0]
                    file_path = process_wikipedia_article(alt_title, title)
                    if file_path:
                        processed_docs.append(file_path)
                continue
        
        if not processed_docs:
            logger.warning(f"No Wikipedia articles were successfully processed for topic: {topic}")
        else:
            logger.info(f"Successfully processed {len(processed_docs)} Wikipedia articles for topic: {topic}")
            
        return processed_docs
    
    except Exception as e:
        logger.error(f"Failed to search Wikipedia for {topic}: {str(e)}")
        raise


def ingest_from_file(file_path: str) -> str:
    """
    Ingest content from a local file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Path to the processed document
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        doc_id = f"file_{hash(file_name)}_{int(time.time())}"
        
        metadata = {
            "source": "file",
            "file_name": file_name,
            "file_type": file_ext,
            "type": "file"
        }
        
        return process_document(text, doc_id, metadata)
    
    except Exception as e:
        logger.error(f"Failed to ingest file {file_path}: {str(e)}")
        raise


def load_processed_document(doc_path: str) -> Dict[str, Any]:
    """
    Load a processed document from disk.
    
    Args:
        doc_path: Path to the document
        
    Returns:
        Document object
    """
    with open(doc_path, 'r') as f:
        return json.load(f)


def list_processed_documents() -> List[Dict[str, Any]]:
    """
    List all processed documents.
    
    Returns:
        List of document metadata
    """
    documents = []
    
    for file_path in PROCESSED_DIR.glob('*.json'):
        try:
            with open(file_path, 'r') as f:
                doc = json.load(f)
                documents.append({
                    "id": doc["id"],
                    "path": str(file_path),
                    "metadata": doc["metadata"],
                    "processed_at": doc["processed_at"],
                    "chunks": len(doc["chunks"])
                })
        except Exception as e:
            logger.error(f"Failed to load document {file_path}: {str(e)}")
    
    return documents


def process_news_article(article: Dict[str, Any], topic: str, source_name: str = "newsapi") -> Optional[str]:
    """
    Process a single news article.
    
    Args:
        article: Article data
        topic: Search topic
        source_name: Source name for metadata
        
    Returns:
        Path to the processed document or None if processing failed
    """
    try:
        title = article.get("title", "Untitled")
        source = article.get("source", "Unknown Source")
        author = article.get("author", "Unknown Author")
        published_at = article.get("published_at", "")
        url = article.get("url", "")
        description = article.get("description", "")
        content = article.get("content", "")
        
        full_text = f"Title: {title}\n\n"
        full_text += f"Source: {source}\n"
        full_text += f"Author: {author}\n"
        full_text += f"Published: {published_at}\n\n"
        full_text += f"Description: {description}\n\n"
        full_text += f"Content:\n{content}"
        
        doc_id = f"news_{hash(title)}_{int(time.time())}"
        
        metadata = {
            "source": f"{source_name}",
            "title": title,
            "url": url,
            "author": author,
            "published_at": published_at,
            "source_name": source,
            "type": "news",
            "topic": topic
        }
        
        file_path = process_document(full_text, doc_id, metadata)
        logger.info(f"Successfully processed news article: {title}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to process news article: {str(e)}")
        return None


def ingest_news_topic(topic: str, max_articles: int = NEWS_API_MAX_ARTICLES) -> List[str]:
    """
    Ingest news articles about a topic using the external news_api module.
    
    Args:
        topic: Topic to search for
        max_articles: Maximum number of articles to ingest
        
    Returns:
        List of paths to processed documents
    """
    logger.info(f"Ingesting news articles about '{topic}' using external news_api module")
    
    try:
        articles = fetch_news(topic, max_articles=max_articles)
        
        if not articles:
            logger.warning(f"No news articles found for topic: {topic}")
            return []
        
        logger.info(f"Found {len(articles)} news articles about '{topic}'")
        
        processed_docs = []
        for article in articles:
            file_path = process_news_article(article, topic, "newsapi_external")
            if file_path:
                processed_docs.append(file_path)
        
        if not processed_docs:
            logger.warning(f"No news articles were successfully processed for topic: {topic}")
        else:
            logger.info(f"Successfully processed {len(processed_docs)} news articles for topic: {topic}")
            
        return processed_docs
        
    except Exception as e:
        logger.error(f"Failed to ingest news for topic '{topic}': {str(e)}")
        return []


def ingest_from_news_api(topic: str, max_articles: int = NEWS_API_MAX_ARTICLES, 
                      sort_by: str = NEWS_API_SORT_BY, days_back: int = 30) -> List[str]:
    """
    Ingest news articles from NewsAPI.
    
    Args:
        topic: Topic to search for
        max_articles: Maximum number of articles to ingest (defaults to NEWS_API_MAX_ARTICLES from env)
        sort_by: Sorting method (relevancy, popularity, publishedAt)
        days_back: Number of days to look back for articles
        
    Returns:
        List of paths to processed documents
    """
    if not NEWS_API_KEY:
        raise ValueError("NewsAPI key not found in environment variables")
    
    try:
        logger.info(f"Searching NewsAPI for '{topic}' (max articles: {max_articles}, sort: {sort_by})")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "apiKey": NEWS_API_KEY,
            "sortBy": sort_by,
            "language": "en",
            "from": from_date,
            "to": to_date,
            "pageSize": max_articles
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") != "ok":
            logger.error(f"NewsAPI returned error: {data.get('message', 'Unknown error')}")
            raise ValueError(f"NewsAPI error: {data.get('message', 'Unknown error')}")
        
        articles = data.get("articles", [])
        logger.info(f"Found {len(articles)} articles about '{topic}'")
        
        processed_docs = []
        for article in articles:
            processed_article = {
                "title": article.get("title", "Untitled"),
                "source": article.get("source", {}).get("name", "Unknown Source"),
                "author": article.get("author", "Unknown Author"),
                "published_at": article.get("publishedAt", ""),
                "url": article.get("url", ""),
                "description": article.get("description", ""),
                "content": article.get("content", "")
            }
            
            if not processed_article["content"] or "..." in processed_article["content"] or "[+" in processed_article["content"]:
                logger.info(f"Content truncated or empty, fetching from URL: {processed_article['url']}")
                try:
                    article_data = extract_text_from_url(processed_article["url"])
                    processed_article["content"] = article_data.get("text", "")
                except Exception as e:
                    logger.warning(f"Failed to extract text from URL {processed_article['url']}: {str(e)}")
                    processed_article["content"] = processed_article["description"]
            
            file_path = process_news_article(processed_article, topic, "newsapi")
            if file_path:
                processed_docs.append(file_path)
        
        if not processed_docs:
            logger.warning(f"No news articles were successfully processed for topic: {topic}")
        else:
            logger.info(f"Successfully processed {len(processed_docs)} news articles for topic: {topic}")
            
        return processed_docs
    
    except Exception as e:
        logger.error(f"Failed to search NewsAPI for {topic}: {str(e)}")
        raise


def process_financial_data(data: Dict[str, Any], ticker: str, source_name: str) -> str:
    """
    Process financial data into a document.
    
    Args:
        data: Financial data
        ticker: Stock ticker symbol
        source_name: Source name for metadata
        
    Returns:
        Path to the processed document
    """
    try:
        company_profile = data.get("company_profile", {})
        company_name = company_profile.get("companyName", ticker)
        description = company_profile.get("description", "")
        sector = company_profile.get("sector", "")
        industry = company_profile.get("industry", "")
        
        income_statements = data.get("income_statement", [])
        balance_sheets = data.get("balance_sheet", [])
        cash_flows = data.get("cash_flow", [])
        key_metrics = data.get("key_metrics", [])
        stock_price = data.get("stock_price", {})
        news = data.get("news", [])
        
        text = f"Company: {company_name}\n"
        text += f"Symbol: {ticker}\n"
        text += f"Sector: {sector}\n"
        text += f"Industry: {industry}\n\n"
        text += f"Description: {description}\n\n"
        
        if stock_price:
            text += "Current Stock Information:\n"
            text += f"Price: ${stock_price.get('price', 'N/A')}\n"
            text += f"Change: {stock_price.get('change', 'N/A')} ({stock_price.get('changesPercentage', 'N/A')}%)\n"
            text += f"Market Cap: ${stock_price.get('marketCap', 'N/A')}\n"
            text += f"Volume: {stock_price.get('volume', 'N/A')}\n\n"
        
        if income_statements:
            text += "Income Statement Data:\n"
            for i, statement in enumerate(income_statements[:2]):
                year = statement.get("date", "N/A")
                text += f"Year {i+1} ({year}):\n"
                text += f"  Revenue: ${statement.get('revenue', 0):,}\n"
                text += f"  Gross Profit: ${statement.get('grossProfit', 0):,}\n"
                text += f"  Operating Income: ${statement.get('operatingIncome', 0):,}\n"
                text += f"  Net Income: ${statement.get('netIncome', 0):,}\n"
                text += f"  EPS: ${statement.get('eps', 0)}\n\n"
        
        if balance_sheets:
            text += "Balance Sheet Data:\n"
            for i, sheet in enumerate(balance_sheets[:2]):
                year = sheet.get("date", "N/A")
                text += f"Year {i+1} ({year}):\n"
                text += f"  Total Assets: ${sheet.get('totalAssets', 0):,}\n"
                text += f"  Total Liabilities: ${sheet.get('totalLiabilities', 0):,}\n"
                text += f"  Total Equity: ${sheet.get('totalStockholdersEquity', 0):,}\n\n"
        
        if key_metrics:
            text += "Key Financial Metrics:\n"
            for i, metrics in enumerate(key_metrics[:2]):
                year = metrics.get("date", "N/A")
                text += f"Year {i+1} ({year}):\n"
                text += f"  ROE: {metrics.get('roe', 'N/A')}\n"
                text += f"  ROA: {metrics.get('roa', 'N/A')}\n"
                text += f"  Debt to Equity: {metrics.get('debtToEquity', 'N/A')}\n"
                text += f"  Current Ratio: {metrics.get('currentRatio', 'N/A')}\n\n"
        
        if news:
            text += "Recent News:\n"
            for i, article in enumerate(news[:3]):
                text += f"News {i+1}: {article.get('title', 'N/A')}\n"
                text += f"Date: {article.get('publishedDate', 'N/A')}\n"
                text += f"Source: {article.get('site', 'N/A')}\n"
                text += f"Summary: {article.get('text', 'N/A')[:200]}...\n\n"
        
        doc_id = f"financial_{ticker}_{int(time.time())}"
        
        metadata = {
            "source": source_name,
            "ticker": ticker,
            "company_name": company_name,
            "sector": sector,
            "industry": industry,
            "type": "financial"
        }
        
        return process_document(text, doc_id, metadata)
        
    except Exception as e:
        logger.error(f"Failed to process financial data for {ticker}: {str(e)}")
        raise


def ingest_financial_data(ticker: str) -> str:
    """
    Ingest financial data for a company using the external fmp_api module.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        Path to the processed document
    """
    logger.info(f"Ingesting financial data for '{ticker}' using external fmp_api module")
    
    try:
        financial_data = fetch_financials(ticker)
        
        if not financial_data:
            logger.warning(f"No financial data found for ticker: {ticker}")
            return ""
        
        file_path = process_financial_data(financial_data, ticker, "financial_modeling_prep_external")
        logger.info(f"Successfully processed financial data for {ticker}")
        
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to ingest financial data for {ticker}: {str(e)}")
        return ""


def ingest_from_financial_api(symbol: str) -> str:
    """
    Ingest financial data from Financial Modeling Prep API.
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Path to the processed document
    """
    if not FMP_API_KEY:
        raise ValueError("Financial Modeling Prep API key not found in environment variables")
    
    try:
        profile_url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"
        profile_response = requests.get(profile_url)
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        if not profile_data:
            raise ValueError(f"No data found for symbol {symbol}")
        
        financials_url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=4&apikey={FMP_API_KEY}"
        financials_response = requests.get(financials_url)
        financials_response.raise_for_status()
        financials_data = financials_response.json()
        
        financial_data = {
            "company_profile": profile_data[0] if profile_data else {},
            "income_statement": financials_data
        }
        
        return process_financial_data(financial_data, symbol, "financial_modeling_prep")
    
    except Exception as e:
        logger.error(f"Failed to ingest financial data for {symbol}: {str(e)}")
        raise


if __name__ == "__main__":
    print("Ingesting from Wikipedia...")
    wiki_docs = ingest_from_wikipedia("Artificial Intelligence", max_articles=2)
    print(f"Processed {len(wiki_docs)} Wikipedia articles")
    
    print("\nIngesting from NewsAPI...")
    news_docs = ingest_news_topic("Artificial Intelligence", max_articles=2)
    print(f"Processed {len(news_docs)} news articles")
    
    print("\nIngesting financial data...")
    financial_doc = ingest_financial_data("AAPL")
    print(f"Processed financial data: {financial_doc}")
    
    print("\nListing processed documents:")
    docs = list_processed_documents()
    for doc in docs:
        print(f"- {doc['id']}: {doc['metadata'].get('title', 'Untitled')} ({doc['chunks']} chunks)")
