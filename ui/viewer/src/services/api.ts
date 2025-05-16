import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import { API_CONFIG } from '../config/config';

const agentRunnerApi = axios.create({
  baseURL: API_CONFIG.AGENT_RUNNER_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

const ragServiceApi = axios.create({
  baseURL: API_CONFIG.RAG_SERVICE_URL,
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

const addRequestInterceptor = (instance: typeof agentRunnerApi) => {
  instance.interceptors.request.use(
    (config) => {
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

const addResponseInterceptor = (instance: typeof agentRunnerApi) => {
  instance.interceptors.response.use(
    (response) => {
      return response;
    },
    (error: AxiosError) => {
      const formattedError = {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
        config: {
          url: error.config?.url,
          method: error.config?.method,
        },
      };
      
      return Promise.reject(formattedError);
    }
  );
};

addRequestInterceptor(agentRunnerApi);
addRequestInterceptor(ragServiceApi);
addResponseInterceptor(agentRunnerApi);
addResponseInterceptor(ragServiceApi);

export interface AgentStep {
  type: string;
  timestamp: string;
  details: any;
}

export interface AgentResponse {
  agent_name: string;
  final_output: string;
  steps: AgentStep[];
  token_usage: number;
  response_time: number;
}

export const agentRunnerService = {
  async runAgent(agentName: string, topic: string): Promise<AgentResponse> {
    try {
      const response = await agentRunnerApi.post('/run', {
        agent: agentName,
        topic: topic
      });
      
      return response.data;
    } catch (error) {
      console.error(`Error running ${agentName} agent:`, error);
      throw error;
    }
  },
  
  async getAvailableAgents(): Promise<string[]> {
    try {
      const response = await agentRunnerApi.get('/frameworks');
      return response.data.frameworks || [];
    } catch (error) {
      console.error('Error fetching available agents:', error);
      throw error;
    }
  }
};

export interface QueryResult {
  chunk: string;
  metadata: any;
  score: number;
}

export interface QueryResponse {
  query: string;
  results: QueryResult[];
  total_chunks: number;
  time_taken: number;
}

export interface StatusResponse {
  status: string;
  vector_store_size: number;
  last_ingest: string | null;
}

export const ragService = {
  async query(q: string, topK: number = 5): Promise<QueryResponse> {
    try {
      const response = await ragServiceApi.get('/query', {
        params: { q, top_k: topK }
      });
      return response.data;
    } catch (error) {
      console.error('Error querying RAG service:', error);
      throw error;
    }
  },
  
  async ingestText(text: string, metadata: any = {}): Promise<any> {
    try {
      const response = await ragServiceApi.post('/ingest', {
        text,
        metadata
      });
      return response.data;
    } catch (error) {
      console.error('Error ingesting text to RAG service:', error);
      throw error;
    }
  },
  
  async ingestUrl(url: string, metadata: any = {}): Promise<any> {
    try {
      const response = await ragServiceApi.post('/ingest', {
        url,
        metadata
      });
      return response.data;
    } catch (error) {
      console.error('Error ingesting URL to RAG service:', error);
      throw error;
    }
  },
  
  async getStatus(): Promise<StatusResponse> {
    try {
      const response = await ragServiceApi.get('/status');
      return response.data;
    } catch (error) {
      console.error('Error getting RAG service status:', error);
      throw error;
    }
  }
};
