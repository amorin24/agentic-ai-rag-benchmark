# UI Viewer Usage Guide

This document provides detailed instructions for using the UI viewer in the Agentic AI RAG Benchmark project.

## Starting the UI Viewer

### Using Node.js

To start the UI viewer using Node.js:

```bash
# Navigate to the UI directory
cd ui/viewer

# Install dependencies (if not already installed)
npm install

# Start the development server
npm start
```

The UI will start on the port specified in the `.env` file (default: 3000) and can be accessed at `http://localhost:3000`.

### Using Docker

To start the UI viewer using Docker:

```bash
# Start only the UI
docker-compose up -d ui

# View logs
docker-compose logs -f ui
```

## UI Features

The UI viewer provides a comprehensive interface for comparing agent frameworks:

### Company/Topic Selection

1. **Select a company or topic**: Use the dropdown menu or enter a custom company/topic name
2. **Configure parameters**: Set maximum tokens, timeout, and other parameters
3. **Select agent frameworks**: Choose which frameworks to run and compare

### Running Agent Frameworks

1. **Run all frameworks**: Click the "Run All" button to run all selected frameworks
2. **Run individual framework**: Click the "Run" button next to a specific framework
3. **View progress**: See real-time progress indicators for each framework

### Viewing Results

The UI displays results in a tabbed interface with several sections:

#### Final Output Tab

This tab shows the final output from each agent framework side-by-side, allowing for easy comparison of the generated reports.

#### Steps Tab

This tab shows the execution steps for each agent framework, including:

- Research planning
- Information gathering
- Analysis
- Report generation

Each step includes:
- Step name
- Output
- Timestamp
- Duration

#### Metrics Tab

This tab shows performance metrics for each agent framework, including:

- Token usage
- Response time
- Factual overlap with RAG context
- Reasoning clarity

#### Logs Tab

This tab shows detailed logs for each agent framework, including:

- API calls
- RAG service interactions
- Error messages
- Debugging information

### Comparing Frameworks

The UI provides several tools for comparing frameworks:

1. **Side-by-side comparison**: View outputs from different frameworks side-by-side
2. **Metric comparison**: Compare performance metrics across frameworks
3. **Step comparison**: Compare execution steps across frameworks
4. **Highlight differences**: Highlight differences between framework outputs

### Exporting Results

The UI allows exporting results in several formats:

1. **JSON**: Export all data in JSON format
2. **CSV**: Export metrics in CSV format
3. **PDF**: Export reports in PDF format
4. **HTML**: Export reports in HTML format

## Advanced Features

### Customizing the UI

The UI can be customized using environment variables in the `.env` file:

```
# UI Configuration
UI_PORT=3000
UI_HOST=localhost
UI_THEME=light
UI_DEFAULT_FRAMEWORK=crewai
```

### Filtering Results

The UI provides several filtering options:

1. **Filter by framework**: Show only specific frameworks
2. **Filter by metric**: Sort frameworks by specific metrics
3. **Filter by date**: Show only results from a specific date range

### Saving and Loading Results

The UI allows saving and loading results:

1. **Save results**: Save current results to local storage
2. **Load results**: Load previously saved results
3. **Share results**: Generate a shareable link for results

## Troubleshooting

### UI Not Starting

If the UI fails to start:

1. Check if the required dependencies are installed
2. Verify that the port is not already in use
3. Check the logs for error messages

### UI Not Connecting to RAG Service

If the UI cannot connect to the RAG service:

1. Check if the RAG service is running
2. Verify that the RAG service URL is correctly configured in the `.env` file
3. Check for network issues or firewall restrictions

### UI Not Displaying Results

If the UI does not display results:

1. Check if the agent frameworks are running
2. Verify that the agent runner API is correctly configured
3. Check the browser console for error messages

## Next Steps

For more information on the UI architecture, see the [UI Viewer Architecture](../architecture/ui_viewer.md) documentation.
