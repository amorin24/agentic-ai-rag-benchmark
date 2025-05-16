"""
Agent Runner API Service.

This module provides a FastAPI application for running agent tasks
with centralized logging and error handling.
"""

import os
import time
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from fastapi import FastAPI, HTTPException, Query, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_DIR = os.path.join(os.getenv("LOG_DIR", "logs"), "agent_runner")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("agent_runner_api")
logger.setLevel(getattr(logging, LOG_LEVEL))

console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, LOG_LEVEL))
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, f"agent_runner_api_{datetime.now().strftime('%Y%m%d')}.log"))
file_handler.setLevel(getattr(logging, LOG_LEVEL))
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

from crewai.runner import CrewAIRunner
from autogen.runner import AutoGenRunner
from langgraph.runner import LangGraphRunner
from googleadk.runner import GoogleADKRunner
from squidai.runner import SquidAIRunner
from lettaai.runner import LettaAIRunner
from portiaai.runner import PortiaAIRunner
from h2oai.runner import H2OAIRunner
from uipath.runner import UiPathRunner

app = FastAPI(
    title=os.getenv("API_TITLE", "Agent Runner API"),
    description=os.getenv("API_DESCRIPTION", "API for running agent tasks"),
    version=os.getenv("API_VERSION", "1.0.0"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=bool(os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"),
    allow_methods=os.getenv("CORS_METHODS", "*").split(","),
    allow_headers=os.getenv("CORS_HEADERS", "*").split(","),
)

class RunRequest(BaseModel):
    agent: str = Field(..., description="Agent framework to use")
    topic: str = Field(..., description="Topic to research")

class AgentStep(BaseModel):
    type: str
    timestamp: str
    details: Dict[str, Any]

class AgentResponse(BaseModel):
    agent_name: str
    final_output: str
    steps: List[AgentStep]
    token_usage: int
    response_time: float
    error: Optional[bool] = False

class FrameworksResponse(BaseModel):
    frameworks: List[str]

agent_runners = {
    "crewai": CrewAIRunner(),
    "autogen": AutoGenRunner(),
    "langgraph": LangGraphRunner(),
    "googleadk": GoogleADKRunner(),
    "squidai": SquidAIRunner(),
    "lettaai": LettaAIRunner(),
    "portiaai": PortiaAIRunner(),
    "h2oai": H2OAIRunner(),
    "uipath": UiPathRunner()
}

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
        event_type: Type of event (e.g., 'request', 'response', 'error')
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

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Request Error",
                "message": str(exc.detail),
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/frameworks", response_model=FrameworksResponse)
async def get_frameworks(request: Request):
    """
    Get available agent frameworks.
    """
    log_event(
        event_type="frameworks_request",
        message="Frameworks list requested",
        level="info",
        details={
            "client_host": request.client.host if request.client else None
        }
    )
    
    return {"frameworks": list(agent_runners.keys())}

@app.post("/run", response_model=AgentResponse)
async def run_agent(request: RunRequest, req: Request):
    """
    Run an agent task.
    """
    request_id = str(uuid.uuid4())
    
    log_event(
        event_type="run_request",
        message=f"Agent run requested: {request.agent} for topic '{request.topic}'",
        level="info",
        details={
            "agent": request.agent,
            "topic": request.topic,
            "client_host": req.client.host if req.client else None
        },
        request_id=request_id
    )
    
    if request.agent not in agent_runners:
        log_event(
            event_type="run_error",
            message=f"Invalid agent framework requested: {request.agent}",
            level="error",
            details={"available_agents": list(agent_runners.keys())},
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid Agent",
                "message": f"Agent framework '{request.agent}' not found",
                "available_agents": list(agent_runners.keys()),
                "request_id": request_id
            }
        )
    
    try:
        start_time = time.time()
        
        runner = agent_runners[request.agent]
        result = runner.run_task(request.topic)
        
        process_time = time.time() - start_time
        
        log_event(
            event_type="run_complete",
            message=f"Agent run completed: {request.agent} for topic '{request.topic}'",
            level="info",
            details={
                "agent": request.agent,
                "topic": request.topic,
                "process_time_ms": round(process_time * 1000, 2),
                "token_usage": result.get("token_usage", 0)
            },
            request_id=request_id
        )
        
        return result
    except Exception as e:
        log_event(
            event_type="run_error",
            message=f"Error running agent {request.agent}: {str(e)}",
            level="error",
            details={
                "agent": request.agent,
                "topic": request.topic,
                "error": str(e)
            },
            request_id=request_id
        )
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Agent Execution Failed",
                "message": f"Error running {request.agent} agent: {str(e)}",
                "request_id": request_id
            }
        )

@app.get("/health")
async def health_check():
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
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("API_VERSION", "1.0.0")
    }

@app.get("/status")
async def status():
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
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "frameworks": list(agent_runners.keys())
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    
    log_event(
        event_type="server_start",
        message=f"Starting Agent Runner API on {host}:{port}",
        level="info",
        details={
            "host": host,
            "port": port,
            "frameworks": list(agent_runners.keys())
        }
    )
    
    uvicorn.run(app, host=host, port=port)
