# Agent Runners

Modular implementations for different agent frameworks that use the shared RAG service.

## Supported Frameworks

- **CrewAI**: Multi-agent framework with specialized roles
- **AutoGen**: Conversational framework for multiple agents
- **LangGraph**: Graph-based workflow for agent orchestration

## Common Interface

All agent implementations follow a common interface to ensure fair comparison:

```python
class AgentRunner:
    def __init__(self, rag_service_url: str):
        """Initialize the agent with RAG service connection."""
        pass
        
    def run(self, task: str) -> dict:
        """Run the agent on a given task and return results."""
        pass
```

## Output Schema

All agents return results in a standardized format:

```json
{
  "result": "Final answer or solution",
  "reasoning": "Step-by-step reasoning process",
  "rag_queries": [
    {
      "query": "Question sent to RAG service",
      "retrieved_context": "Context returned by RAG service",
      "usage": "How the agent used this information"
    }
  ],
  "metrics": {
    "time_taken": 10.5,
    "tokens_used": 1500,
    "rag_calls": 5
  }
}
```
