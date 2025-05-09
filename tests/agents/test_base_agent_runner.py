"""
Unit tests for the base agent runner.
"""

import os
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pathlib import Path

from agents.base_agent_runner import AgentRunner

class TestAgentRunner(AgentRunner):
    """Test implementation of the AgentRunner abstract class."""
    
    def run_task(self, topic: str):
        """Implement the abstract method for testing."""
        super().run_task(topic)
        
        self._add_step("test_step", {
            "test_data": "test value"
        })
        
        self._update_token_usage(100)
        
        self._set_final_output(f"Test output for {topic}")
        
        self._complete_task()
        
        return self.format_output()


class TestBaseAgentRunner:
    """Test cases for the base agent runner."""
    
    @pytest.fixture
    def agent_runner(self, tmp_path):
        """Create a test agent runner instance."""
        with patch.object(Path, 'mkdir'):
            with patch('agents.base_agent_runner.LOGS_DIR', tmp_path):
                return TestAgentRunner("test_agent", "http://localhost:8000")
    
    def test_initialization(self, agent_runner):
        """Test agent runner initialization."""
        assert agent_runner.agent_name == "test_agent"
        assert agent_runner.rag_service_url == "http://localhost:8000"
        assert agent_runner.steps == []
        assert agent_runner.token_usage == 0
        assert agent_runner.final_output == ""
    
    def test_run_task(self, agent_runner):
        """Test run_task method."""
        result = agent_runner.run_task("test_topic")
        
        assert result["agent_name"] == "test_agent"
        assert result["final_output"] == "Test output for test_topic"
        assert len(result["steps"]) == 3  # task_start, test_step, task_complete
        assert result["token_usage"] == 100
        assert isinstance(result["response_time"], float)
    
    def test_add_step(self, agent_runner):
        """Test _add_step method."""
        agent_runner._add_step("test_type", {"key": "value"})
        
        assert len(agent_runner.steps) == 1
        assert agent_runner.steps[0]["step_type"] == "test_type"
        assert agent_runner.steps[0]["key"] == "value"
        assert "timestamp" in agent_runner.steps[0]
        assert "step_id" in agent_runner.steps[0]
    
    def test_update_token_usage(self, agent_runner):
        """Test _update_token_usage method."""
        initial_usage = agent_runner.token_usage
        agent_runner._update_token_usage(50)
        
        assert agent_runner.token_usage == initial_usage + 50
    
    def test_set_final_output(self, agent_runner):
        """Test _set_final_output method."""
        agent_runner._set_final_output("Final test output")
        
        assert agent_runner.final_output == "Final test output"
        assert len(agent_runner.steps) == 1
        assert agent_runner.steps[0]["step_type"] == "final_output"
        assert agent_runner.steps[0]["output"] == "Final test output"
    
    def test_complete_task(self, agent_runner):
        """Test _complete_task method."""
        agent_runner.start_time = time.time() - 1  # Set start time 1 second ago
        agent_runner._complete_task()
        
        assert agent_runner.end_time is not None
        assert len(agent_runner.steps) == 1
        assert agent_runner.steps[0]["step_type"] == "task_complete"
        assert "duration" in agent_runner.steps[0]
        assert agent_runner.steps[0]["duration"] > 0
    
    def test_format_output(self, agent_runner):
        """Test format_output method."""
        agent_runner.start_time = time.time() - 2
        agent_runner.end_time = time.time()
        agent_runner.token_usage = 150
        agent_runner.final_output = "Test formatted output"
        agent_runner._add_step("test_step", {"data": "test"})
        
        output = agent_runner.format_output()
        
        assert output["agent_name"] == "test_agent"
        assert output["final_output"] == "Test formatted output"
        assert output["token_usage"] == 150
        assert output["response_time"] > 0
        assert len(output["steps"]) == 1
    
    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.dump')
    def test_log_metadata(self, mock_json_dump, mock_open, agent_runner):
        """Test log_metadata method."""
        agent_runner.start_time = time.time() - 3
        agent_runner.end_time = time.time()
        agent_runner.token_usage = 200
        agent_runner.final_output = "Test log output"
        agent_runner._add_step("test_log_step", {"log_data": "test"})
        
        log_path = agent_runner.log_metadata()
        
        assert mock_open.called
        assert mock_json_dump.called
        
        args, _ = mock_json_dump.call_args
        log_data = args[0]
        
        assert log_data["agent_name"] == "test_agent"
        assert log_data["token_usage"] == 200
        assert log_data["final_output"] == "Test log output"
        assert len(log_data["steps"]) == 1
        assert log_data["steps"][0]["step_type"] == "test_log_step"
        assert log_data["steps"][0]["log_data"] == "test"
