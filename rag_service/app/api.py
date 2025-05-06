import os
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl
from fastapi import FastAPI, HTTPException, Query
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI(title="RAG Service API")

model = SentenceTransformer('all-MiniLM-L6-v2')

embedding_size = 384  # Size of embeddings from all-MiniLM-L6-v2
index = faiss.IndexFlatL2(embedding_size)

chunks = []
metadata = []
last_ingest_time = None

class IngestTextRequest(BaseModel):
    text: str
    metadata: Optional[Dict] = Field(default_factory=dict)

class IngestUrlRequest(BaseModel):
    url: HttpUrl
    metadata: Optional[Dict] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    query: str
    results: List[Dict]
    total_chunks: int
    time_taken: float

class StatusResponse(BaseModel):
    status: str
    vector_store_size: int
    last_ingest: Optional[str] = None

def extract_text_from_url(url: str) -> str:
    """Extract text content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from URL: {str(e)}")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text) and text[end] != ' ':
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        
        chunks.append(text[start:end])
        start = end - overlap if end - overlap > start else end
    
    return chunks

@app.post("/ingest")
async def ingest(request: Union[IngestTextRequest, IngestUrlRequest]):
    """
    Ingest text or URL content into the vector store.
    """
    global last_ingest_time
    
    if hasattr(request, 'url'):
        text = extract_text_from_url(str(request.url))
        source = str(request.url)
    else:
        text = request.text
        source = "direct_input"
    
    request_metadata = request.metadata or {}
    request_metadata['source'] = source
    
    text_chunks = chunk_text(text)
    
    for chunk in text_chunks:
        embedding = model.encode([chunk])[0]
        
        faiss.normalize_L2(np.array([embedding], dtype=np.float32))
        index.add(np.array([embedding], dtype=np.float32))
        
        chunks.append(chunk)
        metadata.append(request_metadata)
    
    last_ingest_time = datetime.now().isoformat()
    
    return {
        "status": "success",
        "chunks_ingested": len(text_chunks),
        "vector_store_size": len(chunks)
    }

@app.get("/query", response_model=QueryResponse)
async def query(q: str = Query(..., description="Query string"), 
                top_k: int = Query(5, description="Number of results to return")):
    """
    Query the vector store for relevant chunks.
    """
    start_time = time.time()
    
    if not chunks:
        raise HTTPException(status_code=400, detail="Vector store is empty. Ingest some data first.")
    
    query_embedding = model.encode([q])[0]
    faiss.normalize_L2(np.array([query_embedding], dtype=np.float32))
    
    top_k = min(top_k, len(chunks))  # Ensure we don't request more than available
    distances, indices = index.search(np.array([query_embedding], dtype=np.float32), top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # FAISS returns -1 for padded results
            results.append({
                "chunk": chunks[idx],
                "metadata": metadata[idx],
                "score": float(1.0 / (1.0 + distances[0][i]))  # Convert distance to similarity score
            })
    
    time_taken = time.time() - start_time
    
    return {
        "query": q,
        "results": results,
        "total_chunks": len(chunks),
        "time_taken": time_taken
    }

@app.get("/status", response_model=StatusResponse)
async def status():
    """
    Return the status of the vector store.
    """
    return {
        "status": "healthy",
        "vector_store_size": len(chunks),
        "last_ingest": last_ingest_time
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
