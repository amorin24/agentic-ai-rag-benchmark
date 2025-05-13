"""
Unit tests for the Retriever component.
"""

import os
import json
import tempfile
import shutil
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from rag_service.retriever import Retriever, get_retriever, load_documents_from_processed_dir

class MockEmbedder:
    """Mock embedder for testing."""
    
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.embed_calls = []
    
    def embed_text(self, texts):
        """Mock embedding function that returns random vectors."""
        self.embed_calls.append(texts)
        if isinstance(texts, str):
            texts = [texts]
        return np.random.rand(len(texts), self.dimension).astype(np.float32)
    
    def get_dimension(self):
        """Return the embedding dimension."""
        return self.dimension
    
    def get_model_info(self):
        """Return mock model info."""
        return {
            "model_type": "mock",
            "model_name": "mock-embedder",
            "dimension": self.dimension
        }

class TestRetriever:
    """Test cases for the Retriever component."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_embedder(self):
        """Create a mock embedder for testing."""
        return MockEmbedder()
    
    @pytest.fixture
    def retriever(self, temp_dir, mock_embedder):
        """Create a retriever instance for testing."""
        with patch('rag_service.retriever.get_embedder', return_value=mock_embedder):
            with patch('rag_service.retriever.VECTOR_DIR', Path(temp_dir)):
                retriever = Retriever("test_index")
                yield retriever
    
    def test_initialization(self, retriever, temp_dir, mock_embedder):
        """Test retriever initialization."""
        assert retriever.index_name == "test_index"
        assert retriever.index_path == Path(temp_dir) / "test_index.index"
        assert retriever.metadata_path == Path(temp_dir) / "test_index.json"
        assert retriever.embedding_dim == mock_embedder.dimension
        assert len(retriever.doc_ids) == 0
        assert len(retriever.metadata) == 0
    
    def test_add_documents(self, retriever, mock_embedder):
        """Test adding documents to the retriever."""
        documents = [
            {
                "id": "doc1",
                "chunks": ["This is chunk 1", "This is chunk 2"],
                "metadata": {"source": "test", "author": "test_author"}
            },
            {
                "id": "doc2",
                "chunks": ["This is chunk 3"],
                "metadata": {"source": "test", "author": "another_author"}
            }
        ]
        
        with patch('rag_service.retriever.faiss.write_index'):
            num_chunks = retriever.add_documents(documents)
            
            assert num_chunks == 3
            assert len(retriever.doc_ids) == 3
            assert len(retriever.metadata) == 3
            assert retriever.doc_ids[0] == "doc1_0"
            assert retriever.doc_ids[1] == "doc1_1"
            assert retriever.doc_ids[2] == "doc2_0"
            assert retriever.metadata[0]["doc_id"] == "doc1"
            assert retriever.metadata[0]["chunk_index"] == 0
            assert retriever.metadata[0]["source"] == "test"
            assert retriever.metadata[0]["author"] == "test_author"
            assert retriever.metadata[0]["chunk_text"] == "This is chunk 1"
            assert "added_at" in retriever.metadata[0]
    
    def test_add_texts(self, retriever, mock_embedder):
        """Test adding raw texts to the retriever."""
        texts = ["Text 1", "Text 2", "Text 3"]
        metadatas = [
            {"source": "test1"},
            {"source": "test2"},
            {"source": "test3"}
        ]
        
        with patch('rag_service.retriever.faiss.write_index'):
            chunk_ids = retriever.add_texts(texts, metadatas)
            
            assert len(chunk_ids) == 3
            assert len(retriever.doc_ids) == 3
            assert len(retriever.metadata) == 3
            assert all(id.startswith("text_") for id in chunk_ids)
            assert retriever.metadata[0]["source"] == "test1"
            assert retriever.metadata[1]["source"] == "test2"
            assert retriever.metadata[2]["source"] == "test3"
            assert retriever.metadata[0]["chunk_text"] == "Text 1"
            assert retriever.metadata[1]["chunk_text"] == "Text 2"
            assert retriever.metadata[2]["chunk_text"] == "Text 3"
            assert all("added_at" in meta for meta in retriever.metadata)
    
    def test_search(self, retriever, mock_embedder):
        """Test searching for similar documents."""
        texts = ["Apple is a fruit", "Banana is yellow", "Orange is orange"]
        
        with patch('rag_service.retriever.faiss.write_index'):
            retriever.add_texts(texts)
        
        with patch.object(retriever.index, 'search') as mock_search:
            mock_search.return_value = (
                np.array([[0.1, 0.3]]),  # distances
                np.array([[0, 2]])       # indices
            )
            
            results = retriever.search("fruit", top_k=2)
            
            assert len(results) == 2
            assert results[0]["text"] == "Apple is a fruit"
            assert results[1]["text"] == "Orange is orange"
            assert results[0]["score"] > results[1]["score"]  # Lower distance = higher score
    
    def test_save_and_load_index(self, retriever, temp_dir):
        """Test saving and loading the index."""
        texts = ["Text 1", "Text 2", "Text 3"]
        
        with patch('rag_service.retriever.faiss.write_index'):
            retriever.add_texts(texts)
            
            index_path, metadata_path = retriever.save_index()
            
            assert index_path == str(Path(temp_dir) / "test_index.index")
            assert metadata_path == str(Path(temp_dir) / "test_index.json")
            
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file
                
                retriever.save_index()
                
                _, kwargs = mock_file.write.call_args
                metadata_str = kwargs.get('data', '')
                assert "test_index" in metadata_str
                assert "doc_ids" in metadata_str
                assert "metadata" in metadata_str
        
        with patch('rag_service.retriever.faiss.read_index'):
            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_open.return_value.__enter__.return_value = mock_file
                mock_file.read.return_value = json.dumps({
                    "name": "test_index",
                    "doc_ids": ["id1", "id2", "id3"],
                    "metadata": [{"text": "Text 1"}, {"text": "Text 2"}, {"text": "Text 3"}]
                })
                
                success = retriever.load_index()
                
                assert success
                assert len(retriever.doc_ids) == 3
                assert len(retriever.metadata) == 3
                assert retriever.doc_ids == ["id1", "id2", "id3"]
    
    def test_get_index_stats(self, retriever, mock_embedder):
        """Test getting index statistics."""
        texts = ["Text 1", "Text 2"]
        
        with patch('rag_service.retriever.faiss.write_index'):
            retriever.add_texts(texts)
        
        with patch('os.path.getmtime', return_value=1234567890):
            stats = retriever.get_index_stats()
            
            assert stats["name"] == "test_index"
            assert stats["size"] == 2
            assert stats["embedding_model"]["model_type"] == "mock"
            assert stats["embedding_model"]["model_name"] == "mock-embedder"
            assert stats["embedding_model"]["dimension"] == mock_embedder.dimension
    
    def test_clear_index(self, retriever):
        """Test clearing the index."""
        texts = ["Text 1", "Text 2", "Text 3"]
        
        with patch('rag_service.retriever.faiss.write_index'):
            retriever.add_texts(texts)
            assert len(retriever.doc_ids) == 3
            
            retriever.clear_index()
            
            assert len(retriever.doc_ids) == 0
            assert len(retriever.metadata) == 0
    
    def test_get_retriever_factory(self, mock_embedder):
        """Test the get_retriever factory function."""
        with patch('rag_service.retriever.Retriever') as mock_retriever_class:
            mock_retriever_class.return_value = "mock_retriever_instance"
            
            with patch('rag_service.retriever.get_embedder', return_value=mock_embedder):
                retriever = get_retriever("test_index", "sentence-transformer")
                
                mock_retriever_class.assert_called_once_with("test_index", "sentence-transformer")
                assert retriever == "mock_retriever_instance"
    
    def test_load_documents_from_processed_dir(self, temp_dir):
        """Test loading documents from the processed directory."""
        processed_dir = Path(temp_dir) / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        doc1 = {"id": "doc1", "chunks": ["Chunk 1"], "metadata": {"source": "test1"}}
        doc2 = {"id": "doc2", "chunks": ["Chunk 2"], "metadata": {"source": "test2"}}
        
        with open(processed_dir / "doc1.json", "w") as f:
            json.dump(doc1, f)
        
        with open(processed_dir / "doc2.json", "w") as f:
            json.dump(doc2, f)
        
        with patch('rag_service.retriever.PROCESSED_DIR', processed_dir):
            documents = load_documents_from_processed_dir()
            
            assert len(documents) == 2
            assert any(doc["id"] == "doc1" for doc in documents)
            assert any(doc["id"] == "doc2" for doc in documents)
            assert any(doc["metadata"]["source"] == "test1" for doc in documents)
            assert any(doc["metadata"]["source"] == "test2" for doc in documents)
    
    def test_error_handling_in_load_index(self, retriever):
        """Test error handling when loading the index."""
        with patch('rag_service.retriever.faiss.read_index', side_effect=Exception("Test error")):
            success = retriever.load_index()
            
            assert not success
            assert len(retriever.doc_ids) == 0
            assert len(retriever.metadata) == 0
