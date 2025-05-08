"""
Unit tests for the CrewAI runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from agents.crewai.runner import CrewAIRunner

class TestCrewAIRunner:
    """Test cases for the CrewAI runner."""
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests module for testing."""
        with patch('agents.crewai.runner.requests') as mock_requests:
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
    def crewai_runner(self):
        """Create a CrewAI runner instance for testing."""
        return CrewAIRunner("http://localhost:8000")
    
    def test_initialization(self, crewai_runner):
        """Test CrewAI runner initialization."""
        assert crewai_runner.agent_name == "crewai"
        assert crewai_runner.rag_service_url == "http://localhost:8000"
    
    def test_run_task(self, crewai_runner, mock_requests):
        """Test run_task method."""
        with patch('time.sleep'):  # Mock sleep to speed up tests
            result = crewai_runner.run_task("Test Company")
            
            assert result["agent_name"] == "crewai"
            assert "Test Company" in result["final_output"]
            assert len(result["steps"]) > 0
            assert result["token_usage"] > 0
            assert isinstance(result["response_time"], float)
    
    def test_query_rag_service_success(self, crewai_runner, mock_requests):
        """Test _query_rag_service method with successful response."""
        results = crewai_runner._query_rag_service("Test Company", "company information")
        
        assert len(results) == 1
        assert results[0]["text"] == "Test company information"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["score"] == 0.95
        
        mock_requests.get.assert_called_once_with(
            "http://localhost:8000/query",
            params={"q": "Test Company company information", "top_k": 3}
        )
    
    def test_query_rag_service_error(self, crewai_runner):
        """Test _query_rag_service method with error response."""
        with patch('agents.crewai.runner.requests.get') as mock_get:
            mock_get.side_effect = Exception("Test error")
            
            results = crewai_runner._query_rag_service("Test Company", "company information")
            
            assert len(results) == 1
            assert "Test Company" in results[0]["text"]
            assert results[0]["metadata"]["source"] == "simulated"
    
    def test_generate_placeholder_results(self, crewai_runner):
        """Test _generate_placeholder_results method."""
        company = "Test Company"
        
        results = crewai_runner._generate_placeholder_results(company, "company information")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert results[0]["metadata"]["source"] == "simulated"
        
        results = crewai_runner._generate_placeholder_results(company, "latest news")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "partnership" in results[0]["text"].lower()
        
        results = crewai_runner._generate_placeholder_results(company, "unknown aspect")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "unknown aspect" in results[0]["text"].lower()
    
    def test_simulate_analysis(self, crewai_runner):
        """Test _simulate_analysis method."""
        with patch('time.sleep'):
            with patch.object(crewai_runner, '_add_step') as mock_add_step:
                company_info = [{"text": "Test company info"}]
                news_info = [{"text": "Test news"}]
                product_info = [{"text": "Test products"}]
                financial_info = [{"text": "Test financials"}]
                
                crewai_runner._simulate_analysis(
                    "Test Company", 
                    company_info, 
                    news_info, 
                    product_info, 
                    financial_info
                )
                
                assert mock_add_step.call_count == 4
    
    def test_generate_report(self, crewai_runner):
        """Test _generate_report method."""
        with patch('time.sleep'):
            company_info = [{"text": "Test company info"}]
            news_info = [{"text": "Test news"}]
            product_info = [{"text": "Test products"}]
            financial_info = [{"text": "Test financials"}]
            
            report = crewai_runner._generate_report(
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
