"""
NewsAPI integration module for the Agentic AI RAG Benchmark project.

This module provides functions to fetch news articles from NewsAPI.
It handles API requests, error handling, and data normalization.
"""

import logging
import time
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from utils.config import NEWS_API_KEY, NEWS_API_MAX_ARTICLES, NEWS_API_SORT_BY, LOGS_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

failed_requests_handler = logging.FileHandler(LOGS_DIR / 'news_api_errors.log')
failed_requests_handler.setLevel(logging.ERROR)
failed_requests_logger = logging.getLogger('news_api_errors')
failed_requests_logger.addHandler(failed_requests_handler)
failed_requests_logger.propagate = False  # Don't propagate to root logger


def fetch_news(topic: str, max_articles: int = NEWS_API_MAX_ARTICLES, 
               sort_by: str = NEWS_API_SORT_BY, days_back: int = 30) -> List[Dict]:
    """
    Fetch news articles from NewsAPI based on a topic.
    
    Args:
        topic: Topic to search for
        max_articles: Maximum number of articles to fetch
        sort_by: Sorting method (relevancy, popularity, publishedAt)
        days_back: Number of days to look back for articles
        
    Returns:
        List of dictionaries containing normalized news article data
    """
    if not NEWS_API_KEY:
        logger.error("NewsAPI key not found in environment variables")
        failed_requests_logger.error(f"API key missing for topic: {topic}")
        return []
    
    try:
        logger.info(f"Fetching news for '{topic}' (max articles: {max_articles}, sort: {sort_by})")
        
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
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") != "ok":
            error_message = f"NewsAPI returned error: {data.get('message', 'Unknown error')}"
            logger.error(error_message)
            failed_requests_logger.error(f"API error for topic '{topic}': {error_message}")
            return []
        
        articles = data.get("articles", [])
        logger.info(f"Found {len(articles)} articles about '{topic}'")
        
        normalized_articles = []
        for article in articles:
            try:
                normalized_article = {
                    "title": article.get("title", "").strip(),
                    "source": article.get("source", {}).get("name", "Unknown Source"),
                    "author": article.get("author", "Unknown Author"),
                    "published_at": article.get("publishedAt", ""),
                    "url": article.get("url", ""),
                    "description": article.get("description", "").strip(),
                    "content": article.get("content", "").strip(),
                    "fetch_timestamp": datetime.now().isoformat(),
                    "topic": topic
                }
                
                if not normalized_article["title"]:
                    continue
                    
                normalized_articles.append(normalized_article)
                
            except Exception as e:
                logger.warning(f"Failed to normalize article: {str(e)}")
                continue
        
        if not normalized_articles:
            logger.warning(f"No news articles were successfully processed for topic: {topic}")
        else:
            logger.info(f"Successfully processed {len(normalized_articles)} news articles for topic: {topic}")
            
        return normalized_articles
    
    except requests.exceptions.Timeout:
        error_message = f"Request to NewsAPI timed out for topic: {topic}"
        logger.error(error_message)
        failed_requests_logger.error(error_message)
        return []
        
    except requests.exceptions.RequestException as e:
        error_message = f"Request to NewsAPI failed for topic '{topic}': {str(e)}"
        logger.error(error_message)
        failed_requests_logger.error(error_message)
        return []
        
    except Exception as e:
        error_message = f"Unexpected error fetching news for topic '{topic}': {str(e)}"
        logger.error(error_message)
        failed_requests_logger.error(error_message)
        return []


if __name__ == "__main__":
    """Test the news API functionality."""
    import json
    
    articles = fetch_news("Artificial Intelligence", max_articles=3)
    print(f"Fetched {len(articles)} articles about AI")
    
    if articles:
        print("\nSample article:")
        print(json.dumps(articles[0], indent=2))
    
    import os
    original_key = os.environ.get('NEWS_API_KEY', '')
    os.environ['NEWS_API_KEY'] = 'invalid_key'
    
    print("\nTesting with invalid API key:")
    invalid_articles = fetch_news("Test", max_articles=1)
    print(f"Result: {invalid_articles}")
    
    os.environ['NEWS_API_KEY'] = original_key
