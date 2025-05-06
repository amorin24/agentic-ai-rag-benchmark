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
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from bs4 import BeautifulSoup
import wikipedia
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

PROCESSED_DIR = Path(os.getenv('PROCESSED_DOCS_DIR', 'data/processed'))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
FMP_API_KEY = os.getenv('FMP_API_KEY', '')  # Financial Modeling Prep API key
WIKIPEDIA_MAX_ARTICLES = int(os.getenv('WIKIPEDIA_MAX_ARTICLES', '5'))
WIKIPEDIA_LANGUAGE = os.getenv('WIKIPEDIA_LANGUAGE', 'en')

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
    
    chunks = chunk_text(result["text"])
    
    return save_processed_document(doc_id, chunks, result["metadata"])


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
    
    text = clean_text(text)
    
    doc_id = f"text_{hash(text[:100])}_{int(time.time())}"
    
    chunks = chunk_text(text)
    
    return save_processed_document(doc_id, chunks, metadata)


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
                logger.info(f"Retrieving Wikipedia article: {title}")
                page = wikipedia.page(title)
                
                text = clean_text(page.content)
                
                doc_id = f"wiki_{hash(title)}_{int(time.time())}"
                
                chunks = chunk_text(text)
                
                metadata = {
                    "source": "wikipedia",
                    "title": title,
                    "url": page.url,
                    "type": "wikipedia",
                    "language": WIKIPEDIA_LANGUAGE
                }
                
                file_path = save_processed_document(doc_id, chunks, metadata)
                processed_docs.append(file_path)
                logger.info(f"Successfully processed Wikipedia article: {title}")
                
            except wikipedia.exceptions.DisambiguationError as e:
                logger.warning(f"Disambiguation error for '{title}': {str(e)}")
                if e.options:
                    try:
                        alt_title = e.options[0]
                        logger.info(f"Trying alternative: {alt_title}")
                        page = wikipedia.page(alt_title)
                        
                        text = clean_text(page.content)
                        
                        doc_id = f"wiki_{hash(alt_title)}_{int(time.time())}"
                        
                        chunks = chunk_text(text)
                        
                        metadata = {
                            "source": "wikipedia",
                            "title": alt_title,
                            "original_query": title,
                            "url": page.url,
                            "type": "wikipedia",
                            "language": WIKIPEDIA_LANGUAGE
                        }
                        
                        file_path = save_processed_document(doc_id, chunks, metadata)
                        processed_docs.append(file_path)
                        logger.info(f"Successfully processed alternative Wikipedia article: {alt_title}")
                    except Exception as inner_e:
                        logger.error(f"Failed to process alternative Wikipedia article {alt_title}: {str(inner_e)}")
                continue
            except Exception as e:
                logger.error(f"Failed to process Wikipedia article {title}: {str(e)}")
                continue
        
        if not processed_docs:
            logger.warning(f"No Wikipedia articles were successfully processed for topic: {topic}")
        else:
            logger.info(f"Successfully processed {len(processed_docs)} Wikipedia articles for topic: {topic}")
            
        return processed_docs
    
    except Exception as e:
        logger.error(f"Failed to search Wikipedia for {topic}: {str(e)}")
        raise


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
        
        company_name = profile_data[0].get('companyName', symbol)
        description = profile_data[0].get('description', '')
        sector = profile_data[0].get('sector', '')
        industry = profile_data[0].get('industry', '')
        
        text = f"Company: {company_name}\n"
        text += f"Symbol: {symbol}\n"
        text += f"Sector: {sector}\n"
        text += f"Industry: {industry}\n\n"
        text += f"Description: {description}\n\n"
        text += "Financial Data:\n"
        
        for statement in financials_data:
            text += f"Year: {statement.get('date', 'N/A')}\n"
            text += f"Revenue: ${statement.get('revenue', 0):,}\n"
            text += f"Net Income: ${statement.get('netIncome', 0):,}\n"
            text += f"EPS: ${statement.get('eps', 0)}\n\n"
        
        text = clean_text(text)
        
        doc_id = f"financial_{symbol}_{int(time.time())}"
        
        chunks = chunk_text(text)
        
        metadata = {
            "source": "financial_modeling_prep",
            "symbol": symbol,
            "company_name": company_name,
            "type": "financial"
        }
        
        return save_processed_document(doc_id, chunks, metadata)
    
    except Exception as e:
        logger.error(f"Failed to ingest financial data for {symbol}: {str(e)}")
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
        
        text = clean_text(text)
        
        doc_id = f"file_{hash(file_name)}_{int(time.time())}"
        
        chunks = chunk_text(text)
        
        metadata = {
            "source": "file",
            "file_name": file_name,
            "file_type": file_ext,
            "type": "file"
        }
        
        return save_processed_document(doc_id, chunks, metadata)
    
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


if __name__ == "__main__":
    print("Ingesting from Wikipedia...")
    wiki_docs = ingest_from_wikipedia("Artificial Intelligence", max_articles=2)
    print(f"Processed {len(wiki_docs)} Wikipedia articles")
    
    print("\nListing processed documents:")
    docs = list_processed_documents()
    for doc in docs:
        print(f"- {doc['id']}: {doc['metadata'].get('title', 'Untitled')} ({doc['chunks']} chunks)")
