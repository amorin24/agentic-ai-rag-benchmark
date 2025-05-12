"""
Unit tests for the H2O AI runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from agents.h2oai.runner import H2OAIRunner

class TestH2OAIRunner:
    """Test cases for the H2O AI runner."""
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests module for testing."""
        with patch('agents.h2oai.runner.requests') as mock_requests:
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
    def h2oai_runner(self):
        """Create a H2O AI runner instance for testing."""
        return H2OAIRunner("http://localhost:8000")
    
    def test_initialization(self, h2oai_runner):
        """Test H2O AI runner initialization."""
        assert h2oai_runner.agent_name == "h2oai"
        assert h2oai_runner.rag_service_url == "http://localhost:8000"
    
    def test_run_task(self, h2oai_runner, mock_requests):
        """Test run_task method."""
        with patch('time.sleep'):  # Mock sleep to speed up tests
            result = h2oai_runner.run_task("Test Company")
            
            assert result["agent_name"] == "h2oai"
            assert "Test Company" in result["final_output"]
            assert len(result["steps"]) > 0
            assert result["token_usage"] > 0
            assert isinstance(result["response_time"], float)
    
    def test_query_rag_service_success(self, h2oai_runner, mock_requests):
        """Test _query_rag_service method with successful response."""
        results = h2oai_runner._query_rag_service("Test Company", "company overview")
        
        assert len(results) == 1
        assert results[0]["text"] == "Test company information"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["score"] == 0.95
        
        mock_requests.get.assert_called_once_with(
            "http://localhost:8000/query",
            params={"q": "Test Company company overview", "top_k": 3}
        )
    
    def test_query_rag_service_error(self, h2oai_runner):
        """Test _query_rag_service method with error response."""
        with patch('agents.h2oai.runner.requests.get') as mock_get:
            mock_get.side_effect = Exception("Test error")
            
            results = h2oai_runner._query_rag_service("Test Company", "company overview")
            
            assert len(results) == 1
            assert "Test Company" in results[0]["text"]
            assert results[0]["metadata"]["source"] == "simulated"
    
    def test_generate_placeholder_results(self, h2oai_runner):
        """Test _generate_placeholder_results method."""
        company = "Test Company"
        
        results = h2oai_runner._generate_placeholder_results(company, "company overview")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert results[0]["metadata"]["source"] == "simulated"
        
        results = h2oai_runner._generate_placeholder_results(company, "financial performance")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "growth" in results[0]["text"].lower()
        
        results = h2oai_runner._generate_placeholder_results(company, "unknown aspect")
        assert len(results) == 1
        assert company in results[0]["text"]
        assert "unknown aspect" in results[0]["text"].lower()
    
    def test_simulate_predictive_analytics(self, h2oai_runner):
        """Test _simulate_predictive_analytics method."""
        with patch('time.sleep'):
            with patch.object(h2oai_runner, '_add_step') as mock_add_step:
                company_info = [{"text": "Test company info"}]
                financial_info = [{"text": "Test financials"}]
                product_info = [{"text": "Test products"}]
                forecast_info = [{"text": "Test forecast"}]
                
                h2oai_runner._simulate_predictive_analytics(
                    "Test Company", 
                    company_info, 
                    financial_info, 
                    product_info, 
                    forecast_info
                )
                
                assert mock_add_step.call_count == 4
    
    def test_generate_report(self, h2oai_runner):
        """Test _generate_report method."""
        with patch('time.sleep'):
            company_info = [{"text": "Test company info"}]
            financial_info = [{"text": "Test financials"}]
            product_info = [{"text": "Test products"}]
            forecast_info = [{"text": "Test forecast"}]
            
            report = h2oai_runner._generate_report(
                "Test Company", 
                company_info, 
                financial_info, 
                product_info, 
                forecast_info
            )
            
            assert "Test Company" in report
            assert "Test company info" in report
            assert "Test financials" in report
            assert "Test products" in report
            assert "Test forecast" in report
            assert "Predictive Analytics Insights" in report
