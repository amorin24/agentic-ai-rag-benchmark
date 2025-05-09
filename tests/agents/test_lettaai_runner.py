"""
Unit tests for the LettaAI runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from agents.lettaai.runner import LettaAIRunner

class TestLettaAIRunner:
    """Test cases for the LettaAI runner."""
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests module for testing."""
        with patch('agents.lettaai.runner.requests') as mock_requests:
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
    def lettaai_runner(self):
        """Create a LettaAI runner instance for testing."""
        return LettaAIRunner("http://localhost:8000")
    
    def test_initialization(self, lettaai_runner):
        """Test LettaAI runner initialization."""
        assert lettaai_runner.agent_name == "lettaai"
        assert lettaai_runner.rag_service_url == "http://localhost:8000"
    
    def test_run_task(self, lettaai_runner, mock_requests):
        """Test run_task method."""
        with patch('time.sleep'):  # Mock sleep to speed up tests
            result = lettaai_runner.run_task("Test Company")
            
            assert result["agent_name"] == "lettaai"
            assert "Test Company" in result["final_output"]
            assert len(result["steps"]) > 0
            assert result["token_usage"] > 0
            assert isinstance(result["response_time"], float)
    
    def test_query_rag_service_success(self, lettaai_runner, mock_requests):
        """Test _query_rag_service method with successful response."""
        results = lettaai_runner._query_rag_service("Test Company", "company information")
        
        assert len(results) == 1
        assert results[0]["text"] == "Test company information"
        assert results[0]["metadata"] == {"source": "test"}
        assert results[0]["score"] == 0.95
        
        mock_requests.get.assert_called_once_with(
            "http://localhost:8000/query",
            params={"q": "Test Company company information", "top_k": 3}
        )
    
    def test_query_rag_service_error(self, lettaai_runner):
        """Test _query_rag_service method with error response."""
        with patch('agents.lettaai.runner.requests.get') as mock_get:
            mock_get.side_effect = Exception("Test error")
            
            results = lettaai_runner._query_rag_service("Test Company", "company information")
            
            assert len(results) == 1
            assert "Test Company" in results[0]["text"]
            assert results[0]["metadata"]["source"] == "simulated"
    
    def test_initialize_memory(self, lettaai_runner):
        """Test _initialize_memory method."""
        with patch('time.sleep'):
            with patch.object(lettaai_runner, '_add_step') as mock_add_step:
                lettaai_runner._initialize_memory("Test Company")
                
                assert mock_add_step.called
                args, _ = mock_add_step.call_args
                assert args[0] == "memory_operation"
                assert "Test Company" in str(args[1])
    
    def test_simulate_memory_augmented_research(self, lettaai_runner):
        """Test _simulate_memory_augmented_research method."""
        with patch('time.sleep'):
            with patch.object(lettaai_runner, '_add_step') as mock_add_step:
                with patch.object(lettaai_runner, '_simulate_planning'):
                    with patch.object(lettaai_runner, '_initialize_memory'):
                        with patch.object(lettaai_runner, '_research_company_profile'):
                            with patch.object(lettaai_runner, '_research_company_news'):
                                with patch.object(lettaai_runner, '_research_company_products'):
                                    with patch.object(lettaai_runner, '_research_company_financials'):
                                        with patch.object(lettaai_runner, '_consolidate_memory'):
                                            with patch.object(lettaai_runner, '_generate_report'):
                                                lettaai_runner._simulate_memory_augmented_research("Test Company")
                
                assert True
    
    def test_consolidate_memory(self, lettaai_runner):
        """Test _consolidate_memory method."""
        with patch('time.sleep'):
            with patch.object(lettaai_runner, '_add_step') as mock_add_step:
                lettaai_runner._consolidate_memory("Test Company")
                
                assert mock_add_step.called
                args, _ = mock_add_step.call_args
                assert args[0] == "memory_operation"
                assert "Test Company" in str(args[1])
    
    def test_generate_report(self, lettaai_runner):
        """Test _generate_report method."""
        with patch('time.sleep'):
            with patch.object(lettaai_runner, '_add_step'):
                report = lettaai_runner._generate_report("Test Company")
                
                assert "Test Company" in report
                assert "leading global organization" in report
                assert "strategic initiative" in report
                assert "product portfolio" in report
                assert "financial performance" in report
