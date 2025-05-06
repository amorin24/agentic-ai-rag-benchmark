import requests
from typing import List, Dict, Any

class RAGClient:
    """
    Client for interacting with the RAG service.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the RAG client.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        self.rag_service_url = rag_service_url
        
    def query(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the RAG service for relevant documents.
        
        Args:
            query: The query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents
        """
        response = requests.post(
            f"{self.rag_service_url}/query",
            json={"query": query, "top_k": top_k}
        )
        
        if response.status_code != 200:
            raise Exception(f"RAG service query failed: {response.text}")
            
        return response.json()["documents"]
    
    def ingest(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ingest documents into the RAG service.
        
        Args:
            documents: List of documents to ingest
            
        Returns:
            Response from the RAG service
        """
        response = requests.post(
            f"{self.rag_service_url}/ingest",
            json={"documents": documents}
        )
        
        if response.status_code != 200:
            raise Exception(f"RAG service ingestion failed: {response.text}")
            
        return response.json()
