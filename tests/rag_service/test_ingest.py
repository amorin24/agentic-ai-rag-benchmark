"""
Unit tests for the ingest module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import json

from rag_service.ingest import (
    clean_text,
    chunk_text,
    extract_content_from_url,
    ingest_text,
    ingest_url,
    ingest_file,
    ingest_wikipedia_article,
    ingest_news_topic,
    ingest_financial_data
)

class TestIngestModule:
    """Test cases for the ingest module."""
    
    def test_clean_text(self):
        """Test clean_text function."""
        dirty_text = "This is a test\n\n  with extra   spaces \t and tabs."
        cleaned_text = clean_text(dirty_text)
        
        assert cleaned_text == "This is a test with extra spaces and tabs."
        assert "\n" not in cleaned_text
        assert "\t" not in cleaned_text
        assert "  " not in cleaned_text
    
    def test_chunk_text_default_params(self):
        """Test chunk_text function with default parameters."""
        text = "This is a test sentence. This is another test sentence. And here's a third one."
        chunks = chunk_text(text)
        
        assert len(chunks) > 0
        assert isinstance(chunks[0], str)
        assert "test sentence" in chunks[0]
    
    def test_chunk_text_custom_params(self):
        """Test chunk_text function with custom parameters."""
        text = "This is a test sentence. This is another test sentence. And here's a third one."
        chunks = chunk_text(text, chunk_size=10, chunk_overlap=2)
        
        assert len(chunks) > 1  # Should create multiple small chunks
        assert len(chunks[0]) <= 15  # Approximate max length with small chunks
    
    @patch('rag_service.ingest.requests.get')
    @patch('rag_service.ingest.BeautifulSoup')
    def test_extract_content_from_url(self, mock_bs, mock_get):
        """Test extract_content_from_url function."""
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Test content</p></body></html>"
        mock_get.return_value = mock_response
        
        mock_soup = MagicMock()
        mock_soup.get_text.return_value = "Test content"
        mock_bs.return_value = mock_soup
        
        content = extract_content_from_url("https://example.com")
        
        assert content == "Test content"
        mock_get.assert_called_once_with("https://example.com", timeout=10)
        mock_bs.assert_called_once()
    
    @patch('rag_service.ingest.extract_content_from_url')
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.path.exists')
    @patch('rag_service.ingest.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_ingest_url(self, mock_open, mock_makedirs, mock_exists, 
                        mock_chunk, mock_clean, mock_extract):
        """Test ingest_url function."""
        mock_exists.return_value = False
        mock_extract.return_value = "Test content from URL"
        mock_clean.return_value = "Test content from URL"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_url("https://example.com", "test_source")
        
        assert len(result) == 2
        assert result[0]["text"] == "Chunk 1"
        assert result[0]["metadata"]["source"] == "test_source"
        assert result[0]["metadata"]["url"] == "https://example.com"
        
        mock_extract.assert_called_once_with("https://example.com")
        mock_clean.assert_called_once()
        mock_chunk.assert_called_once()
        mock_makedirs.assert_called_once()
        assert mock_open.call_count == 1
    
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.path.exists')
    @patch('rag_service.ingest.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_ingest_text(self, mock_open, mock_makedirs, mock_exists, 
                         mock_chunk, mock_clean):
        """Test ingest_text function."""
        mock_exists.return_value = False
        mock_clean.return_value = "Test content"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_text("Test content", "test_source")
        
        assert len(result) == 2
        assert result[0]["text"] == "Chunk 1"
        assert result[0]["metadata"]["source"] == "test_source"
        
        mock_clean.assert_called_once_with("Test content")
        mock_chunk.assert_called_once()
        mock_makedirs.assert_called_once()
        assert mock_open.call_count == 1
    
    @patch('rag_service.ingest.os.path.exists')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.makedirs')
    def test_ingest_file(self, mock_makedirs, mock_chunk, mock_clean, 
                         mock_open, mock_exists):
        """Test ingest_file function."""
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "Test file content"
        mock_open.return_value = mock_file
        
        mock_clean.return_value = "Test file content"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_file("/path/to/test.txt", "test_source")
        
        assert len(result) == 2
        assert result[0]["text"] == "Chunk 1"
        assert result[0]["metadata"]["source"] == "test_source"
        assert result[0]["metadata"]["file"] == "/path/to/test.txt"
        
        mock_open.assert_called_with("/path/to/test.txt", "r", encoding="utf-8")
        mock_clean.assert_called_once()
        mock_chunk.assert_called_once()
    
    @patch('rag_service.ingest.wikipedia')
    @patch('rag_service.ingest.ingest_text')
    def test_ingest_wikipedia_article(self, mock_ingest_text, mock_wikipedia):
        """Test ingest_wikipedia_article function."""
        mock_wikipedia.page.return_value.content = "Wikipedia article content"
        mock_wikipedia.page.return_value.url = "https://en.wikipedia.org/wiki/Test"
        mock_ingest_text.return_value = [{"text": "Chunk 1", "metadata": {}}]
        
        result = ingest_wikipedia_article("Test Article")
        
        assert result == [{"text": "Chunk 1", "metadata": {}}]
        mock_wikipedia.page.assert_called_once_with("Test Article")
        mock_ingest_text.assert_called_once_with(
            "Wikipedia article content",
            "wikipedia",
            {"title": "Test Article", "url": "https://en.wikipedia.org/wiki/Test"}
        )
    
    @patch('rag_service.ingest.requests.get')
    @patch('rag_service.ingest.ingest_text')
    @patch('rag_service.ingest.os.getenv')
    def test_ingest_news_topic(self, mock_getenv, mock_ingest_text, mock_get):
        """Test ingest_news_topic function."""
        mock_getenv.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "articles": [
                {
                    "title": "Test Article",
                    "description": "Test description",
                    "content": "Test content",
                    "url": "https://example.com/news/1"
                }
            ]
        }
        mock_get.return_value = mock_response
        mock_ingest_text.return_value = [{"text": "Chunk 1", "metadata": {}}]
        
        result = ingest_news_topic("Test Topic")
        
        assert result == [{"text": "Chunk 1", "metadata": {}}]
        mock_get.assert_called_once()
        assert "test_api_key" in mock_get.call_args[0][0]
        assert "Test Topic" in mock_get.call_args[0][0]
        mock_ingest_text.assert_called_once()
    
    @patch('rag_service.ingest.requests.get')
    @patch('rag_service.ingest.ingest_text')
    @patch('rag_service.ingest.os.getenv')
    def test_ingest_financial_data(self, mock_getenv, mock_ingest_text, mock_get):
        """Test ingest_financial_data function."""
        mock_getenv.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbol": "AAPL",
            "profile": {"companyName": "Apple Inc."},
            "financials": {"income": {"revenue": 1000000}},
            "news": [{"title": "Test News", "text": "Test news content"}]
        }
        mock_get.return_value = mock_response
        mock_ingest_text.return_value = [{"text": "Chunk 1", "metadata": {}}]
        
        result = ingest_financial_data("AAPL")
        
        assert result == [{"text": "Chunk 1", "metadata": {}}]
        mock_get.assert_called()
        assert "test_api_key" in mock_get.call_args[0][0]
        assert "AAPL" in mock_get.call_args[0][0]
        mock_ingest_text.assert_called_once()
