"""
Integration tests for the RAG service and agent components.
"""

import os
import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from rag_service.retriever import Retriever, get_retriever
from rag_service.embedder import get_embedder
from agents.base_agent_runner import BaseAgentRunner
from agents.autogen.runner import AutoGenRunner
from agents.crewai.runner import CrewAIRunner

class TestRAGIntegration:
    """Integration tests between RAG service and agent components."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_embedder(self):
        """Create a mock embedder for testing."""
        with patch('rag_service.embedder.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_model.get_sentence_embedding_dimension.return_value = 384
            mock_model.encode.return_value = pytest.approx(
                [[0.1, 0.2, 0.3] + [0.0] * 381],
                [[0.2, 0.3, 0.4] + [0.0] * 381],
                [[0.3, 0.4, 0.5] + [0.0] * 381]
            )
            mock_st.return_value = mock_model
            
            embedder = get_embedder('sentence-transformer')
            yield embedder
    
    @pytest.fixture
    def test_retriever(self, temp_dir, mock_embedder):
        """Create a test retriever with mock embedder."""
        with patch('rag_service.retriever.VECTOR_DIR', Path(temp_dir)):
            with patch('rag_service.retriever.get_embedder', return_value=mock_embedder):
                retriever = get_retriever("test_integration")
                
                texts = [
                    "Apple Inc. is a technology company that makes iPhones and Macs.",
                    "Microsoft Corporation develops Windows and Office software.",
                    "Google is known for its search engine and Android operating system."
                ]
                
                metadatas = [
                    {"company": "Apple", "industry": "Technology"},
                    {"company": "Microsoft", "industry": "Technology"},
                    {"company": "Google", "industry": "Technology"}
                ]
                
                retriever.add_texts(texts, metadatas)
                yield retriever
    
    @pytest.fixture
    def mock_requests(self):
        """Mock requests for testing agent runners."""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [
                    {
                        "chunk": "Apple Inc. is a technology company that makes iPhones and Macs.",
                        "metadata": {"company": "Apple", "industry": "Technology"},
                        "score": 0.95
                    },
                    {
                        "chunk": "Microsoft Corporation develops Windows and Office software.",
                        "metadata": {"company": "Microsoft", "industry": "Technology"},
                        "score": 0.85
                    }
                ],
                "query": "Apple company information",
                "total_chunks": 3,
                "time_taken": 0.05
            }
            mock_get.return_value = mock_response
            yield mock_get
    
    def test_retriever_embedder_integration(self, test_retriever, mock_embedder):
        """Test integration between retriever and embedder."""
        results = test_retriever.search("Apple company")
        
        assert len(results) > 0
        assert "Apple" in results[0]["text"]
        assert results[0]["metadata"]["company"] == "Apple"
        
        assert mock_embedder.model.encode.call_count > 0
    
    def test_agent_rag_integration(self, mock_requests):
        """Test integration between agent and RAG service."""
        agent = AutoGenRunner("http://localhost:8000")
        
        with patch('time.sleep'):  # Speed up tests by not waiting
            result = agent.run_task("Apple")
        
        mock_requests.assert_called_with(
            "http://localhost:8000/query",
            params={"q": "Apple company information", "top_k": 3}
        )
        
        assert "Apple" in result["final_output"]
        assert result["agent_name"] == "autogen"
        assert len(result["steps"]) > 0
    
    def test_multiple_agents_same_rag(self, mock_requests):
        """Test multiple agents using the same RAG service."""
        autogen_agent = AutoGenRunner("http://localhost:8000")
        crewai_agent = CrewAIRunner("http://localhost:8000")
        
        with patch('time.sleep'):  # Speed up tests by not waiting
            autogen_result = autogen_agent.run_task("Apple")
            crewai_result = crewai_agent.run_task("Apple")
        
        assert mock_requests.call_count >= 2
        
        assert "Apple" in autogen_result["final_output"]
        assert "Apple" in crewai_result["final_output"]
        assert autogen_result["agent_name"] == "autogen"
        assert crewai_result["agent_name"] == "crewai"
    
    def test_error_handling_integration(self, mock_requests):
        """Test error handling integration between agent and RAG service."""
        agent = AutoGenRunner("http://localhost:8000")
        
        mock_requests.return_value.status_code = 500
        
        with patch('time.sleep'):  # Speed up tests by not waiting
            result = agent.run_task("Apple")
        
        assert "Apple" in result["final_output"]
        assert result["agent_name"] == "autogen"
        assert len(result["steps"]) > 0
        
        error_steps = [step for step in result["steps"] if step["type"] == "error"]
        assert len(error_steps) > 0
        assert "RAG service returned status code 500" in error_steps[0]["data"]["message"]
        
        for step in result["steps"]:
            if step["type"] == "rag_results":
                for item in step["data"]["results"]:
                    assert item["metadata"].get("simulated") is True
