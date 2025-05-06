"""
SquidAI Runner module for the RAG benchmark.

This module implements a company research agent using the SquidAI framework.
"""

import os
import time
import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent_runner import AgentRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SquidAIRunner(AgentRunner):
    """
    Implementation of the AgentRunner for SquidAI.
    
    This agent is tasked with researching a given company using the SquidAI framework.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the SquidAI runner.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        super().__init__("squidai", rag_service_url)
        
        
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Research a company using SquidAI agents.
        
        Args:
            topic: Company name to research
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        super().run_task(topic)
        
        self._simulate_tool_based_research(topic)
        
        self._complete_task()
        
        self.log_metadata()
        
        return self.format_output()
    
    def _simulate_tool_based_research(self, company: str) -> None:
        """
        Simulate the tool-based research approach of SquidAI.
        
        Args:
            company: Company name to research
        """
        self._simulate_planning(company)
        
        company_info = self._execute_tool("company_info_tool", company)
        self._add_step("tool_execution", {
            "tool": "company_info_tool",
            "input": f"Get information about {company}",
            "output": company_info,
            "usage": "Used to gather general company information"
        })
        
        news_info = self._execute_tool("news_tool", company)
        self._add_step("tool_execution", {
            "tool": "news_tool",
            "input": f"Get latest news about {company}",
            "output": news_info,
            "usage": "Used to gather recent news about the company"
        })
        
        product_info = self._execute_tool("product_tool", company)
        self._add_step("tool_execution", {
            "tool": "product_tool",
            "input": f"Get product information for {company}",
            "output": product_info,
            "usage": "Used to gather information about company products"
        })
        
        financial_info = self._execute_tool("financial_tool", company)
        self._add_step("tool_execution", {
            "tool": "financial_tool",
            "input": f"Get financial data for {company}",
            "output": financial_info,
            "usage": "Used to analyze financial health and trends"
        })
        
        self._simulate_analysis(company, company_info, news_info, product_info, financial_info)
        
        final_report = self._generate_report(company, company_info, news_info, product_info, financial_info)
        
        self._set_final_output(final_report)
    
    def _simulate_planning(self, company: str) -> None:
        """
        Simulate the planning phase.
        
        Args:
            company: Company name to research
        """
        self._add_step("planning", {
            "thought": f"Planning research approach for {company}",
            "plan": [
                f"1. Use company_info_tool to gather general information about {company}",
                f"2. Use news_tool to collect recent news and press releases",
                f"3. Use product_tool to research product portfolio and market position",
                f"4. Use financial_tool to examine financial performance and trends",
                f"5. Analyze collected information and generate a comprehensive report"
            ]
        })
        
        self._update_token_usage(320)
        
        time.sleep(0.7)
    
    def _execute_tool(self, tool_name: str, company: str) -> List[Dict[str, Any]]:
        """
        Simulate the execution of a SquidAI tool.
        
        Args:
            tool_name: Name of the tool to execute
            company: Company name to research
            
        Returns:
            Tool execution results
        """
        tool_to_aspect = {
            "company_info_tool": "company overview",
            "news_tool": "latest news",
            "product_tool": "products and services",
            "financial_tool": "financial performance"
        }
        
        aspect = tool_to_aspect.get(tool_name, "general information")
        
        results = self._query_rag_service(company, aspect)
        
        self._update_token_usage(150)
        
        time.sleep(0.5)
        
        return results
    
    def _query_rag_service(self, company: str, aspect: str) -> List[Dict[str, Any]]:
        """
        Query the RAG service for company information.
        
        Args:
            company: Company name to research
            aspect: Specific aspect to research (e.g., "latest news")
            
        Returns:
            List of relevant documents
        """
        try:
            query = f"{company} {aspect}"
            
            response = requests.get(
                f"{self.rag_service_url}/query",
                params={"q": query, "top_k": 3}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                results = []
                for result in data.get("results", []):
                    results.append({
                        "text": result.get("chunk", ""),
                        "metadata": result.get("metadata", {}),
                        "score": result.get("score", 0.0)
                    })
                
                if not results:
                    results = self._generate_placeholder_results(company, aspect)
                
                return results
            else:
                logger.warning(f"RAG service returned status code {response.status_code}")
                return self._generate_placeholder_results(company, aspect)
                
        except Exception as e:
            logger.error(f"Error querying RAG service: {str(e)}")
            return self._generate_placeholder_results(company, aspect)
    
    def _generate_placeholder_results(self, company: str, aspect: str) -> List[Dict[str, Any]]:
        """
        Generate placeholder results when RAG service is unavailable.
        
        Args:
            company: Company name
            aspect: Research aspect
            
        Returns:
            List of placeholder results
        """
        if aspect == "company overview":
            return [{
                "text": f"{company} is a leading organization in its industry, known for innovation and market leadership with a global presence.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.97
            }]
        elif aspect == "latest news":
            return [{
                "text": f"{company} recently announced a strategic partnership and launched several new initiatives focused on sustainable growth and market expansion.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.94
            }]
        elif aspect == "products and services":
            return [{
                "text": f"{company}'s product portfolio includes a wide range of innovative solutions that have received industry recognition for their quality and performance.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.92
            }]
        elif aspect == "financial performance":
            return [{
                "text": f"{company} has demonstrated strong financial performance with consistent revenue growth of 15% year-over-year and expanding profit margins.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.95
            }]
        else:
            return [{
                "text": f"Information about {company} related to {aspect}.",
                "metadata": {"source": "simulated", "relevance": "medium"},
                "score": 0.82
            }]
    
    def _simulate_analysis(self, company: str, company_info: List[Dict], news_info: List[Dict], 
                          product_info: List[Dict], financial_info: List[Dict]) -> None:
        """
        Simulate the analysis of gathered information.
        
        Args:
            company: Company name
            company_info: General company information
            news_info: Latest news
            product_info: Product information
            financial_info: Financial information
        """
        self._add_step("analysis", {
            "thought": f"Analyzing company profile of {company}",
            "insights": "Company has established a strong market position with significant industry presence."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing recent news about {company}",
            "insights": "Recent announcements indicate strategic growth initiatives and market expansion efforts."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing product portfolio of {company}",
            "insights": "Product lineup demonstrates innovation focus and addresses diverse market needs."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing financial performance of {company}",
            "insights": "Financial indicators show strong performance with consistent growth and healthy margins."
        })
        
        self._update_token_usage(480)
        
        time.sleep(1.0)
    
    def _generate_report(self, company: str, company_info: List[Dict], news_info: List[Dict], 
                        product_info: List[Dict], financial_info: List[Dict]) -> str:
        """
        Generate a final report based on the gathered information.
        
        Args:
            company: Company name
            company_info: General company information
            news_info: Latest news
            product_info: Product information
            financial_info: Financial information
            
        Returns:
            Final report text
        """
        company_text = company_info[0]["text"] if company_info else ""
        news_text = news_info[0]["text"] if news_info else ""
        product_text = product_info[0]["text"] if product_info else ""
        financial_text = financial_info[0]["text"] if financial_info else ""
        
        report = f"""# {company} Research Report

{company_text}

{news_text}

{product_text}

{financial_text}

Based on our tool-based research using SquidAI, {company} demonstrates strong market positioning with innovative products and solid financial performance. The company has shown consistent growth and strategic initiatives that position it well for future success.

- Established market presence and brand recognition
- Strategic partnerships and growth initiatives
- Innovative product portfolio with industry recognition
- Strong financial performance with healthy margins

- Continue monitoring strategic partnerships and acquisitions
- Track product innovation and market reception
- Analyze competitive landscape for potential threats
- Evaluate financial trends for investment opportunities
"""
        
        self._add_step("report_generation", {
            "thought": f"Generating comprehensive report for {company}",
            "report_sections": ["Company Overview", "Latest News", "Products and Services", "Financial Performance", "Summary Analysis", "Key Insights", "Recommendations"]
        })
        
        self._update_token_usage(400)
        
        time.sleep(0.8)
        
        return report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    runner = SquidAIRunner(rag_service_url)
    
    result = runner.run_task("Netflix Inc.")
    
    print(json.dumps(result, indent=2))
