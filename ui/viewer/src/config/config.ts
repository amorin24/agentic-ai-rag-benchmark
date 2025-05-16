/**
 * Application configuration
 * 
 * This file centralizes all configuration values that were previously hardcoded
 * throughout the application.
 */

export const API_CONFIG = {
  AGENT_RUNNER_URL: process.env.REACT_APP_AGENT_RUNNER_URL || 'http://localhost:8001',
  
  RAG_SERVICE_URL: process.env.REACT_APP_RAG_SERVICE_URL || 'http://localhost:8000',
};

export const AGENT_FRAMEWORKS = {
  ALL_FRAMEWORKS: [
    'crewai',
    'autogen',
    'langgraph',
    'googleadk',
    'squidai',
    'lettaai',
    'portiaai',
    'h2oai',
    'uipath'
  ],
  
  MOCK_FRAMEWORKS: ['squidai', 'lettaai', 'h2oai'],
  
  get REAL_FRAMEWORKS() {
    return this.ALL_FRAMEWORKS.filter(
      framework => !this.MOCK_FRAMEWORKS.includes(framework)
    );
  }
};

export const COMPANY_OPTIONS = [
  'Apple Inc.',
  'Microsoft Corporation',
  'Amazon.com Inc.',
  'Tesla Inc.',
  'Netflix Inc.',
  'Google LLC',
];

export const UI_CONFIG = {
  DEFAULT_TAB: 0,
  
  MAX_LOGS: 1000,
  
  LOG_PANEL_HEIGHT: '300px',
};
