"""
Configuration module for the Agentic AI RAG Benchmark project.

This module loads environment variables from the .env file and exposes them as typed constants
that can be imported by other modules in the project. Variables are grouped by category
for better organization and maintainability.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _get_env(key: str, default: Any = None, required: bool = False, var_type: type = str) -> Any:
    """
    Get environment variable with type conversion and validation.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        var_type: Type to convert the value to
        
    Returns:
        The environment variable value converted to the specified type
    
    Raises:
        ValueError: If the variable is required but not found
    """
    value = os.getenv(key)
    
    if value is None:
        if required:
            raise ValueError(f"Required environment variable {key} not found")
        return default
    
    if var_type == bool:
        return value.lower() in ('true', 'yes', '1', 'y')
    elif var_type == int:
        return int(value)
    elif var_type == float:
        return float(value)
    elif var_type == list:
        return value.split(',')
    elif var_type == Path:
        return Path(value)
    else:
        return value

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / _get_env("LOG_DIR", "./logs", var_type=str).lstrip("./")

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

RAG_SERVICE_HOST = _get_env("RAG_SERVICE_HOST", "localhost")
RAG_SERVICE_PORT = _get_env("RAG_SERVICE_PORT", 8000, var_type=int)
RAG_SERVICE_URL = f"http://{RAG_SERVICE_HOST}:{RAG_SERVICE_PORT}"
VECTOR_DB_PATH = _get_env("VECTOR_DB_PATH", "./data/vector_store")
PROCESSED_DOCS_DIR = _get_env("PROCESSED_DOCS_DIR", "data/processed")
CHUNK_SIZE = _get_env("CHUNK_SIZE", 1000, var_type=int)
CHUNK_OVERLAP = _get_env("CHUNK_OVERLAP", 200, var_type=int)

OPENAI_API_KEY = _get_env("OPENAI_API_KEY", required=True)
OPENAI_MODEL = _get_env("OPENAI_MODEL", "gpt-4o")
ANTHROPIC_API_KEY = _get_env("ANTHROPIC_API_KEY", "")

WIKIPEDIA_MAX_ARTICLES = _get_env("WIKIPEDIA_MAX_ARTICLES", 5, var_type=int)
WIKIPEDIA_LANGUAGE = _get_env("WIKIPEDIA_LANGUAGE", "en")

NEWS_API_KEY = _get_env("NEWS_API_KEY", "")
NEWS_API_MAX_ARTICLES = _get_env("NEWS_API_MAX_ARTICLES", 10, var_type=int)
NEWS_API_SORT_BY = _get_env("NEWS_API_SORT_BY", "relevancy")

FMP_API_KEY = _get_env("FMP_API_KEY", "")

UI_PORT = _get_env("UI_PORT", 3000, var_type=int)

LOG_LEVEL = _get_env("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

CONFIG: Dict[str, Any] = {
    "rag_service": {
        "host": RAG_SERVICE_HOST,
        "port": RAG_SERVICE_PORT,
        "url": RAG_SERVICE_URL,
        "vector_db_path": VECTOR_DB_PATH,
        "processed_docs_dir": PROCESSED_DOCS_DIR,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
    },
    
    "agent": {
        "openai_api_key": OPENAI_API_KEY,
        "openai_model": OPENAI_MODEL,
        "anthropic_api_key": ANTHROPIC_API_KEY,
    },
    
    "data_sources": {
        "wikipedia": {
            "max_articles": WIKIPEDIA_MAX_ARTICLES,
            "language": WIKIPEDIA_LANGUAGE,
        },
        "news_api": {
            "api_key": NEWS_API_KEY,
            "max_articles": NEWS_API_MAX_ARTICLES,
            "sort_by": NEWS_API_SORT_BY,
        },
        "fmp_api": {
            "api_key": FMP_API_KEY,
        },
    },
    
    "ui": {
        "port": UI_PORT,
    },
    
    "logging": {
        "level": LOG_LEVEL,
        "format": LOG_FORMAT,
        "dir": LOGS_DIR,
    },
    
    "paths": {
        "project_root": PROJECT_ROOT,
        "data_dir": DATA_DIR,
        "logs_dir": LOGS_DIR,
    },
}

if __name__ == "__main__":
    """Print configuration when module is run directly."""
    import json
    
    safe_config = CONFIG.copy()
    safe_config["agent"]["openai_api_key"] = "***" if OPENAI_API_KEY else None
    safe_config["agent"]["anthropic_api_key"] = "***" if ANTHROPIC_API_KEY else None
    safe_config["data_sources"]["news_api"]["api_key"] = "***" if NEWS_API_KEY else None
    safe_config["data_sources"]["fmp_api"]["api_key"] = "***" if FMP_API_KEY else None
    
    print(json.dumps(safe_config, indent=2, default=str))
