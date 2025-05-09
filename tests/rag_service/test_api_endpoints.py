import pytest
import faiss
from fastapi.testclient import TestClient
from rag_service.app.api import app

client = TestClient(app)

def test_status_endpoint():
    """Test the status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "vector_store_size" in data
    assert "last_ingest" in data
    assert data["status"] == "healthy"

def test_ingest_text_endpoint():
    """Test ingesting text."""
    response = client.post(
        "/ingest",
        json={"text": "This is a test document for the RAG service.", "metadata": {"source": "test"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "chunks_ingested" in data
    assert "vector_store_size" in data
    assert data["status"] == "success"
    assert data["chunks_ingested"] >= 1

def test_ingest_url_endpoint():
    """Test ingesting from URL."""
    response = client.post(
        "/ingest",
        json={"url": "https://example.com", "metadata": {"source_type": "web"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "chunks_ingested" in data
    assert "vector_store_size" in data
    assert data["status"] == "success"
    assert data["chunks_ingested"] >= 1

def test_query_endpoint():
    """Test the query endpoint."""
    client.post(
        "/ingest",
        json={"text": "Artificial intelligence is transforming how we work and live.", "metadata": {"topic": "AI"}}
    )
    
    response = client.get("/query?q=artificial%20intelligence&top_k=2")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert "total_chunks" in data
    assert "time_taken" in data
    assert data["query"] == "artificial intelligence"
    assert len(data["results"]) > 0
    assert "chunk" in data["results"][0]
    assert "metadata" in data["results"][0]
    assert "score" in data["results"][0]

def test_query_empty_store():
    """Test querying an empty vector store."""
    from rag_service.app.api import app as fresh_app
    import rag_service.app.api as api_module
    api_module.chunks = []
    api_module.metadata = []
    api_module.index = faiss.IndexFlatL2(api_module.embedding_size)
    
    fresh_client = TestClient(fresh_app)
    
    response = fresh_client.get("/query?q=test%20query")
    assert response.status_code == 400
    assert "Vector store is empty" in response.json()["detail"]
