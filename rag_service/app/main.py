import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exception_handlers import http_exception_handler
import time
import uuid

from ..logging_utils import LoggingMiddleware, log_event

app = FastAPI(
    title=os.getenv("API_TITLE", "RAG Service API"),
    description=os.getenv("API_DESCRIPTION", "Retrieval-Augmented Generation Service API"),
    version=os.getenv("API_VERSION", "1.0.0"),
    docs_url=os.getenv("API_DOCS_URL", "/docs"),
    redoc_url=os.getenv("API_REDOC_URL", "/redoc"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=bool(os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"),
    allow_methods=os.getenv("CORS_METHODS", "*").split(","),
    allow_headers=os.getenv("CORS_HEADERS", "*").split(","),
)

app.add_middleware(LoggingMiddleware)

from .api import app as api_app

for route in api_app.routes:
    app.routes.append(route)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for all unhandled exceptions.
    Logs the exception and returns a user-friendly error message.
    """
    request_id = str(uuid.uuid4())
    
    log_event(
        event_type="exception",
        message=f"Unhandled exception: {str(exc)}",
        level="error",
        details={
            "exception_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
        },
        request_id=request_id
    )
    
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "request_id": request_id,
            "timestamp": time.time()
        }
    )

@app.get("/", include_in_schema=False)
async def root():
    """
    Redirect to API documentation.
    """
    log_event(
        event_type="redirect",
        message="Root path redirected to docs",
        level="debug"
    )
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    log_event(
        event_type="health_check",
        message="Health check performed",
        level="debug"
    )
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": os.getenv("API_VERSION", "1.0.0")
    }

@app.get("/status")
def status():
    """
    Detailed status endpoint.
    """
    log_event(
        event_type="status_check",
        message="Status check performed",
        level="info"
    )
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_title": os.getenv("API_TITLE", "RAG Service API")
    }
