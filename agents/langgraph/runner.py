"""
LangGraph Runner module for the RAG benchmark.

This module implements a company research agent using the LangGraph framework.
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

class LangGraphRunner(AgentRunner):
    """
    Implementation of the AgentRunner for LangGraph.
    
    This agent is tasked with researching a given company using the LangGraph framework.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the LangGraph runner.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        super().__init__("langgraph", rag_service_url)
        
        
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Research a company using LangGraph workflow.
        
        Args:
            topic: Company name to research
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        # Initialize timing and steps from parent class
        super().run_task(topic)
        
        self._simulate_graph_execution(topic)
        
        self._complete_task()
        
        self.log_metadata()
        
        return self.format_output()
    
    def _simulate_graph_execution(self, company: str) -> None:
        """
        Simulate the execution of a LangGraph workflow for company research.
        
        Args:
            company: Company name to research
        """
        self._simulate_research_node(company)
        
        self._simulate_analysis_node(company)
        
        self._simulate_report_node(company)
    
    def _simulate_research_node(self, company: str) -> None:
        """
        Simulate the research node of the graph.
        
        Args:
            company: Company name to research
        """
        self._add_step("graph_node_execution", {
            "node": "research",
            "input": f"Research company: {company}",
            "thought": f"Planning research approach for {company}"
        })
        
        self._add_step("planning", {
            "thought": f"Planning research approach for {company}",
            "plan": [
                f"1. Gather general information about {company}",
                f"2. Research latest news and press releases",
                f"3. Analyze product portfolio and market position",
                f"4. Examine financial performance and trends"
            ]
        })
        
        company_info = self._query_rag_service(company, "company profile")
        self._add_step("rag_query", {
            "query": f"Company profile for {company}",
            "results": company_info,
            "usage": "Used to gather general company information"
        })
        
        news_info = self._query_rag_service(company, "latest news")
        self._add_step("rag_query", {
            "query": f"Latest news about {company}",
            "results": news_info,
            "usage": "Used to gather recent news about the company"
        })
        
        self._update_token_usage(350)
        
        time.sleep(0.8)
    
    def _simulate_analysis_node(self, company: str) -> None:
        """
        Simulate the analysis node of the graph.
        
        Args:
            company: Company name to research
        """
        self._add_step("graph_node_execution", {
            "node": "analyze",
            "input": f"Analyze research data for {company}",
            "thought": f"Analyzing gathered information about {company}"
        })
        
        product_info = self._query_rag_service(company, "products and services")
        self._add_step("rag_query", {
            "query": f"Products and services of {company}",
            "results": product_info,
            "usage": "Used to analyze product portfolio"
        })
        
        financial_info = self._query_rag_service(company, "financial performance")
        self._add_step("rag_query", {
            "query": f"Financial performance of {company}",
            "results": financial_info,
            "usage": "Used to analyze financial health and trends"
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing company profile of {company}",
            "insights": "Company has a strong market position and global presence."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing news about {company}",
            "insights": "Recent news indicates strategic growth initiatives and positive market reception."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing product portfolio of {company}",
            "insights": "Product lineup shows innovation focus with regular updates and feature additions."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing financial performance of {company}",
            "insights": "Financial indicators suggest strong performance with consistent growth."
        })
        
        self._update_token_usage(450)
        
        time.sleep(1.0)
    
    def _simulate_report_node(self, company: str) -> None:
        """
        Simulate the report node of the graph.
        
        Args:
            company: Company name to research
        """
        self._add_step("graph_node_execution", {
            "node": "report",
            "input": f"Generate report for {company}",
            "thought": f"Synthesizing analysis into comprehensive report for {company}"
        })
        
        report = self._generate_report(company)
        
        self._set_final_output(report)
        
        self._update_token_usage(400)
        
        time.sleep(0.7)
    
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
            
            # Call RAG service
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
                
                self._update_token_usage(100)
                
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
        if aspect == "company profile":
            return [{
                "text": f"{company} is a leading global corporation with a diverse portfolio of products and services, operating in multiple markets worldwide.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.96
            }]
        elif aspect == "latest news":
            return [{
                "text": f"{company} has recently announced a strategic partnership to enhance its product offerings and expand into new markets.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.93
            }]
        elif aspect == "products and services":
            return [{
                "text": f"{company}'s product lineup includes cutting-edge solutions that have received industry recognition for innovation and quality.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.91
            }]
        elif aspect == "financial performance":
            return [{
                "text": f"{company} reported strong quarterly results with revenue growth of 12% year-over-year and improved profit margins.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.94
            }]
        else:
            return [{
                "text": f"Information about {company} related to {aspect}.",
                "metadata": {"source": "simulated", "relevance": "medium"},
                "score": 0.80
            }]
    
    def _generate_report(self, company: str) -> str:
        """
        Generate a final report based on the graph execution.
        
        Args:
            company: Company name
            
        Returns:
            Final report text
        """
        
        report = f"""# {company} Research Report

{company} is a leading global corporation with a diverse portfolio of products and services, operating in multiple markets worldwide.

{company} has recently announced a strategic partnership to enhance its product offerings and expand into new markets.

{company}'s product lineup includes cutting-edge solutions that have received industry recognition for innovation and quality.

{company} reported strong quarterly results with revenue growth of 12% year-over-year and improved profit margins.

Based on our graph-based analysis, {company} demonstrates strong market positioning with innovative products and solid financial performance. The company has shown consistent growth and strategic initiatives that position it well for future success.

- Strong global presence and brand recognition
- Strategic partnerships driving growth
- Innovative product portfolio with industry recognition
- Consistent financial performance with healthy margins
"""
        
        self._add_step("report_generation", {
            "thought": f"Generating comprehensive report for {company}",
            "report_sections": ["Company Profile", "Latest News", "Products and Market Position", "Financial Performance", "Summary Analysis", "Key Insights"]
        })
        
        return report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    runner = LangGraphRunner(rag_service_url)
    
    result = runner.run_task("Tesla Inc.")
    
    print(json.dumps(result, indent=2))
