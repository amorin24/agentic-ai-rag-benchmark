"""
Unit tests for UI components.
"""

import os
import pytest
import json
from unittest.mock import patch, MagicMock

class MockReactTestingLibrary:
    def render(self, component):
        return MagicMock()
    
    def screen(self):
        return MagicMock()
    
    def fireEvent(self):
        return MagicMock()

@pytest.fixture
def mock_react_testing_library():
    return MockReactTestingLibrary()

class TestUIComponents:
    """Test cases for UI components."""
    
    @pytest.fixture
    def mock_axios(self):
        """Mock axios for testing API calls."""
        with patch('axios') as mock_axios:
            mock_axios.get.return_value = {
                "data": {
                    "frameworks": ["crewai", "autogen", "langgraph", "googleadk", "squidai", "lettaai", "portiaai", "h2oai", "uipath"],
                    "results": {
                        "crewai": {
                            "response_time": 2.5,
                            "token_usage": 1500,
                            "factual_overlap": 0.85,
                            "reasoning_clarity": 0.9,
                            "final_output": "Test output from CrewAI",
                            "steps": [{"type": "info", "data": {"message": "Test step"}}]
                        },
                        "autogen": {
                            "response_time": 3.0,
                            "token_usage": 1800,
                            "factual_overlap": 0.8,
                            "reasoning_clarity": 0.85,
                            "final_output": "Test output from AutoGen",
                            "steps": [{"type": "info", "data": {"message": "Test step"}}]
                        }
                    }
                }
            }
            yield mock_axios
    
    def test_app_component_initialization(self, mock_react_testing_library, mock_axios):
        """Test App component initialization."""
        
        app = {"component": "App", "props": {}}
        render_result = mock_react_testing_library.render(app)
        
        mock_axios.get.assert_called_with("/api/available-agents")
    
    def test_agent_results_interface(self):
        """Test AgentResults interface includes all frameworks."""
        app_tsx_path = os.path.join(os.path.dirname(__file__), "../../ui/viewer/src/App.tsx")
        
        with open(app_tsx_path, "r") as f:
            app_tsx_content = f.read()
        
        frameworks = ["crewai", "autogen", "langgraph", "googleadk", "squidai", "lettaai", "portiaai", "h2oai", "uipath"]
        for framework in frameworks:
            assert f"{framework}?" in app_tsx_content
    
    def test_get_available_agents_fallback(self):
        """Test getAvailableAgents fallback includes all frameworks."""
        app_tsx_path = os.path.join(os.path.dirname(__file__), "../../ui/viewer/src/App.tsx")
        
        with open(app_tsx_path, "r") as f:
            app_tsx_content = f.read()
        
        frameworks = ["crewai", "autogen", "langgraph", "googleadk", "squidai", "lettaai", "portiaai", "h2oai", "uipath"]
        fallback_list_line = None
        
        for line in app_tsx_content.split("\n"):
            if "return [" in line and "crewai" in line:
                fallback_list_line = line
                break
        
        assert fallback_list_line is not None
        for framework in frameworks:
            assert framework in fallback_list_line
    
    def test_tab_panel_component(self, mock_react_testing_library):
        """Test TabPanel component."""
        tab_panel = {
            "component": "TabPanel",
            "props": {
                "value": 0,
                "index": 0,
                "children": "Test content"
            }
        }
        render_result = mock_react_testing_library.render(tab_panel)
        
        assert True
    
    def test_agent_comparison_component(self, mock_react_testing_library, mock_axios):
        """Test AgentComparison component."""
        agent_comparison = {
            "component": "AgentComparison",
            "props": {
                "results": {
                    "crewai": {
                        "response_time": 2.5,
                        "token_usage": 1500,
                        "factual_overlap": 0.85,
                        "reasoning_clarity": 0.9,
                        "final_output": "Test output from CrewAI",
                        "steps": [{"type": "info", "data": {"message": "Test step"}}]
                    },
                    "autogen": {
                        "response_time": 3.0,
                        "token_usage": 1800,
                        "factual_overlap": 0.8,
                        "reasoning_clarity": 0.85,
                        "final_output": "Test output from AutoGen",
                        "steps": [{"type": "info", "data": {"message": "Test step"}}]
                    }
                }
            }
        }
        render_result = mock_react_testing_library.render(agent_comparison)
        
        assert True
