"""
Unit tests for the UiPath runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from agents.uipath.runner import UiPathRunner

class TestUiPathRunner:
    """Test cases for the UiPath runner."""
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests module for testing."""
        with patch('agents.uipath.runner.requests') as mock_requests:
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
    def uipath_runner(self):
        """Create a UiPath runner instance for testing."""
        return UiPathRunner("http://localhost:8000")
    
    def test_initialization(self, uipath_runner):
        """Test UiPath runner initialization."""
        assert uipath_runner.agent_name == "uipath"
        assert uipath_runner.rag_service_url == "http://localhost:8000"
    
    def test_run_task(self, uipath_runner, mock_requests):
        """Test run_task method."""
        with patch('time.sleep'):  # Mock sleep to speed up tests
            result = uipath_runner.run_task("Test Company")
            
            assert result["agent_name"] == "uipath"
            assert "Test Company" in result["final_output"]
            assert len(result["steps"]) > 0
            assert result["token_usage"] > 0
            assert isinstance(result["response_time"], float)
    
    def test_query_rag_service_success(self, uipath_runner, mock_requests):
        """Test _query_rag_service method with successful response."""
        results = uipath_runner._query_rag_service("Test Company", "company information")
        
        assert len(results) == 1
        assert results[0]["text"] == "Test company information"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["score"] == 0.95
        
        mock_requests.get.assert_called_once_with(
            "http://localhost:8000/query",
            params={"q": "Test Company company information", "top_k": 3}
        )
    
    def test_query_rag_service_error(self, uipath_runner):
        """Test _query_rag_service method with error response."""
        with patch('agents.uipath.runner.requests.get') as mock_get:
            mock_get.side_effect = Exception("Test error")
            
            results = uipath_runner._query_rag_service("Test Company", "company information")
            
            assert len(results) == 1
            assert "Test Company" in results[0]["text"]
            assert results[0]["metadata"]["source"] == "simulated"
    
    def test_generate_placeholder_results(self, uipath_runner):
        """Test _generate_placeholder_results method."""
        company = "Test Company"
        
        results = uipath_runner._generate_placeholder_results(company, "company information")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert results[0]["metadata"]["source"] == "simulated"
        
        results = uipath_runner._generate_placeholder_results(company, "recent news")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "strategic" in results[0]["text"].lower()
        
        results = uipath_runner._generate_placeholder_results(company, "unknown aspect")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "unknown aspect" in results[0]["text"].lower()
    
    def test_simulate_automation_workflow(self, uipath_runner):
        """Test _simulate_automation_workflow method."""
        with patch('time.sleep'):
            with patch.object(uipath_runner, '_add_step') as mock_add_step:
                company_info = [{"text": "Test company info"}]
                news_info = [{"text": "Test news"}]
                financial_info = [{"text": "Test financials"}]
                competitor_info = [{"text": "Test competitors"}]
                
                uipath_runner._simulate_automation_workflow(
                    "Test Company", 
                    company_info, 
                    news_info, 
                    financial_info, 
                    competitor_info
                )
                
                assert mock_add_step.call_count == 4
    
    def test_generate_report(self, uipath_runner):
        """Test _generate_report method."""
        with patch('time.sleep'):
            company_info = [{"text": "Test company info"}]
            news_info = [{"text": "Test news"}]
            financial_info = [{"text": "Test financials"}]
            competitor_info = [{"text": "Test competitors"}]
            
            report = uipath_runner._generate_report(
                "Test Company", 
                company_info, 
                news_info, 
                financial_info, 
                competitor_info
            )
            
            assert "Test Company" in report
            assert "Test company info" in report
            assert "Test news" in report
            assert "Test financials" in report
            assert "Test competitors" in report
            assert "Automated Analysis Summary" in report
