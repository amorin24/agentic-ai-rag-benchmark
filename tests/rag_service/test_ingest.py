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
    extract_text_from_url,
    ingest_from_text,
    ingest_from_url,
    ingest_from_file,
    ingest_from_wikipedia,
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
    def test_extract_text_from_url(self, mock_bs, mock_get):
        """Test extract_text_from_url function."""
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Test content</p></body></html>"
        mock_get.return_value = mock_response
        
        mock_soup = MagicMock()
        mock_soup.get_text.return_value = "Test content"
        mock_bs.return_value = mock_soup
        
        content = extract_text_from_url("https://example.com")
        
        assert content["text"] == "Test content"
        assert content["metadata"]["source"] == "https://example.com"
        assert "title" in content["metadata"]
        assert content["metadata"]["type"] == "web"
        mock_get.assert_called_once_with("https://example.com", headers={'User-Agent': 'Mozilla/5.0'})
        mock_bs.assert_called_once()
    
    @patch('rag_service.ingest.extract_text_from_url')
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.path.exists')
    @patch('rag_service.ingest.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_ingest_from_url(self, mock_open, mock_makedirs, mock_exists, 
                        mock_chunk, mock_clean, mock_extract):
        """Test ingest_from_url function."""
        mock_exists.return_value = False
        mock_extract.return_value = {
            "text": "Test content from URL",
            "metadata": {
                "source": "https://example.com",
                "title": "Test Title",
                "type": "web"
            }
        }
        mock_clean.return_value = "Test content from URL"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_from_url("https://example.com")
        
        assert isinstance(result, str)
        assert "url_" in result
        assert ".json" in result
        
        mock_extract.assert_called_once_with("https://example.com")
        mock_clean.assert_called_once()
        mock_chunk.assert_called_once()
        # mock_makedirs.assert_called_once()
        assert mock_open.call_count == 1
    
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.path.exists')
    @patch('rag_service.ingest.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_ingest_from_text(self, mock_open, mock_makedirs, mock_exists, 
                         mock_chunk, mock_clean):
        """Test ingest_from_text function."""
        mock_exists.return_value = False
        mock_clean.return_value = "Test content"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_from_text("Test content")
        
        assert isinstance(result, str)
        assert "text_" in result
        assert ".json" in result
        
        mock_clean.assert_called_once_with("Test content")
        mock_chunk.assert_called_once()
        # mock_makedirs.assert_called_once()
        assert mock_open.call_count == 1
    
    @patch('rag_service.ingest.os.path.exists')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('rag_service.ingest.clean_text')
    @patch('rag_service.ingest.chunk_text')
    @patch('rag_service.ingest.os.makedirs')
    def test_ingest_from_file(self, mock_makedirs, mock_chunk, mock_clean, 
                         mock_open, mock_exists):
        """Test ingest_from_file function."""
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "Test file content"
        mock_open.side_effect = [mock_file, MagicMock()]  # First for reading, second for writing
        
        mock_clean.return_value = "Test file content"
        mock_chunk.return_value = ["Chunk 1", "Chunk 2"]
        
        result = ingest_from_file("/path/to/test.txt")
        
        assert isinstance(result, str)
        assert "file_" in result
        assert ".json" in result
        
        assert mock_open.call_args_list[0][0][0] == "/path/to/test.txt"
        assert mock_open.call_args_list[0][0][1] == "r"
        
        mock_clean.assert_called_once()
        mock_chunk.assert_called_once()
    
    @patch('rag_service.ingest.wikipedia')
    @patch('rag_service.ingest.process_wikipedia_article')
    def test_ingest_from_wikipedia(self, mock_process_article, mock_wikipedia):
        """Test ingest_from_wikipedia function."""
        mock_process_article.return_value = "/path/to/wikipedia_file.json"
        mock_wikipedia.search.return_value = ["Test Article"]
        
        result = ingest_from_wikipedia("Test Article")
        
        assert isinstance(result, list)
        assert len(result) > 0
        mock_wikipedia.search.assert_called_once()
        mock_process_article.assert_called_once_with("Test Article")
    
    @patch('rag_service.ingest.fetch_news')
    @patch('rag_service.ingest.process_news_article')
    def test_ingest_news_topic(self, mock_process_article, mock_fetch_news):
        """Test ingest_news_topic function."""
        mock_fetch_news.return_value = [
            {
                "title": "Test Article",
                "description": "Test description",
                "content": "Test content",
                "url": "https://example.com/news/1"
            }
        ]
        mock_process_article.return_value = "/path/to/news_file.json"
        
        result = ingest_news_topic("Test Topic")
        
        assert isinstance(result, list)
        assert len(result) > 0
        mock_fetch_news.assert_called_once_with("Test Topic", max_articles=10)
        mock_process_article.assert_called_once()
    
    @patch('rag_service.ingest.fetch_financials')
    @patch('rag_service.ingest.process_financial_data')
    def test_ingest_financial_data(self, mock_process_data, mock_fetch_financials):
        """Test ingest_financial_data function."""
        mock_fetch_financials.return_value = {
            "company_profile": {"companyName": "Apple Inc."},
            "income_statement": [{"revenue": 1000000}],
            "news": [{"title": "Test News", "text": "Test news content"}]
        }
        mock_process_data.return_value = "/path/to/financial_file.json"
        
        result = ingest_financial_data("AAPL")
        
        assert isinstance(result, str)
        assert result == "/path/to/financial_file.json"
        mock_fetch_financials.assert_called_once_with("AAPL")
        mock_process_data.assert_called_once()
