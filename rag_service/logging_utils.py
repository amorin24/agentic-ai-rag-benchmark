"""
Centralized logging utilities for the RAG service.

This module provides logging functions and middleware for consistent
logging across the application.
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from pathlib import Path
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_DIR = Path(os.getenv("LOG_DIR", "logs/rag_service"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("rag_service")
logger.setLevel(getattr(logging, LOG_LEVEL))

console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, LOG_LEVEL))
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(LOG_DIR / f"rag_service_{datetime.now().strftime('%Y%m%d')}.log")
file_handler.setLevel(getattr(logging, LOG_LEVEL))
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def log_event(
    event_type: str,
    message: str,
    level: str = "info",
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> None:
    """
    Log an event with standardized format.
    
    Args:
        event_type: Type of event (e.g., 'query', 'ingest', 'error')
        message: Log message
        level: Log level (info, warning, error, debug)
        details: Additional details to include in the log
        request_id: Optional request ID for tracking
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "message": message,
        "request_id": request_id,
        "details": details or {}
    }
    
    log_method = getattr(logger, level.lower())
    log_method(json.dumps(log_data))

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = f"req_{int(time.time() * 1000)}_{hash(request.url) % 10000:04d}"
        
        log_event(
            event_type="http_request",
            message=f"Request {request.method} {request.url.path}",
            level="info",
            details={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": request.client.host if request.client else None
            },
            request_id=request_id
        )
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time
            log_event(
                event_type="http_response",
                message=f"Response {response.status_code} for {request.method} {request.url.path}",
                level="info",
                details={
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time * 1000, 2)
                },
                request_id=request_id
            )
            
            return response
        except Exception as e:
            process_time = time.time() - start_time
            log_event(
                event_type="http_exception",
                message=f"Exception during {request.method} {request.url.path}: {str(e)}",
                level="error",
                details={
                    "exception": str(e),
                    "process_time_ms": round(process_time * 1000, 2)
                },
                request_id=request_id
            )
            raise
