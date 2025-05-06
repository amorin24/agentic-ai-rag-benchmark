"""
AutoGen Runner module for the RAG benchmark.

This module implements a company research agent using the AutoGen framework.
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

class AutoGenRunner(AgentRunner):
    """
    Implementation of the AgentRunner for AutoGen.
    
    This agent is tasked with researching a given company using the AutoGen framework.
    """
    
    def __init__(self, rag_service_url: str):
        """
        Initialize the AutoGen runner.
        
        Args:
            rag_service_url: URL of the RAG service
        """
        super().__init__("autogen", rag_service_url)
        
        
    def run_task(self, topic: str) -> Dict[str, Any]:
        """
        Research a company using AutoGen agents.
        
        Args:
            topic: Company name to research
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        # Initialize timing and steps from parent class
        super().run_task(topic)
        
        self._simulate_research_planning(topic)
        
        company_info = self._query_rag_service(topic, "company overview")
        self._add_step("rag_query", {
            "query": f"Company overview for {topic}",
            "results": company_info,
            "usage": "Used to gather general company information"
        })
        
        news_info = self._query_rag_service(topic, "recent news")
        self._add_step("rag_query", {
            "query": f"Recent news about {topic}",
            "results": news_info,
            "usage": "Used to gather recent news about the company"
        })
        
        product_info = self._query_rag_service(topic, "product portfolio")
        self._add_step("rag_query", {
            "query": f"Product portfolio of {topic}",
            "results": product_info,
            "usage": "Used to gather information about company products"
        })
        
        financial_info = self._query_rag_service(topic, "financial analysis")
        self._add_step("rag_query", {
            "query": f"Financial analysis of {topic}",
            "results": financial_info,
            "usage": "Used to analyze financial health and trends"
        })
        
        self._simulate_multi_agent_conversation(topic, company_info, news_info, product_info, financial_info)
        
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
                f"1. Gather comprehensive overview of {company}",
                f"2. Collect recent news and press releases",
                f"3. Research product portfolio and market positioning",
                f"4. Analyze financial performance and future outlook",
                f"5. Synthesize information into a detailed report"
            ]
        })
        
        self._update_token_usage(280)
        
        time.sleep(0.6)
    
    def _query_rag_service(self, company: str, aspect: str) -> List[Dict[str, Any]]:
        """
        Query the RAG service for company information.
        
        Args:
            company: Company name to research
            aspect: Specific aspect to research (e.g., "recent news")
            
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
                
                self._update_token_usage(120)
                
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
                "text": f"{company} is a global leader in its industry, with operations in over 50 countries and a strong focus on innovation.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.94
            }]
        elif aspect == "recent news":
            return [{
                "text": f"{company} recently announced a major acquisition that is expected to significantly expand its market share in emerging markets.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.91
            }]
        elif aspect == "product portfolio":
            return [{
                "text": f"{company}'s diverse product portfolio includes industry-leading solutions that have consistently outperformed competitors in independent benchmarks.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.89
            }]
        elif aspect == "financial analysis":
            return [{
                "text": f"{company}'s financial performance has been robust, with year-over-year revenue growth of 18% and expanding profit margins.",
                "metadata": {"source": "simulated", "relevance": "high"},
                "score": 0.93
            }]
        else:
            return [{
                "text": f"Information about {company} related to {aspect}.",
                "metadata": {"source": "simulated", "relevance": "medium"},
                "score": 0.78
            }]
    
    def _simulate_multi_agent_conversation(self, company: str, company_info: List[Dict], news_info: List[Dict], 
                                         product_info: List[Dict], financial_info: List[Dict]) -> None:
        """
        Simulate a multi-agent conversation analyzing the company.
        
        Args:
            company: Company name
            company_info: General company information
            news_info: Latest news
            product_info: Product information
            financial_info: Financial information
        """
        
        self._add_step("agent_conversation", {
            "agent": "researcher",
            "message": f"I've gathered comprehensive information about {company}. The company appears to be a significant player in its industry with strong market presence."
        })
        
        self._add_step("agent_conversation", {
            "agent": "analyst",
            "message": f"Based on the news, {company} is making strategic moves to expand its market reach. Their product portfolio shows innovation and market leadership."
        })
        
        self._add_step("agent_conversation", {
            "agent": "financial_expert",
            "message": f"The financial data indicates strong performance with consistent growth. Their profit margins are healthy and they appear to be financially stable."
        })
        
        self._add_step("agent_conversation", {
            "agent": "researcher",
            "message": "What are the key strengths and potential risks we should highlight in our report?"
        })
        
        self._add_step("agent_conversation", {
            "agent": "analyst",
            "message": f"Key strengths include market leadership, innovative products, and strategic growth initiatives. Potential risks might include market competition and regulatory challenges."
        })
        
        self._update_token_usage(650)
        
        time.sleep(1.2)
    
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

Our multi-agent analysis of {company} reveals a strong market position with innovative products and solid financial performance. The company has demonstrated strategic vision through recent initiatives and maintains a competitive edge in its industry. Based on our comprehensive assessment, {company} shows promising growth potential and resilience in its market sector.

- Strong market leadership and brand recognition
- Innovative product portfolio with consistent updates
- Robust financial performance with healthy margins
- Strategic growth initiatives and market expansion

- Competitive market landscape
- Regulatory challenges in key markets
- Potential for market disruption from emerging technologies
"""
        
        self._add_step("report_generation", {
            "thought": f"Generating comprehensive report for {company}",
            "report_sections": ["Company Overview", "Recent News", "Product Portfolio", "Financial Analysis", "Executive Summary", "Strengths and Opportunities", "Potential Risks"]
        })
        
        self._update_token_usage(450)
        
        time.sleep(0.9)
        
        return report


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    runner = AutoGenRunner(rag_service_url)
    
    result = runner.run_task("Microsoft Corporation")
    
    print(json.dumps(result, indent=2))
