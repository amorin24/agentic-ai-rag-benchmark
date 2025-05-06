# Tests

Test suite for the RAG benchmark project.

## Structure

- **rag_service/**: Tests for the RAG service
- **agents/**: Tests for agent implementations
- **ui/**: Tests for the UI components

## Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/rag_service
pytest tests/agents
pytest tests/ui

# Run with coverage
pytest --cov=.
```
