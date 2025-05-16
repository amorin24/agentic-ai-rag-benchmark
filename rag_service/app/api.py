import os
import time
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl
from fastapi import FastAPI, HTTPException, Query, Request
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import uvicorn
import uuid

from ..logging_utils import log_event

app = FastAPI(title="RAG Service API")

model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
model = SentenceTransformer(model_name)

embedding_size = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(embedding_size)

chunks = []
metadata = []
last_ingest_time = None

log_event(
    event_type="initialization",
    message=f"RAG Service initialized with model: {model_name}",
    level="info",
    details={
        "embedding_size": embedding_size,
        "model": model_name,
        "vector_store": "FAISS"
    }
)

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
    request_id = str(uuid.uuid4())
    
    log_event(
        event_type="url_extraction",
        message=f"Extracting text from URL: {url}",
        level="info",
        details={"url": url},
        request_id=request_id
    )
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        log_event(
            event_type="url_extraction",
            message=f"Successfully fetched URL: {url}",
            level="debug",
            details={"status_code": response.status_code, "content_length": len(response.text)},
            request_id=request_id
        )
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        log_event(
            event_type="url_extraction",
            message=f"Text extracted from URL: {url}",
            level="debug",
            details={"text_length": len(text), "url": url},
            request_id=request_id
        )
        
        return text
    except Exception as e:
        log_event(
            event_type="url_extraction_error",
            message=f"Failed to extract text from URL: {url}",
            level="error",
            details={"error": str(e), "url": url},
            request_id=request_id
        )
        raise HTTPException(status_code=400, detail=f"Failed to extract text from URL: {str(e)}")

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """Split text into overlapping chunks."""
    chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", "1000"))
    overlap = overlap or int(os.getenv("CHUNK_OVERLAP", "200"))
    
    log_event(
        event_type="text_chunking",
        message=f"Chunking text of length {len(text)}",
        level="debug",
        details={
            "text_length": len(text),
            "chunk_size": chunk_size,
            "overlap": overlap
        }
    )
    
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
    
    log_event(
        event_type="text_chunking",
        message=f"Text chunked into {len(chunks)} chunks",
        level="debug",
        details={
            "chunk_count": len(chunks),
            "average_chunk_size": sum(len(c) for c in chunks) / len(chunks) if chunks else 0
        }
    )
    
    return chunks

@app.post("/ingest")
async def ingest(request: Union[IngestTextRequest, IngestUrlRequest], req: Request):
    """
    Ingest text or URL content into the vector store.
    """
    global last_ingest_time
    request_id = str(uuid.uuid4())
    
    log_event(
        event_type="ingest_request",
        message="Received ingest request",
        level="info",
        details={
            "request_type": "url" if hasattr(request, 'url') else "text",
            "client_host": req.client.host if req.client else None,
            "metadata": request.metadata
        },
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        if hasattr(request, 'url'):
            text = extract_text_from_url(str(request.url))
            source = str(request.url)
        else:
            text = request.text
            source = "direct_input"
        
        request_metadata = request.metadata or {}
        request_metadata['source'] = source
        request_metadata['ingest_time'] = datetime.now().isoformat()
        request_metadata['request_id'] = request_id
        
        text_chunks = chunk_text(text)
        
        log_event(
            event_type="ingest_processing",
            message=f"Processing {len(text_chunks)} chunks for ingestion",
            level="info",
            details={
                "chunk_count": len(text_chunks),
                "source": source,
                "text_length": len(text)
            },
            request_id=request_id
        )
        
        for chunk in text_chunks:
            embedding = model.encode([chunk])[0]
            
            faiss.normalize_L2(np.array([embedding], dtype=np.float32))
            index.add(np.array([embedding], dtype=np.float32))
            
            chunks.append(chunk)
            metadata.append(request_metadata)
        
        last_ingest_time = datetime.now().isoformat()
        
        process_time = time.time() - start_time
        
        log_event(
            event_type="ingest_complete",
            message="Ingest operation completed successfully",
            level="info",
            details={
                "chunks_ingested": len(text_chunks),
                "vector_store_size": len(chunks),
                "process_time_ms": round(process_time * 1000, 2),
                "source": source
            },
            request_id=request_id
        )
        
        return {
            "status": "success",
            "chunks_ingested": len(text_chunks),
            "vector_store_size": len(chunks),
            "process_time_ms": round(process_time * 1000, 2),
            "request_id": request_id
        }
    except Exception as e:
        process_time = time.time() - start_time
        
        log_event(
            event_type="ingest_error",
            message=f"Error during ingest operation: {str(e)}",
            level="error",
            details={
                "error": str(e),
                "process_time_ms": round(process_time * 1000, 2),
                "source": source if 'source' in locals() else None
            },
            request_id=request_id
        )
        
        if isinstance(e, HTTPException):
            raise e
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Ingest operation failed",
                "message": str(e),
                "request_id": request_id
            }
        )

