# Agent Frameworks

This section provides detailed architecture diagrams and explanations for each agent framework implemented in the Agentic AI RAG Benchmark project.

## Supported Frameworks

The project supports both real and mock agent frameworks:

### Real Implementations

These frameworks have real implementations with actual dependencies:

- [CrewAI](./crewai.md): A framework for creating multi-agent systems with specialized roles
- [AutoGen](./autogen.md): A framework for building conversational agents with LLMs
- [LangGraph](./langgraph.md): A framework for building graph-based workflows with LLMs
- [Google ADK](./googleadk.md): Google's Agent Development Kit for building AI agents
- [UiPath](./uipath.md): A framework for building process automation agents

### Mock Implementations

These frameworks have simulated implementations for demonstration and comparison purposes:

- [SquidAI](./squidai.md): A simulated framework for building tool-using agents
- [LettaAI](./lettaai.md): A simulated framework for building memory-augmented agents
- [Portia AI](./portiaai.md): A simulated framework for building knowledge graph-enhanced agents
- [H2O AI](./h2oai.md): A simulated framework for building predictive analytics and machine learning-powered agents

## Common Architecture

All agent frameworks share a common architecture pattern:

1. **Base Agent Runner**: All frameworks extend the `AgentRunner` abstract base class
2. **RAG Integration**: All frameworks use the RAG service to retrieve relevant information
3. **Logging**: All frameworks log execution steps, metrics, and outputs
4. **Output Format**: All frameworks return outputs in a standardized format

For details on the specific architecture of each framework, see the corresponding documentation.
