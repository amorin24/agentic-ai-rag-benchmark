"""
Test script for the new ingest functions in rag_service/ingest.py.
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

data_dir = Path("data/processed")
data_dir.mkdir(parents=True, exist_ok=True)

try:
    from rag_service.ingest import ingest_news_topic, ingest_financial_data
    logger.info("Successfully imported ingest functions")
except ImportError as e:
    logger.error(f"Failed to import ingest functions: {str(e)}")
    exit(1)

def test_ingest_news_topic():
    """Test the ingest_news_topic function."""
    logger.info("Testing ingest_news_topic function...")
    
    topic = "Tesla"
    logger.info(f"Fetching news for topic: {topic}")
    news_files = ingest_news_topic(topic, max_articles=2)
    logger.info(f"Created {len(news_files)} news files")
    
    invalid_topic = "xyznonexistenttopic123456789"
    logger.info(f"Testing with invalid topic: {invalid_topic}")
    invalid_news_files = ingest_news_topic(invalid_topic, max_articles=1)
    logger.info(f"Created {len(invalid_news_files)} news files for invalid topic")
    
    return news_files

def test_ingest_financial_data():
    """Test the ingest_financial_data function."""
    logger.info("Testing ingest_financial_data function...")
    
    ticker = "AAPL"
    logger.info(f"Fetching financial data for ticker: {ticker}")
    financial_file = ingest_financial_data(ticker)
    logger.info(f"Created financial file: {financial_file}")
    
    invalid_ticker = "XYZNONEXISTENT"
    logger.info(f"Testing with invalid ticker: {invalid_ticker}")
    invalid_financial_file = ingest_financial_data(invalid_ticker)
    logger.info(f"Result for invalid ticker: {invalid_financial_file}")
    
    return financial_file

if __name__ == "__main__":
    logger.info("Starting tests for ingest functions")
    
    news_files = test_ingest_news_topic()
    financial_file = test_ingest_financial_data()
    
    logger.info("\nTest Results:")
    logger.info(f"News files created: {len(news_files)}")
    logger.info(f"Financial file created: {financial_file}")
    
    if news_files:
        for file in news_files:
            if os.path.exists(file):
                logger.info(f"Verified news file exists: {file}")
            else:
                logger.error(f"News file does not exist: {file}")
    
    if financial_file and os.path.exists(financial_file):
        logger.info(f"Verified financial file exists: {financial_file}")
    elif financial_file:
        logger.error(f"Financial file does not exist: {financial_file}")
    
    logger.info("Tests completed")
