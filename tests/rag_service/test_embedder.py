"""
Unit tests for the Embedder component.
"""

import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from rag_service.embedder import Embedder, get_embedder

class TestEmbedder:
    """Test cases for the Embedder component."""
    
    @pytest.fixture
    def mock_sentence_transformer(self):
        """Mock SentenceTransformer for testing."""
        with patch('rag_service.embedder.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_model.get_sentence_embedding_dimension.return_value = 384
            mock_model.encode.return_value = np.random.rand(2, 384).astype(np.float32)
            mock_st.return_value = mock_model
            yield mock_st
    
    @pytest.fixture
    def mock_openai(self):
        """Mock OpenAI API for testing."""
        with patch('rag_service.embedder.openai') as mock_openai:
            mock_openai.Embedding.create.return_value = {
                "data": [
                    {"embedding": list(np.random.rand(1536))},
                    {"embedding": list(np.random.rand(1536))}
                ]
            }
            yield mock_openai
    
    def test_initialization_sentence_transformer(self, mock_sentence_transformer):
        """Test embedder initialization with sentence transformer."""
        embedder = Embedder('sentence-transformer')
        
        assert embedder.model_type == 'sentence-transformer'
        assert embedder.dimension == 384
        mock_sentence_transformer.assert_called_once_with('all-MiniLM-L6-v2')
    
    def test_initialization_openai(self, mock_openai):
        """Test embedder initialization with OpenAI."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            embedder = Embedder('openai')
            
            assert embedder.model_type == 'openai'
            assert embedder.dimension == 1536
    
    def test_initialization_openai_fallback(self, mock_sentence_transformer):
        """Test embedder initialization with OpenAI fallback to sentence transformer."""
        with patch('rag_service.embedder.openai', side_effect=ImportError):
            embedder = Embedder('openai')
            
            assert embedder.model_type == 'sentence-transformer'
            assert embedder.dimension == 384
    
    def test_initialization_default(self, mock_sentence_transformer):
        """Test embedder initialization with default model type."""
        with patch('rag_service.embedder.DEFAULT_EMBEDDING_MODEL', 'sentence-transformer'):
            embedder = Embedder()
            
            assert embedder.model_type == 'sentence-transformer'
            assert embedder.dimension == 384
    
    def test_embed_text_sentence_transformer(self, mock_sentence_transformer):
        """Test embedding text with sentence transformer."""
        embedder = Embedder('sentence-transformer')
        
        single_embedding = embedder.embed_text("Test text")
        assert isinstance(single_embedding, np.ndarray)
        assert single_embedding.shape[0] == 2  # Our mock returns 2 embeddings
        assert single_embedding.shape[1] == 384
        
        texts = ["Text 1", "Text 2"]
        embeddings = embedder.embed_text(texts)
        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] == 384
        
        embedder.model.encode.assert_called_with(texts, convert_to_numpy=True)
    
    def test_embed_text_openai(self, mock_openai):
        """Test embedding text with OpenAI."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            embedder = Embedder('openai')
            
            texts = ["Text 1", "Text 2"]
            embeddings = embedder.embed_text(texts)
            
            assert isinstance(embeddings, np.ndarray)
            assert embeddings.shape[0] == 2
            assert embeddings.shape[1] == 1536
            
            mock_openai.Embedding.create.assert_called_with(
                input=texts,
                model='text-embedding-ada-002'
            )
    
    def test_embed_text_openai_batching(self, mock_openai):
        """Test embedding text with OpenAI batching."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            embedder = Embedder('openai')
            
            texts = [f"Text {i}" for i in range(1500)]
            
            with patch.object(embedder, '_embed_with_openai', wraps=embedder._embed_with_openai) as mock_embed:
                embeddings = embedder.embed_text(texts)
                
                assert mock_embed.call_count == 1
                
                assert mock_openai.Embedding.create.call_count == 2
                
                first_call_args = mock_openai.Embedding.create.call_args_list[0][1]
                second_call_args = mock_openai.Embedding.create.call_args_list[1][1]
                
                assert len(first_call_args['input']) == 1000
                assert len(second_call_args['input']) == 500
    
    def test_embed_text_error_handling(self, mock_sentence_transformer):
        """Test error handling when embedding text."""
        embedder = Embedder('sentence-transformer')
        
        embedder.model.encode.side_effect = Exception("Test error")
        
        with pytest.raises(Exception) as excinfo:
            embedder.embed_text("Test text")
        
        assert "Test error" in str(excinfo.value)
    
    def test_get_dimension(self, mock_sentence_transformer):
        """Test getting the embedding dimension."""
        embedder = Embedder('sentence-transformer')
        
        assert embedder.get_dimension() == 384
    
    def test_get_model_info(self, mock_sentence_transformer):
        """Test getting model information."""
        embedder = Embedder('sentence-transformer')
        
        model_info = embedder.get_model_info()
        
        assert model_info["model_type"] == "sentence-transformer"
        assert model_info["model_name"] == "all-MiniLM-L6-v2"
        assert model_info["dimension"] == 384
    
    def test_get_embedder_factory(self, mock_sentence_transformer):
        """Test the get_embedder factory function."""
        with patch('rag_service.embedder.Embedder') as mock_embedder_class:
            mock_embedder_class.return_value = "mock_embedder_instance"
            
            embedder = get_embedder("sentence-transformer")
            
            mock_embedder_class.assert_called_once_with("sentence-transformer")
            assert embedder == "mock_embedder_instance"
