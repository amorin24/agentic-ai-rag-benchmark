from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="RAG Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    documents: List[Document]
    query: str

class IngestRequest(BaseModel):
    documents: List[Document]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Retrieve relevant documents based on a query.
    """
    documents = [
        Document(
            content="This is a placeholder document.",
            metadata={"source": "placeholder"}
        )
    ]
    
    return QueryResponse(documents=documents, query=request.query)

@app.post("/ingest")
async def ingest_documents(request: IngestRequest):
    """
    Add new documents to the knowledge base.
    """
    return {"status": "success", "documents_ingested": len(request.documents)}
