# Agent Frameworks Usage Guide

This document provides detailed instructions for using the agent frameworks in the Agentic AI RAG Benchmark project.

## Supported Frameworks

The project currently supports the following agent frameworks:

1. **CrewAI**: A framework for creating multi-agent systems with specialized roles
2. **AutoGen**: A framework for building conversational agents with LLMs
3. **LangGraph**: A framework for building graph-based workflows with LLMs
4. **Google ADK**: Google's Agent Development Kit for building AI agents
5. **SquidAI**: A framework for building tool-using agents
6. **LettaAI**: A framework for building memory-augmented agents
7. **Portia AI**: A framework for building knowledge graph-enhanced agents
8. **H2O AI**: A framework for building predictive analytics and machine learning-powered agents
9. **UiPath**: A framework for building process automation agents

## Running Agent Frameworks

### Using Python

To run an agent framework using Python:

```bash
# Activate your virtual environment
source venv/bin/activate

# Run a specific agent framework
python -m agents.runner --topic "Tesla" --framework "crewai"
```

Available command-line options:

- `--topic`: The topic or company to research (required)
- `--framework`: The agent framework to use (default: value from environment variable)
- `--max_tokens`: Maximum number of tokens to generate (default: 4000)
- `--timeout`: Maximum time in seconds to wait for the agent to complete (default: 300)

### Using Docker

To run an agent framework using Docker:

```bash
# Run with CrewAI (default)
AGENT_FRAMEWORK=crewai docker-compose up -d agent_runner

# Run with AutoGen
AGENT_FRAMEWORK=autogen docker-compose up -d agent_runner

# View logs
docker-compose logs -f agent_runner
```

## Framework-Specific Usage

### CrewAI

CrewAI uses a multi-agent approach with specialized roles:

```python
from agents.crewai.runner import CrewAIRunner

# Create a CrewAI runner
runner = CrewAIRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

CrewAI creates a crew of agents with different roles:

1. **Researcher**: Gathers information about the company
2. **Analyst**: Analyzes the gathered information
3. **Writer**: Generates the final report

### AutoGen

AutoGen uses a conversational approach with multiple agents:

```python
from agents.autogen.runner import AutoGenRunner

# Create an AutoGen runner
runner = AutoGenRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

AutoGen creates a group chat with the following agents:

1. **User Proxy**: Represents the user's interests
2. **Researcher**: Gathers information about the company
3. **Analyst**: Analyzes the gathered information
4. **Financial Expert**: Provides financial insights

### LangGraph

LangGraph uses a graph-based workflow:

```python
from agents.langgraph.runner import LangGraphRunner

# Create a LangGraph runner
runner = LangGraphRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

LangGraph creates a graph with the following nodes:

1. **Research**: Gathers information about the company
2. **Analysis**: Analyzes the gathered information
3. **Report**: Generates the final report

### Google ADK

Google ADK uses a tool-based approach:

```python
from agents.googleadk.runner import GoogleADKRunner

# Create a Google ADK runner
runner = GoogleADKRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

Google ADK creates an agent with the following tools:

1. **RAG Tool**: Retrieves information from the RAG service
2. **Web Search Tool**: Searches the web for information
3. **Analysis Tool**: Analyzes the gathered information

### SquidAI

SquidAI uses a tool-based approach with specialized tools:

```python
from agents.squidai.runner import SquidAIRunner

# Create a SquidAI runner
runner = SquidAIRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

SquidAI creates an agent with the following tools:

1. **Company Profile Tool**: Retrieves company profile information
2. **News Tool**: Retrieves news articles about the company
3. **Financial Tool**: Retrieves financial data about the company
4. **Product Tool**: Retrieves information about the company's products
5. **Analysis Tool**: Analyzes the gathered information

### LettaAI

LettaAI uses a memory-augmented approach:

```python
from agents.lettaai.runner import LettaAIRunner

# Create a LettaAI runner
runner = LettaAIRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

LettaAI creates an agent with the following memory types:

1. **Working Memory**: Stores current context and information
2. **Episodic Memory**: Stores past experiences and interactions
3. **Semantic Memory**: Stores general knowledge and facts

### Portia AI

Portia AI uses a knowledge graph-enhanced approach:

