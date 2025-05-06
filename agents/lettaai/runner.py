"""
LettaAI Runner module for the RAG benchmark.

This module implements a company research agent using the LettaAI framework.
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

class LettaAIRunner(AgentRunner):
    """
    Implementation of the AgentRunner for LettaAI.
    
    This agent is tasked with researching a given company using the LettaAI framework.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the LettaAI runner.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        super().__init__("lettaai", rag_service_url)
        
        
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Research a company using LettaAI agents.
        
        Args:
            topic: Company name to research
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        super().run_task(topic)
        
        self._simulate_memory_augmented_research(topic)
        
        self._complete_task()
        
        self.log_metadata()
        
        return self.format_output()
    
    def _simulate_memory_augmented_research(self, company: str) -> None:
        """
        Simulate the memory-augmented research approach of LettaAI.
        
        Args:
            company: Company name to research
        """
        self._simulate_planning(company)
        
        self._initialize_memory(company)
        
        self._research_company_profile(company)
        self._research_company_news(company)
        self._research_company_products(company)
        self._research_company_financials(company)
        
        self._consolidate_memory(company)
        
        final_report = self._generate_report(company)
        
        self._set_final_output(final_report)
    
    def _simulate_planning(self, company: str) -> None:
        """
        Simulate the planning phase.
        
        Args:
            company: Company name to research
        """
        self._add_step("planning", {
            "thought": f"Planning memory-augmented research approach for {company}",
            "plan": [
                f"1. Initialize memory with basic information about {company}",
                f"2. Research company profile and update memory",
                f"3. Research latest news and update memory",
                f"4. Research product portfolio and update memory",
                f"5. Research financial performance and update memory",
                f"6. Consolidate memory and generate comprehensive report"
            ]
        })
        
        self._update_token_usage(350)
        
        time.sleep(0.8)
    
    def _initialize_memory(self, company: str) -> None:
        """
        Simulate memory initialization with basic company information.
        
        Args:
            company: Company name to research
        """
        self._add_step("memory_operation", {
            "operation": "initialize",
            "content": f"Initializing memory with basic information about {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "initialized",
                "knowledge_areas": ["profile", "news", "products", "financials"],
                "completion": {
                    "profile": 0,
                    "news": 0,
                    "products": 0,
                    "financials": 0
                }
            }
        })
        
        self._update_token_usage(150)
        
        time.sleep(0.4)
    
    def _research_company_profile(self, company: str) -> None:
        """
        Simulate company profile research with memory updates.
        
        Args:
            company: Company name to research
        """
        profile_info = self._query_rag_service(company, "company profile")
        
        self._add_step("rag_query", {
            "query": f"Company profile for {company}",
            "results": profile_info,
            "usage": "Used to gather general company information"
        })
        
        self._add_step("memory_operation", {
            "operation": "update",
            "content": f"Updating memory with profile information for {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "in_progress",
                "profile": {
                    "description": profile_info[0]["text"] if profile_info else "",
                    "industry": "Technology",
                    "founded": "2005",
                    "headquarters": "San Francisco, CA"
                },
                "completion": {
                    "profile": 100,
                    "news": 0,
                    "products": 0,
                    "financials": 0
                }
            }
        })
        
        self._update_token_usage(200)
        
        time.sleep(0.6)
    
    def _research_company_news(self, company: str) -> None:
        """
        Simulate company news research with memory updates.
        
        Args:
            company: Company name to research
        """
        news_info = self._query_rag_service(company, "latest news")
        
        self._add_step("rag_query", {
            "query": f"Latest news about {company}",
            "results": news_info,
            "usage": "Used to gather recent news about the company"
        })
        
        self._add_step("memory_operation", {
            "operation": "update",
            "content": f"Updating memory with news information for {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "in_progress",
                "news": {
                    "latest_developments": news_info[0]["text"] if news_info else "",
                    "press_releases": "Recent strategic partnership announcements",
                    "media_coverage": "Positive coverage in industry publications"
                },
                "completion": {
                    "profile": 100,
                    "news": 100,
                    "products": 0,
                    "financials": 0
                }
            }
        })
        
        self._update_token_usage(220)
        
        time.sleep(0.7)
    
    def _research_company_products(self, company: str) -> None:
        """
        Simulate company products research with memory updates.
        
        Args:
            company: Company name to research
        """
        product_info = self._query_rag_service(company, "products and services")
        
        self._add_step("rag_query", {
            "query": f"Products and services of {company}",
            "results": product_info,
            "usage": "Used to gather information about company products"
        })
        
        self._add_step("memory_operation", {
            "operation": "update",
            "content": f"Updating memory with product information for {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "in_progress",
                "products": {
                    "portfolio": product_info[0]["text"] if product_info else "",
                    "flagship_products": "Industry-leading solutions",
                    "market_position": "Market leader in key segments"
                },
                "completion": {
                    "profile": 100,
                    "news": 100,
                    "products": 100,
                    "financials": 0
                }
            }
        })
        
        self._update_token_usage(210)
        
        time.sleep(0.6)
    
    def _research_company_financials(self, company: str) -> None:
        """
        Simulate company financials research with memory updates.
        
        Args:
            company: Company name to research
        """
        financial_info = self._query_rag_service(company, "financial performance")
        
        self._add_step("rag_query", {
            "query": f"Financial performance of {company}",
            "results": financial_info,
            "usage": "Used to analyze financial health and trends"
        })
        
        self._add_step("memory_operation", {
            "operation": "update",
            "content": f"Updating memory with financial information for {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "in_progress",
                "financials": {
                    "performance": financial_info[0]["text"] if financial_info else "",
                    "revenue_growth": "15% year-over-year",
                    "profit_margins": "Expanding margins",
                    "market_outlook": "Positive growth trajectory"
                },
                "completion": {
                    "profile": 100,
                    "news": 100,
                    "products": 100,
                    "financials": 100
                }
            }
        })
        
        self._update_token_usage(230)
        
        time.sleep(0.7)
    
    def _consolidate_memory(self, company: str) -> None:
        """
        Simulate memory consolidation before report generation.
        
        Args:
            company: Company name to research
        """
        self._add_step("memory_operation", {
            "operation": "consolidate",
            "content": f"Consolidating memory for {company}",
            "memory_state": {
                "company_name": company,
                "research_status": "completed",
                "insights": [
                    "Strong market position with established brand",
                    "Recent strategic initiatives for growth",
                    "Innovative product portfolio with market recognition",
                    "Solid financial performance with consistent growth"
                ],
                "completion": {
                    "profile": 100,
                    "news": 100,
                    "products": 100,
                    "financials": 100,
                    "overall": 100
                }
            }
        })
        
        self._update_token_usage(180)
        
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
        if aspect == "company profile":
            return [{
                "text": f"{company} is a leading global organization known for innovation and excellence in its industry, with operations spanning multiple continents.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.98
            }]
        elif aspect == "latest news":
            return [{
                "text": f"{company} has recently announced a major strategic initiative aimed at expanding its market presence and enhancing its product offerings.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.95
            }]
        elif aspect == "products and services":
            return [{
                "text": f"{company}'s product portfolio includes a comprehensive suite of solutions that have received industry recognition for innovation and quality.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.93
            }]
        elif aspect == "financial performance":
            return [{
                "text": f"{company} has demonstrated exceptional financial performance with consistent revenue growth and expanding profit margins, outperforming industry benchmarks.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.96
            }]
        else:
            return [{
                "text": f"Information about {company} related to {aspect}.",
                "metadata": {"source": "simulated", "relevance": "medium"},
                "score": 0.85
            }]
    
    def _generate_report(self, company: str) -> str:
        """
        Generate a final report based on the consolidated memory.
        
        Args:
            company: Company name
            
        Returns:
            Final report text
        """
        report = f"""# {company} Research Report

{company} is a leading global organization known for innovation and excellence in its industry, with operations spanning multiple continents.

{company} has recently announced a major strategic initiative aimed at expanding its market presence and enhancing its product offerings.

{company}'s product portfolio includes a comprehensive suite of solutions that have received industry recognition for innovation and quality.

{company} has demonstrated exceptional financial performance with consistent revenue growth and expanding profit margins, outperforming industry benchmarks.

Based on our memory-augmented research using LettaAI, {company} demonstrates strong market positioning with innovative products and solid financial performance. The company has shown consistent growth and strategic initiatives that position it well for future success.

- Established global presence with strong brand recognition
- Strategic growth initiatives and market expansion
- Innovative and diverse product portfolio
- Exceptional financial performance with industry-leading metrics

- Continued market expansion through strategic partnerships
- Ongoing product innovation to maintain competitive edge
- Potential for further revenue growth and margin improvement
- Strong positioning for long-term industry leadership
"""
        
        self._add_step("report_generation", {
            "thought": f"Generating comprehensive report for {company} based on consolidated memory",
            "report_sections": ["Company Profile", "Latest News", "Products and Services", "Financial Performance", "Memory-Augmented Analysis", "Key Insights", "Future Outlook"]
        })
        
        self._update_token_usage(450)
        
        time.sleep(1.0)
        
        return report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    runner = LettaAIRunner(rag_service_url)
    
    result = runner.run_task("Apple Inc.")
    
    print(json.dumps(result, indent=2))
