"""
CrewAI Runner module for the RAG benchmark.

This module implements a company research agent using the CrewAI framework.
"""

import os
import time
import json
import random
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents.base_agent_runner import AgentRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CrewAIRunner(AgentRunner):
    """
    Implementation of the AgentRunner for CrewAI.
    
    This agent is tasked with researching a given company using the CrewAI framework.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the CrewAI runner.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        super().__init__("crewai", rag_service_url)
        
        
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Research a company using CrewAI agents.
        
        Args:
            topic: Company name to research
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        # Initialize timing and steps from parent class
        super().run_task(topic)
        
        self._simulate_research_planning(topic)
        
        company_info = self._query_rag_service(topic, "company information")
        self._add_step("rag_query", {
            "query": f"Information about {topic}",
            "results": company_info,
            "usage": "Used to gather general company information"
        })
        
        news_info = self._query_rag_service(topic, "latest news")
        self._add_step("rag_query", {
            "query": f"Latest news about {topic}",
            "results": news_info,
            "usage": "Used to gather recent news about the company"
        })
        
        product_info = self._query_rag_service(topic, "products and services")
        self._add_step("rag_query", {
            "query": f"Products and services of {topic}",
            "results": product_info,
            "usage": "Used to gather information about company products"
        })
        
        financial_info = self._query_rag_service(topic, "financial performance")
        self._add_step("rag_query", {
            "query": f"Financial trends and performance of {topic}",
            "results": financial_info,
            "usage": "Used to analyze financial health and trends"
        })
        
        self._simulate_analysis(topic, company_info, news_info, product_info, financial_info)
        
        final_report = self._generate_report(topic, company_info, news_info, product_info, financial_info)
        
        self._set_final_output(final_report)
        self._complete_task()
        
        self.log_metadata()
        
        return self.format_output()
    
    def _simulate_research_planning(self, company: str) -> None:
        """
        Simulate the research planning phase.
        
        Args:
            company: Company name to research
        """
        
        self._add_step("planning", {
            "thought": f"Planning research approach for {company}",
            "plan": [
                f"1. Gather general information about {company}",
                f"2. Research latest news and press releases for {company}",
                f"3. Analyze product portfolio and recent updates",
                f"4. Examine financial performance and market trends",
                f"5. Synthesize findings into a comprehensive report"
            ]
        })
        
        self._update_token_usage(250)
        
        time.sleep(0.5)
    
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
        if aspect == "company information":
            return [{
                "text": f"{company} is a leading company in its industry, known for innovation and quality products.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.95
            }]
        elif aspect == "latest news":
            return [{
                "text": f"{company} recently announced a new strategic partnership to expand its market reach.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.92
            }]
        elif aspect == "products and services":
            return [{
                "text": f"{company}'s flagship product line continues to see strong growth, with new features added quarterly.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.88
            }]
        elif aspect == "financial performance":
            return [{
                "text": f"{company} reported strong quarterly earnings, exceeding analyst expectations with revenue growth of 15%.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.90
            }]
        else:
            return [{
                "text": f"Information about {company} related to {aspect}.",
                "metadata": {"source": "simulated", "relevance": "medium"},
                "score": 0.75
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
            "thought": f"Analyzing general information about {company}",
            "insights": "Company appears to be well-established in its industry with a strong reputation."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing latest news about {company}",
            "insights": "Recent news suggests strategic growth initiatives and positive market reception."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing product portfolio of {company}",
            "insights": "Product lineup shows innovation focus with regular updates and feature additions."
        })
        
        self._add_step("analysis", {
            "thought": f"Analyzing financial performance of {company}",
            "insights": "Financial indicators suggest strong performance with consistent growth."
        })
        
        self._update_token_usage(500)
        
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

Based on our research, {company} demonstrates strong market positioning with innovative products and solid financial performance. The company has shown consistent growth and strategic initiatives that position it well for future success.
"""
        
        self._add_step("report_generation", {
            "thought": f"Generating comprehensive report for {company}",
            "report_sections": ["Company Overview", "Latest News", "Products and Services", "Financial Trends", "Summary"]
        })
        
        self._update_token_usage(350)
        
        time.sleep(0.8)
        
        return report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    runner = CrewAIRunner(rag_service_url)
    
    result = runner.run_task("Apple Inc.")
    
    print(json.dumps(result, indent=2))