```python
from agents.portiaai.runner import PortiaAIRunner

# Create a Portia AI runner
runner = PortiaAIRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

Portia AI creates an agent with the following components:

1. **Knowledge Graph Builder**: Builds a knowledge graph from retrieved information
2. **Entity Analysis**: Analyzes entities in the knowledge graph
3. **Relationship Mapping**: Maps relationships between entities
4. **Graph-Based Analysis**: Extracts insights from the knowledge graph

### H2O AI

H2O AI uses a predictive analytics approach:

```python
from agents.h2oai.runner import H2OAIRunner

# Create an H2O AI runner
runner = H2OAIRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

H2O AI creates an agent with the following components:

1. **Data Preprocessing**: Cleans and structures the data
2. **Time Series Analysis**: Analyzes trends and patterns over time
3. **Market Segmentation**: Identifies key market segments
4. **Predictive Modeling**: Builds models to forecast future performance

### UiPath

UiPath uses a process automation approach:

```python
from agents.uipath.runner import UiPathRunner

# Create a UiPath runner
runner = UiPathRunner()

# Run the agent
result = runner.run_task("Tesla")

# Print the result
print(result["final_output"])
```

UiPath creates an agent with the following components:

1. **Workflow Planner**: Plans the research workflow
2. **Data Collection Process**: Gathers information from various sources
3. **Data Structuring Process**: Organizes the collected data
4. **Comparative Analysis**: Compares the company with competitors

## Comparing Agent Frameworks

To compare multiple agent frameworks:

```python
from agents.runner import compare_frameworks

# Compare frameworks
results = compare_frameworks(
    topic="Tesla",
    frameworks=["crewai", "autogen", "langgraph"],
    max_tokens=4000,
    timeout=300
)

# Print results
for framework, result in results.items():
    print(f"{framework}: {result['final_output'][:100]}...")
```

## Customizing Agent Frameworks

Each agent framework can be customized by modifying its configuration in the `.env` file:

```
# CrewAI Configuration
CREWAI_AGENT_COUNT=3
CREWAI_MEMORY_ENABLED=True

# AutoGen Configuration
AUTOGEN_AGENT_COUNT=3
AUTOGEN_MAX_ROUNDS=10

# LangGraph Configuration
LANGGRAPH_NODE_COUNT=3
LANGGRAPH_MAX_ITERATIONS=5

# Google ADK Configuration
GOOGLEADK_TOOL_COUNT=5
GOOGLEADK_MEMORY_ENABLED=True

# SquidAI Configuration
SQUIDAI_TOOL_COUNT=6
SQUIDAI_MEMORY_ENABLED=True

# LettaAI Configuration
LETTAAI_MEMORY_TYPES=3
LETTAAI_WORKFLOW_COUNT=3

# Portia AI Configuration
PORTIAAI_ENTITY_THRESHOLD=0.7
PORTIAAI_RELATION_THRESHOLD=0.6

# H2O AI Configuration
H2OAI_MODEL_TYPE=gradient_boosting
H2OAI_FORECAST_HORIZON=90

# UiPath Configuration
UIPATH_PROCESS_TIMEOUT=60
UIPATH_MAX_SOURCES=10
```

## Logging

Each agent framework logs its execution to the `logs/{framework_name}/` directory. The logs include:

- Execution steps
- Token usage
- Response time
- Intermediate outputs
- Final output

To view the logs:

```bash
# View CrewAI logs
cat logs/crewai/latest.json

# View AutoGen logs
cat logs/autogen/latest.json
```

## Troubleshooting

### Agent Not Starting

If an agent framework fails to start:

1. Check if the required environment variables are set in the `.env` file
2. Verify that the required dependencies are installed
3. Check the logs for error messages

### Agent Execution Failures

If an agent execution fails:

1. Check if the RAG service is running and accessible
2. Verify that the agent framework is properly configured
3. Check the logs for error messages

### Timeout Issues

If an agent execution times out:

1. Increase the timeout value
2. Reduce the complexity of the task
3. Check if the agent is stuck in a loop

## Next Steps

For more information on the agent frameworks API, see the [Agent Runner API](../api/agent_runner.md) documentation.

For more information on the agent frameworks architecture, see the [Agent Frameworks Architecture](../architecture/frameworks/README.md) documentation.
