"""
Base Agent Runner module for the RAG benchmark.

This module defines an abstract base class for agent runners that will be
implemented by different agent frameworks.
"""

import os
import time
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LOGS_DIR = Path(os.getenv('LOGS_DIR', 'logs'))


class AgentRunner(ABC):
    """
    Abstract base class for agent runners.
    
    This class defines the interface that all agent framework implementations
    must follow to ensure consistent behavior and output format.
    """
    
    def __init__(self, agent_name: str, rag_service_url: str):
        """
        Initialize the agent runner.
        
        Args:
            agent_name: Name of the agent framework
            rag_service_url: URL of the RAG service
        """
        self.agent_name = agent_name
        self.rag_service_url = rag_service_url
        self.start_time = None
        self.end_time = None
        self.steps = []
        self.token_usage = 0
        self.final_output = ""
        
        self.logs_dir = LOGS_DIR / agent_name
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Perform the agent task using the shared RAG service.
        
        This method should be implemented by each agent framework to execute
        the task using its specific approach.
        
        Args:
            topic: The topic or task to perform
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        self.start_time = time.time()
        
        self._add_step("task_start", {
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })
        
        pass
    
    def log_metadata(self) -> str:
        """
        Store run logs, steps, and timing information.
        
        This method saves the execution metadata to a log file in the
        logs/{agent_name}/ folder.
        
        Returns:
            Path to the log file
        """
        if self.end_time is None:
            self.end_time = time.time()
        
        log_data = {
            "agent_name": self.agent_name,
            "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            "response_time": self.end_time - self.start_time if self.start_time and self.end_time else None,
            "token_usage": self.token_usage,
            "steps": self.steps,
            "final_output": self.final_output
        }
        
        log_file = self.logs_dir / f"run_{log_data['run_id']}.json"
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Logged run metadata to {log_file}")
        return str(log_file)
    
    def format_output(self) -> Dict[str, Any]:
        """
        Return final output in standardized format.
        
        Returns:
            Dictionary with agent name, final output, steps, token usage, and response time
        """
        if self.end_time is None:
            self.end_time = time.time()
        
        response_time = self.end_time - self.start_time if self.start_time and self.end_time else None
        
        return {
            "agent_name": self.agent_name,
            "final_output": self.final_output,
            "steps": self.steps,
            "token_usage": self.token_usage,
            "response_time": response_time
        }
    
    def _add_step(self, step_type: str, step_data: Dict[str, Any]) -> None:
        """
        Add a step to the execution log.
        
        Args:
            step_type: Type of step (e.g., 'rag_query', 'reasoning', 'action')
            step_data: Data associated with the step
        """
        step = {
            "step_id": len(self.steps) + 1,
            "step_type": step_type,
            "timestamp": datetime.now().isoformat(),
            **step_data
        }
        
        self.steps.append(step)
    
    def _update_token_usage(self, additional_tokens: int) -> None:
        """
        Update the token usage counter.
        
        Args:
            additional_tokens: Number of tokens to add to the counter
        """
        self.token_usage += additional_tokens
    
    def _set_final_output(self, output: str) -> None:
        """
        Set the final output of the agent.
        
        Args:
            output: Final output text
        """
        self.final_output = output
        
        self._add_step("final_output", {
            "output": output
        })
    
    def _complete_task(self) -> None:
        """
        Mark the task as complete and record timing.
        """
        self.end_time = time.time()
        
        self._add_step("task_complete", {
            "timestamp": datetime.now().isoformat(),
            "duration": self.end_time - self.start_time if self.start_time else None
        })


if __name__ == "__main__":
    
    class ExampleAgent(AgentRunner):
        def run_task(self, topic: str) -> Dict[str, Any]:
            super().run_task(topic)  # Initialize timing and steps
            
            time.sleep(1)
            
            self._add_step("rag_query", {
                "query": f"Information about {topic}",
                "results": ["Sample result 1", "Sample result 2"]
            })
            
            time.sleep(0.5)
            
            self._add_step("reasoning", {
                "thought": f"Analyzing information about {topic}"
            })
            
            self._update_token_usage(150)
            
            self._set_final_output(f"This is what I learned about {topic}...")
            
            self._complete_task()
            
            return self.format_output()
    
    print("Example of how an agent implementation would use this base class:")
    print("agent = ExampleAgent('example_agent', 'http://localhost:8000')")
    print("result = agent.run_task('artificial intelligence')")
    print("agent.log_metadata()")
    print("output = agent.format_output()")