@app.get("/query", response_model=QueryResponse)
async def query(
    q: str = Query(..., description="Query string"), 
    top_k: int = Query(None, description="Number of results to return"),
    req: Request = None
):
    """
    Query the vector store for relevant chunks.
    """
    request_id = str(uuid.uuid4())
    top_k = top_k or int(os.getenv("DEFAULT_TOP_K", "5"))
    
    log_event(
        event_type="query_request",
        message=f"Received query request: '{q}'",
        level="info",
        details={
            "query": q,
            "top_k": top_k,
            "client_host": req.client.host if req and req.client else None
        },
        request_id=request_id
    )
    
    start_time = time.time()
    
    try:
        if not chunks:
            log_event(
                event_type="query_error",
                message="Query failed: Vector store is empty",
                level="warning",
                details={"query": q},
                request_id=request_id
            )
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "Vector store is empty",
                    "message": "Ingest some data first before querying",
                    "request_id": request_id
                }
            )
        
        query_embedding = model.encode([q])[0]
        faiss.normalize_L2(np.array([query_embedding], dtype=np.float32))
        
        top_k = min(top_k, len(chunks))  # Ensure we don't request more than available
        distances, indices = index.search(np.array([query_embedding], dtype=np.float32), top_k)
        
        log_event(
            event_type="query_search",
            message=f"FAISS search completed for query: '{q}'",
            level="debug",
            details={
                "top_k": top_k,
                "results_found": len([i for i in indices[0] if i != -1])
            },
            request_id=request_id
        )
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS returns -1 for padded results
                score = float(1.0 / (1.0 + distances[0][i]))  # Convert distance to similarity score
                results.append({
                    "chunk": chunks[idx],
                    "metadata": metadata[idx],
                    "score": score
                })
        
        time_taken = time.time() - start_time
        
        log_event(
            event_type="query_complete",
            message=f"Query completed successfully: '{q}'",
            level="info",
            details={
                "query": q,
                "results_count": len(results),
                "process_time_ms": round(time_taken * 1000, 2),
                "top_score": results[0]["score"] if results else None
            },
            request_id=request_id
        )
        
        return {
            "query": q,
            "results": results,
            "total_chunks": len(chunks),
            "time_taken": time_taken,
            "request_id": request_id
        }
    except Exception as e:
        if not isinstance(e, HTTPException):
            time_taken = time.time() - start_time
            
            log_event(
                event_type="query_error",
                message=f"Error during query operation: {str(e)}",
                level="error",
                details={
                    "query": q,
                    "error": str(e),
                    "process_time_ms": round(time_taken * 1000, 2)
                },
                request_id=request_id
            )
            
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Query operation failed",
                    "message": str(e),
                    "request_id": request_id
                }
            )
        raise e

@app.get("/status", response_model=StatusResponse)
async def status(req: Request = None):
    """
    Return the status of the vector store.
    """
    log_event(
        event_type="status_request",
        message="Vector store status requested",
        level="debug",
        details={
            "vector_store_size": len(chunks),
            "client_host": req.client.host if req and req.client else None
        }
    )
    
    return {
        "status": "healthy",
        "vector_store_size": len(chunks),
        "last_ingest": last_ingest_time
    }

@app.get("/config")
async def get_config():
    """
    Return the current configuration of the RAG service.
    """
    log_event(
        event_type="config_request",
        message="Configuration requested",
        level="debug"
    )
    
    return {
        "embedding_model": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        "embedding_size": embedding_size,
        "chunk_size": int(os.getenv("CHUNK_SIZE", "1000")),
        "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", "200")),
        "default_top_k": int(os.getenv("DEFAULT_TOP_K", "5")),
        "vector_store_type": "FAISS",
        "api_version": os.getenv("API_VERSION", "1.0.0")
    }

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    log_event(
        event_type="server_start",
        message=f"Starting RAG service on {host}:{port}",
        level="info",
        details={
            "host": host,
            "port": port,
            "embedding_model": os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        }
    )
    
    uvicorn.run(app, host=host, port=port)
