from abc import ABC, abstractmethod
from typing import Dict, Any

class AgentRunner(ABC):
    """
    Abstract base class for agent runners.
    All agent implementations should inherit from this class.
    """
    
    @abstractmethod
    def __init__(self, rag_service_url: str):
        """
        Initialize the agent with RAG service connection.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        pass
        
    @abstractmethod
    def run(self, task: str) -> Dict[str, Any]:
        """
        Run the agent on a given task and return results.
        
        Args:
            task: The task description
            
        Returns:
            Dictionary containing the agent's results and metrics
        """
        pass
