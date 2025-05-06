import React, { useState } from 'react';
import axios from 'axios';

interface AgentStep {
  type: string;
  timestamp: string;
  details: any;
}

interface AgentResponse {
  agent_name: string;
  final_output: string;
  steps: AgentStep[];
  token_usage: number;
  response_time: number;
}

interface AgentResults {
  crewai?: AgentResponse;
  autogen?: AgentResponse;
  langgraph?: AgentResponse;
  googleadk?: AgentResponse;
  squidai?: AgentResponse;
  lettaai?: AgentResponse;
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
      {value === index && <div className="p-4">{children}</div>}
    </div>
  );
}

interface CollapsibleProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function Collapsible({ title, children, defaultOpen = false }: CollapsibleProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border rounded-md mb-4">
      <button
        className="w-full text-left p-3 font-medium flex justify-between items-center bg-gray-50 hover:bg-gray-100 rounded-t-md"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>{title}</span>
        <span>{isOpen ? '▼' : '►'}</span>
      </button>
      {isOpen && <div className="p-3 border-t">{children}</div>}
    </div>
  );
}

function App() {
  const [company, setCompany] = useState('');
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [results, setResults] = useState<AgentResults>({});

  const companyOptions = [
    'Apple Inc.',
    'Microsoft Corporation',
    'Amazon.com Inc.',
    'Tesla Inc.',
    'Netflix Inc.',
    'Google LLC',
  ];

  const handleTabChange = (newValue: number) => {
    setTabValue(newValue);
  };

  const handleRunAgents = async () => {
    if (!company) return;
    
    setLoading(true);
    
    try {
      
      const crewaiPromise = simulateAgentRun('crewai', company);
      const autogenPromise = simulateAgentRun('autogen', company);
      const langgraphPromise = simulateAgentRun('langgraph', company);
      const googleadkPromise = simulateAgentRun('googleadk', company);
      const squidaiPromise = simulateAgentRun('squidai', company);
      const lettaaiPromise = simulateAgentRun('lettaai', company);
      
      const [crewai, autogen, langgraph, googleadk, squidai, lettaai] = await Promise.all([
        crewaiPromise,
        autogenPromise,
        langgraphPromise,
        googleadkPromise,
        squidaiPromise,
        lettaaiPromise
      ]);
      
      setResults({
        crewai,
        autogen,
        langgraph,
        googleadk,
        squidai,
        lettaai
      });
    } catch (error) {
      console.error('Error running agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const simulateAgentRun = (agentName: string, company: string): Promise<AgentResponse> => {
    const timings: Record<string, number> = {
      crewai: 2300,
      autogen: 2800,
      langgraph: 3500,
      googleadk: 3000,
      squidai: 2600,
      lettaai: 3200
    };
    
    const tokenUsage: Record<string, number> = {
      crewai: 1500,
      autogen: 1800,
      langgraph: 2200,
      googleadk: 1900,
      squidai: 1600,
      lettaai: 2000
    };
    
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          agent_name: agentName,
          final_output: `${agentName.charAt(0).toUpperCase() + agentName.slice(1)} analysis for ${company}: This company has shown strong performance in recent quarters with innovative product launches and strategic partnerships. Market position remains competitive with opportunities for growth in emerging markets.`,
          steps: [
            {
              type: 'planning',
              timestamp: new Date().toISOString(),
              details: {
                thought: `Planning research approach for ${company}`,
                plan: [
                  `1. Gather general information about ${company}`,
                  `2. Collect recent news and press releases`,
                  `3. Research product portfolio and market position`,
                  `4. Examine financial performance and trends`,
                  `5. Analyze collected information and generate a report`
                ]
              }
            },
            {
              type: 'rag_query',
              timestamp: new Date().toISOString(),
              details: {
                query: `${company} company overview`,
                results: [
                  {
                    text: `${company} is a leading organization in its industry, known for innovation and market leadership.`,
                    score: 0.92
                  }
                ]
              }
            },
            {
              type: 'analysis',
              timestamp: new Date().toISOString(),
              details: {
                thought: `Analyzing company profile of ${company}`,
                insights: "Company has established a strong market position with significant industry presence."
              }
            }
          ],
          token_usage: tokenUsage[agentName],
          response_time: timings[agentName] / 1000
        });
      }, timings[agentName]);
    });
  };

  const getAgentNames = (): string[] => {
    return Object.keys(results);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">
          Agentic AI RAG Benchmark
        </h1>
        
        {/* Input section */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">
            Company Research
          </h2>
          
          <div className="mb-4">
            <label htmlFor="company-select" className="block text-sm font-medium text-gray-700 mb-1">
              Select a company to research
            </label>
            <div className="flex gap-2">
              <select
                id="company-select"
                className="flex-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
              >
                <option value="">-- Select a company --</option>
                {companyOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
              
              <input
                type="text"
                placeholder="Or enter a custom company name"
                className="flex-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
                value={company === '' || companyOptions.includes(company) ? '' : company}
                onChange={(e) => setCompany(e.target.value)}
              />
            </div>
          </div>
          
          <button
            className={`px-4 py-2 rounded-md font-medium ${
              loading || !company
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
            onClick={handleRunAgents}
            disabled={loading || !company}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Running Agents...
              </span>
            ) : (
              'Run All Agents'
            )}
          </button>
        </div>
        
        {/* Results section */}
        {getAgentNames().length > 0 && (
          <div className="bg-white rounded-lg shadow-md">
            {/* Tabs */}
            <div className="border-b">
              <div className="flex overflow-x-auto">
                {getAgentNames().map((agentName, index) => (
                  <button
                    key={agentName}
                    className={`px-4 py-3 font-medium text-sm ${
                      tabValue === index
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                    onClick={() => handleTabChange(index)}
                  >
                    {agentName.charAt(0).toUpperCase() + agentName.slice(1)}
                  </button>
                ))}
                <button
                  className={`px-4 py-3 font-medium text-sm ${
                    tabValue === getAgentNames().length
                      ? 'border-b-2 border-blue-500 text-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                  onClick={() => handleTabChange(getAgentNames().length)}
                >
                  Comparison
                </button>
              </div>
            </div>
            
            {/* Individual agent panels */}
            {getAgentNames().map((agentName, index) => (
              <TabPanel key={agentName} value={tabValue} index={index}>
                <AgentResultPanel result={results[agentName as keyof AgentResults]!} />
              </TabPanel>
            ))}
            
            {/* Comparison panel */}
            <TabPanel value={tabValue} index={getAgentNames().length}>
              <ComparisonPanel results={results} />
            </TabPanel>
          </div>
        )}
      </div>
    </div>
  );
}

function AgentResultPanel({ result }: { result: AgentResponse }) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4 text-gray-800">
        {result.agent_name.charAt(0).toUpperCase() + result.agent_name.slice(1)} Results
      </h3>
      
      <div className="bg-gray-50 p-4 rounded-md mb-6 border">
        <h4 className="font-medium mb-2 text-gray-700">Final Output</h4>
        <p className="text-gray-800 whitespace-pre-line">{result.final_output}</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-50 p-4 rounded-md border">
          <h4 className="font-medium mb-2 text-gray-700">Response Time</h4>
          <p className="text-2xl font-bold text-blue-600">{result.response_time.toFixed(2)}s</p>
        </div>
        
        <div className="bg-gray-50 p-4 rounded-md border">
          <h4 className="font-medium mb-2 text-gray-700">Token Usage</h4>
          <p className="text-2xl font-bold text-green-600">{result.token_usage.toLocaleString()}</p>
        </div>
      </div>
      
      <Collapsible title="Execution Steps" defaultOpen={false}>
        <div className="space-y-4">
          {result.steps.map((step, index) => (
            <div key={index} className="border rounded-md p-3 bg-gray-50">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium text-gray-800">{step.type.charAt(0).toUpperCase() + step.type.slice(1)}</span>
                <span className="text-xs text-gray-500">{new Date(step.timestamp).toLocaleTimeString()}</span>
              </div>
              <div className="text-sm">
                {Object.entries(step.details).map(([key, value]) => (
                  <div key={key} className="mb-1">
                    <span className="font-medium">{key.charAt(0).toUpperCase() + key.slice(1)}: </span>
                    {typeof value === 'string' ? (
                      <span>{value}</span>
                    ) : Array.isArray(value) ? (
                      <ul className="list-disc pl-5 mt-1">
                        {value.map((item, i) => (
                          <li key={i} className="text-gray-700">
                            {typeof item === 'string' ? item : JSON.stringify(item)}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <pre className="bg-gray-100 p-2 rounded mt-1 text-xs overflow-auto">
                        {JSON.stringify(value, null, 2)}
                      </pre>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Collapsible>
    </div>
  );
}

function ComparisonPanel({ results }: { results: AgentResults }) {
  const agentNames = Object.keys(results);
  
  const maxResponseTime = Math.max(...agentNames.map(name => results[name as keyof AgentResults]?.response_time || 0));
  const maxTokenUsage = Math.max(...agentNames.map(name => results[name as keyof AgentResults]?.token_usage || 0));
  
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4 text-gray-800">
        Agent Comparison
      </h3>
      
      <Collapsible title="Response Time Comparison" defaultOpen={true}>
        <div className="space-y-3">
          {agentNames.map(name => {
            const agent = results[name as keyof AgentResults]!;
            const percentage = (agent.response_time / maxResponseTime) * 100;
            
            return (
              <div key={name} className="flex items-center">
                <div className="w-32 text-sm font-medium text-gray-700">{name.charAt(0).toUpperCase() + name.slice(1)}:</div>
                <div className="flex-1 h-6 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-600 rounded-full"
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
                <div className="w-20 text-right text-sm ml-2">{agent.response_time.toFixed(2)}s</div>
              </div>
            );
          })}
        </div>
      </Collapsible>
      
      <Collapsible title="Token Usage Comparison" defaultOpen={true}>
        <div className="space-y-3">
          {agentNames.map(name => {
            const agent = results[name as keyof AgentResults]!;
            const percentage = (agent.token_usage / maxTokenUsage) * 100;
            
            return (
              <div key={name} className="flex items-center">
                <div className="w-32 text-sm font-medium text-gray-700">{name.charAt(0).toUpperCase() + name.slice(1)}:</div>
                <div className="flex-1 h-6 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-green-600 rounded-full"
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
                <div className="w-20 text-right text-sm ml-2">{agent.token_usage.toLocaleString()}</div>
              </div>
            );
          })}
        </div>
      </Collapsible>
      
      <Collapsible title="Output Comparison" defaultOpen={true}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agentNames.map(name => {
            const agent = results[name as keyof AgentResults]!;
            
            return (
              <div key={name} className="border rounded-md p-4 bg-gray-50">
                <h4 className="font-medium mb-2 text-gray-800">{name.charAt(0).toUpperCase() + name.slice(1)}</h4>
                <p className="text-sm text-gray-700">{agent.final_output}</p>
              </div>
            );
          })}
        </div>
      </Collapsible>
    </div>
  );
}

export default App;
