"""
Comprehensive tests for the RAG service API endpoints.
"""

import pytest
import json
import faiss
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from rag_service.app.api import app

client = TestClient(app)

class TestRAGServiceAPI:
    """Comprehensive test cases for the RAG service API."""
    
    @pytest.fixture
    def mock_retriever(self):
        """Mock retriever for testing."""
        with patch('rag_service.app.api.get_retriever') as mock_get_retriever:
            mock_retriever = MagicMock()
            mock_retriever.add_texts.return_value = ["id1", "id2"]
            mock_retriever.search.return_value = [
                {
                    "chunk_id": "id1",
                    "text": "Test result 1",
                    "metadata": {"source": "test"},
                    "score": 0.95
                }
            ]
            mock_retriever.get_index_stats.return_value = {
                "name": "default",
                "size": 10,
                "last_updated": 1234567890
            }
            mock_get_retriever.return_value = mock_retriever
            yield mock_retriever
    
    @pytest.fixture
    def mock_embedder(self):
        """Mock embedder for testing."""
        with patch('rag_service.app.api.get_embedder') as mock_get_embedder:
            mock_embedder = MagicMock()
            mock_embedder.embed_text.return_value = np.random.rand(1, 384).astype(np.float32)
            mock_embedder.get_dimension.return_value = 384
            mock_get_embedder.return_value = mock_embedder
            yield mock_embedder
    
    @pytest.fixture
    def mock_ingest_functions(self):
        """Mock ingest functions for testing."""
        with patch('rag_service.app.api.ingest_from_text') as mock_ingest_text, \
             patch('rag_service.app.api.ingest_from_url') as mock_ingest_url, \
             patch('rag_service.app.api.ingest_from_file') as mock_ingest_file, \
             patch('rag_service.app.api.ingest_from_wikipedia') as mock_ingest_wiki, \
             patch('rag_service.app.api.ingest_news_topic') as mock_ingest_news, \
             patch('rag_service.app.api.ingest_financial_data') as mock_ingest_financial:
            
            mock_ingest_text.return_value = "text_12345.json"
            mock_ingest_url.return_value = "url_12345.json"
            mock_ingest_file.return_value = "file_12345.json"
            mock_ingest_wiki.return_value = ["wiki_12345.json"]
            mock_ingest_news.return_value = ["news_12345.json"]
            mock_ingest_financial.return_value = "financial_12345.json"
            
            yield {
                "text": mock_ingest_text,
                "url": mock_ingest_url,
                "file": mock_ingest_file,
                "wiki": mock_ingest_wiki,
                "news": mock_ingest_news,
                "financial": mock_ingest_financial
            }
    
    def test_status_endpoint_success(self, mock_retriever):
        """Test the status endpoint with successful response."""
        response = client.get("/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "vector_store_size" in data
        assert "last_ingest" in data
    
    def test_status_endpoint_error(self, mock_retriever):
        """Test the status endpoint with error."""
        mock_retriever.get_index_stats.side_effect = Exception("Test error")
        
        response = client.get("/status")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Error getting status" in data["detail"]
    
    def test_query_endpoint_success(self, mock_retriever):
        """Test the query endpoint with successful response."""
        response = client.get("/query?q=test%20query&top_k=3")
        
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "test query"
        assert "results" in data
        assert len(data["results"]) > 0
        assert "total_chunks" in data
        assert "time_taken" in data
    
    def test_query_endpoint_missing_query(self):
        """Test the query endpoint with missing query parameter."""
        response = client.get("/query")
        
        assert response.status_code == 422  # Validation error
    
    def test_query_endpoint_empty_query(self):
        """Test the query endpoint with empty query parameter."""
        response = client.get("/query?q=")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Query cannot be empty" in data["detail"]
    
    def test_query_endpoint_search_error(self, mock_retriever):
        """Test the query endpoint with search error."""
        mock_retriever.search.side_effect = Exception("Test search error")
        
        response = client.get("/query?q=test%20query")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Error searching" in data["detail"]
    
    def test_ingest_text_success(self, mock_retriever, mock_ingest_functions):
        """Test ingesting text with successful response."""
        response = client.post(
            "/ingest",
            json={"text": "This is a test document.", "metadata": {"source": "test"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "chunks_ingested" in data
        assert "vector_store_size" in data
        
        mock_ingest_functions["text"].assert_called_once_with(
            "This is a test document.",
            metadata={"source": "test"}
        )
    
    def test_ingest_url_success(self, mock_retriever, mock_ingest_functions):
        """Test ingesting URL with successful response."""
        response = client.post(
            "/ingest",
            json={"url": "https://example.com", "metadata": {"source_type": "web"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        mock_ingest_functions["url"].assert_called_once_with(
            "https://example.com",
            metadata={"source_type": "web"}
        )
    
    def test_ingest_wikipedia_success(self, mock_retriever, mock_ingest_functions):
        """Test ingesting Wikipedia article with successful response."""
        response = client.post(
            "/ingest",
            json={"wikipedia": "Artificial Intelligence", "metadata": {"source_type": "wikipedia"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        mock_ingest_functions["wiki"].assert_called_once_with(
            "Artificial Intelligence",
            metadata={"source_type": "wikipedia"}
        )
    
    def test_ingest_news_success(self, mock_retriever, mock_ingest_functions):
        """Test ingesting news with successful response."""
        response = client.post(
            "/ingest",
            json={"news": "AI advancements", "metadata": {"source_type": "news"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        mock_ingest_functions["news"].assert_called_once_with(
            "AI advancements",
            metadata={"source_type": "news"}
        )
    
    def test_ingest_financial_success(self, mock_retriever, mock_ingest_functions):
        """Test ingesting financial data with successful response."""
        response = client.post(
            "/ingest",
            json={"financial": "AAPL", "metadata": {"source_type": "financial"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        mock_ingest_functions["financial"].assert_called_once_with(
            "AAPL",
            metadata={"source_type": "financial"}
        )
    
    def test_ingest_missing_source(self):
        """Test ingesting with missing source."""
        response = client.post(
            "/ingest",
            json={"metadata": {"source": "test"}}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "No ingest source provided" in data["detail"]
    
    def test_ingest_multiple_sources(self):
        """Test ingesting with multiple sources."""
        response = client.post(
            "/ingest",
            json={
                "text": "Test document",
                "url": "https://example.com",
                "metadata": {"source": "test"}
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Multiple ingest sources provided" in data["detail"]
    
    def test_ingest_error(self, mock_ingest_functions):
        """Test ingesting with error."""
        mock_ingest_functions["text"].side_effect = Exception("Test ingest error")
        
        response = client.post(
            "/ingest",
            json={"text": "This is a test document.", "metadata": {"source": "test"}}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Error ingesting" in data["detail"]
    
    def test_clear_endpoint_success(self, mock_retriever):
        """Test clearing the vector store with successful response."""
        response = client.post("/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
        
        mock_retriever.clear_index.assert_called_once()
    
    def test_clear_endpoint_error(self, mock_retriever):
        """Test clearing the vector store with error."""
        mock_retriever.clear_index.side_effect = Exception("Test clear error")
        
        response = client.post("/clear")
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Error clearing vector store" in data["detail"]
