import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Grid, 
  Paper, 
  Tabs, 
  Tab, 
  CircularProgress 
} from '@mui/material';
import axios from 'axios';

interface AgentResponse {
  result: string;
  reasoning: string;
  rag_queries: {
    query: string;
    retrieved_context: string;
    usage: string;
  }[];
  metrics: {
    time_taken: number;
    tokens_used: number;
    rag_calls: number;
  };
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`agent-tabpanel-${index}`}
      aria-labelledby={`agent-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [task, setTask] = useState('');
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [results, setResults] = useState<{
    crewai?: AgentResponse;
    autogen?: AgentResponse;
    langgraph?: AgentResponse;
  }>({});

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSubmit = async () => {
    if (!task) return;
    
    setLoading(true);
    
    try {
      
      const crewaiPromise = new Promise<AgentResponse>((resolve) => {
        setTimeout(() => {
          resolve({
            result: `CrewAI solution for: ${task}`,
            reasoning: "Step-by-step reasoning process would go here",
            rag_queries: [
              {
                query: `Information needed for: ${task}`,
                retrieved_context: "Placeholder context from RAG service",
                usage: "Used to understand the task requirements"
              }
            ],
            metrics: {
              time_taken: 2.3,
              tokens_used: 1500,
              rag_calls: 1
            }
          });
        }, 2300);
      });
      
      const autogenPromise = new Promise<AgentResponse>((resolve) => {
        setTimeout(() => {
          resolve({
            result: `AutoGen solution for: ${task}`,
            reasoning: "Step-by-step reasoning process would go here",
            rag_queries: [
              {
                query: `Information needed for: ${task}`,
                retrieved_context: "Placeholder context from RAG service",
                usage: "Used to understand the task requirements"
              },
              {
                query: `Additional details for: ${task}`,
                retrieved_context: "More placeholder context from RAG service",
                usage: "Used to gather more specific information"
              }
            ],
            metrics: {
              time_taken: 2.8,
              tokens_used: 1800,
              rag_calls: 2
            }
          });
        }, 2800);
      });
      
      const langgraphPromise = new Promise<AgentResponse>((resolve) => {
        setTimeout(() => {
          resolve({
            result: `LangGraph solution for: ${task}`,
            reasoning: "Step-by-step reasoning process through graph nodes would go here",
            rag_queries: [
              {
                query: `Initial information for: ${task}`,
                retrieved_context: "Placeholder context from RAG service",
                usage: "Used to understand the task requirements"
              },
              {
                query: `Specific details about: ${task}`,
                retrieved_context: "More placeholder context from RAG service",
                usage: "Used in the analysis node of the graph"
              },
              {
                query: `Examples related to: ${task}`,
                retrieved_context: "Example context from RAG service",
                usage: "Used in the solution formulation node"
              }
            ],
            metrics: {
              time_taken: 3.5,
              tokens_used: 2200,
              rag_calls: 3
            }
          });
        }, 3500);
      });
      
      const [crewai, autogen, langgraph] = await Promise.all([
        crewaiPromise,
        autogenPromise,
        langgraphPromise
      ]);
      
      setResults({
        crewai,
        autogen,
        langgraph
      });
    } catch (error) {
      console.error('Error running agents:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Agentic AI RAG Benchmark
        </Typography>
        
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Task Input
          </Typography>
          <TextField
            fullWidth
            label="Enter a task for the agents"
            multiline
            rows={3}
            value={task}
            onChange={(e) => setTask(e.target.value)}
            variant="outlined"
            sx={{ mb: 2 }}
          />
          <Button 
            variant="contained" 
            onClick={handleSubmit}
            disabled={loading || !task}
          >
            {loading ? <CircularProgress size={24} /> : 'Run Agents'}
          </Button>
        </Paper>
        
        {(results.crewai || results.autogen || results.langgraph) && (
          <Paper sx={{ width: '100%' }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              aria-label="agent results tabs"
              centered
            >
              <Tab label="CrewAI" />
              <Tab label="AutoGen" />
              <Tab label="LangGraph" />
              <Tab label="Comparison" />
            </Tabs>
            
            <TabPanel value={tabValue} index={0}>
              {results.crewai ? (
                <AgentResultPanel result={results.crewai} />
              ) : (
                <Typography>No results available</Typography>
              )}
            </TabPanel>
            
            <TabPanel value={tabValue} index={1}>
              {results.autogen ? (
                <AgentResultPanel result={results.autogen} />
              ) : (
                <Typography>No results available</Typography>
              )}
            </TabPanel>
            
            <TabPanel value={tabValue} index={2}>
              {results.langgraph ? (
                <AgentResultPanel result={results.langgraph} />
              ) : (
                <Typography>No results available</Typography>
              )}
            </TabPanel>
            
            <TabPanel value={tabValue} index={3}>
              {(results.crewai && results.autogen && results.langgraph) ? (
                <ComparisonPanel 
                  crewai={results.crewai}
                  autogen={results.autogen}
                  langgraph={results.langgraph}
                />
              ) : (
                <Typography>Complete results not available for comparison</Typography>
              )}
            </TabPanel>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

function AgentResultPanel({ result }: { result: AgentResponse }) {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Result
      </Typography>
      <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
        <Typography>{result.result}</Typography>
      </Paper>
      
      <Typography variant="h6" gutterBottom>
        Reasoning
      </Typography>
      <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
        <Typography>{result.reasoning}</Typography>
      </Paper>
      
      <Typography variant="h6" gutterBottom>
        RAG Queries
      </Typography>
      {result.rag_queries.map((query, index) => (
        <Paper key={index} variant="outlined" sx={{ p: 2, mb: 2 }}>
          <Typography variant="subtitle1">Query: {query.query}</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>Context: {query.retrieved_context}</Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>Usage: {query.usage}</Typography>
        </Paper>
      ))}
      
      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Metrics
      </Typography>
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Typography>Time taken: {result.metrics.time_taken.toFixed(2)}s</Typography>
        <Typography>Tokens used: {result.metrics.tokens_used}</Typography>
        <Typography>RAG calls: {result.metrics.rag_calls}</Typography>
      </Paper>
    </Box>
  );
}

function ComparisonPanel({ 
  crewai, 
  autogen, 
  langgraph 
}: { 
  crewai: AgentResponse; 
  autogen: AgentResponse; 
  langgraph: AgentResponse; 
}) {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Results Comparison
      </Typography>
      
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={4}>
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2, 
              height: '100%',
              backgroundColor: '#f5f5f5'
            }}
          >
            <Typography variant="subtitle1" gutterBottom>CrewAI</Typography>
            <Typography variant="body2">{crewai.result}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2, 
              height: '100%',
              backgroundColor: '#f5f5f5'
            }}
          >
            <Typography variant="subtitle1" gutterBottom>AutoGen</Typography>
            <Typography variant="body2">{autogen.result}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2, 
              height: '100%',
              backgroundColor: '#f5f5f5'
            }}
          >
            <Typography variant="subtitle1" gutterBottom>LangGraph</Typography>
            <Typography variant="body2">{langgraph.result}</Typography>
          </Paper>
        </Grid>
      </Grid>
      
      <Typography variant="h6" gutterBottom>
        Metrics Comparison
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Paper variant="outlined" sx={{ p: 2 }}>
            <Typography variant="subtitle2">Time taken (seconds)</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>CrewAI:</Typography>
              <Box sx={{ 
                width: `${(crewai.metrics.time_taken / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'primary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {crewai.metrics.time_taken.toFixed(2)}s
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>AutoGen:</Typography>
              <Box sx={{ 
                width: `${(autogen.metrics.time_taken / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'secondary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {autogen.metrics.time_taken.toFixed(2)}s
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>LangGraph:</Typography>
              <Box sx={{ 
                width: `${(langgraph.metrics.time_taken / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'error.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {langgraph.metrics.time_taken.toFixed(2)}s
              </Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={4}>
          <Paper variant="outlined" sx={{ p: 2 }}>
            <Typography variant="subtitle2">Tokens used</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>CrewAI:</Typography>
              <Box sx={{ 
                width: `${(crewai.metrics.tokens_used / 3000) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'primary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {crewai.metrics.tokens_used}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>AutoGen:</Typography>
              <Box sx={{ 
                width: `${(autogen.metrics.tokens_used / 3000) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'secondary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {autogen.metrics.tokens_used}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>LangGraph:</Typography>
              <Box sx={{ 
                width: `${(langgraph.metrics.tokens_used / 3000) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'error.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {langgraph.metrics.tokens_used}
              </Typography>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={4}>
          <Paper variant="outlined" sx={{ p: 2 }}>
            <Typography variant="subtitle2">RAG calls</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>CrewAI:</Typography>
              <Box sx={{ 
                width: `${(crewai.metrics.rag_calls / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'primary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {crewai.metrics.rag_calls}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>AutoGen:</Typography>
              <Box sx={{ 
                width: `${(autogen.metrics.rag_calls / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'secondary.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {autogen.metrics.rag_calls}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              <Typography variant="body2" sx={{ minWidth: 100 }}>LangGraph:</Typography>
              <Box sx={{ 
                width: `${(langgraph.metrics.rag_calls / 5) * 100}%`, 
                maxWidth: '100%',
                height: 20, 
                backgroundColor: 'error.main',
                borderRadius: 1
              }} />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {langgraph.metrics.rag_calls}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default App;
