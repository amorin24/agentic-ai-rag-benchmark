import pytest
from fastapi.testclient import TestClient
from rag_service.app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_query_endpoint():
    """Test the query endpoint."""
    response = client.post(
        "/query",
        json={"query": "test query", "top_k": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "query" in data
    assert data["query"] == "test query"

def test_ingest_endpoint():
    """Test the ingest endpoint."""
    response = client.post(
        "/ingest",
        json={"documents": [
            {"content": "test document", "metadata": {"source": "test"}}
        ]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
    assert "documents_ingested" in data
    assert data["documents_ingested"] == 1
