"""
Unit tests for the LangGraph runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from agents.langgraph.runner import LangGraphRunner

class TestLangGraphRunner:
    """Test cases for the LangGraph runner."""
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests module for testing."""
        with patch('agents.langgraph.runner.requests') as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [
                    {
                        "chunk": "Test company information",
                        "metadata": {"source": "test"},
                        "score": 0.95
                    }
                ]
            }
            mock_requests.get.return_value = mock_response
            yield mock_requests
    
    @pytest.fixture
    def langgraph_runner(self):
        """Create a LangGraph runner instance for testing."""
        return LangGraphRunner("http://localhost:8000")
    
    def test_initialization(self, langgraph_runner):
        """Test LangGraph runner initialization."""
        assert langgraph_runner.agent_name == "langgraph"
        assert langgraph_runner.rag_service_url == "http://localhost:8000"
    
    def test_run_task(self, langgraph_runner, mock_requests):
        """Test run_task method."""
        with patch('time.sleep'):  # Mock sleep to speed up tests
            result = langgraph_runner.run_task("Test Company")
            
            assert result["agent_name"] == "langgraph"
            assert "Test Company" in result["final_output"]
            assert len(result["steps"]) > 0
            assert result["token_usage"] > 0
            assert isinstance(result["response_time"], float)
    
    def test_query_rag_service_success(self, langgraph_runner, mock_requests):
        """Test _query_rag_service method with successful response."""
        results = langgraph_runner._query_rag_service("Test Company", "company information")
        
        assert len(results) == 1
        assert results[0]["text"] == "Test company information"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["score"] == 0.95
        
        mock_requests.get.assert_called_once_with(
            "http://localhost:8000/query",
            params={"q": "Test Company company information", "top_k": 3}
        )
    
    def test_query_rag_service_error(self, langgraph_runner):
        """Test _query_rag_service method with error response."""
        with patch('agents.langgraph.runner.requests.get') as mock_get:
            mock_get.side_effect = Exception("Test error")
            
            results = langgraph_runner._query_rag_service("Test Company", "company information")
            
            assert len(results) == 1
            assert "Test Company" in results[0]["text"]
            assert results[0]["metadata"]["source"] == "simulated"
    
    def test_simulate_graph_execution(self, langgraph_runner):
        """Test _simulate_graph_execution method."""
        with patch('time.sleep'):
            with patch.object(langgraph_runner, '_add_step') as mock_add_step:
                company_info = [{"text": "Test company info"}]
                news_info = [{"text": "Test news"}]
                product_info = [{"text": "Test products"}]
                financial_info = [{"text": "Test financials"}]
                
                langgraph_runner._simulate_graph_execution(
                    "Test Company", 
                    company_info, 
                    news_info, 
                    product_info, 
                    financial_info
                )
                
                assert mock_add_step.call_count >= 3
    
    def test_generate_report(self, langgraph_runner):
        """Test _generate_report method."""
        with patch('time.sleep'):
            company_info = [{"text": "Test company info"}]
            news_info = [{"text": "Test news"}]
            product_info = [{"text": "Test products"}]
            financial_info = [{"text": "Test financials"}]
            
            report = langgraph_runner._generate_report(
                "Test Company", 
                company_info, 
                news_info, 
                product_info, 
                financial_info
            )
            
            assert "Test Company" in report
            assert "Test company info" in report
            assert "Test news" in report
            assert "Test products" in report
            assert "Test financials" in report
