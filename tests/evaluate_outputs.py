"""
Evaluation script for comparing agent framework outputs.

This script runs all agent runners with the same input (company name),
collects their outputs, and evaluates them on multiple metrics.
"""

import os
import sys
import json
import time
import csv
import logging
import argparse
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import importlib.util
import numpy as np
from dotenv import load_dotenv
import openai

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crewai.runner import CrewAIRunner
from agents.autogen.runner import AutoGenRunner
from agents.langgraph.runner import LangGraphRunner
from agents.googleadk.runner import GoogleADKRunner
from agents.squidai.runner import SquidAIRunner
from agents.lettaai.runner import LettaAIRunner

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class AgentEvaluator:
    """
    Evaluates and compares outputs from different agent frameworks.
    """
    
    def __init__(self, rag_service_url: str, output_format: str = "json"):
        """
        Initialize the evaluator.
        
        Args:
            rag_service_url: URL of the RAG service
            output_format: Format for output results (json or csv)
        """
        self.rag_service_url = rag_service_url
        self.output_format = output_format
        self.agent_runners = self._initialize_agent_runners()
        
    def _initialize_agent_runners(self) -> Dict[str, Any]:
        """
        Initialize all agent runners.
        
        Returns:
            Dictionary of agent runners
        """
        return {
            "crewai": CrewAIRunner(self.rag_service_url),
            "autogen": AutoGenRunner(self.rag_service_url),
            "langgraph": LangGraphRunner(self.rag_service_url),
            "googleadk": GoogleADKRunner(self.rag_service_url),
            "squidai": SquidAIRunner(self.rag_service_url),
            "lettaai": LettaAIRunner(self.rag_service_url)
        }
    
    def run_evaluation(self, company_name: str, output_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Run evaluation for all agent frameworks.
        
        Args:
            company_name: Company name to research
            output_path: Path to save evaluation results
            
        Returns:
            Dictionary of evaluation results
        """
        rag_context = self._get_rag_context(company_name)
        
        results = {}
        
        for agent_name, runner in self.agent_runners.items():
            logger.info(f"Running {agent_name} agent for {company_name}...")
            
            start_time = time.time()
            output = runner.run_task(company_name)
            end_time = time.time()
            
            response_time = end_time - start_time
            token_usage = output.get("token_usage", 0)
            final_output = output.get("final_output", "")
            steps = output.get("steps", [])
            
            factual_overlap = self._evaluate_factual_overlap(final_output, rag_context)
            reasoning_clarity = self._evaluate_reasoning_clarity(final_output, steps)
            
            results[agent_name] = {
                "response_time": response_time,
                "token_usage": token_usage,
                "factual_overlap": factual_overlap,
                "reasoning_clarity": reasoning_clarity,
                "final_output": final_output,
                "steps": steps
            }
            
            logger.info(f"Completed evaluation for {agent_name}")
        
        self._save_results(results, output_path)
        
        return results
    
    def _get_rag_context(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Get RAG context for the company.
        
        Args:
            company_name: Company name to research
            
        Returns:
            List of RAG context documents
        """
        try:
            response = requests.get(
                f"{self.rag_service_url}/query",
                params={"q": company_name, "top_k": 10}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                logger.warning(f"RAG service returned status code {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error querying RAG service: {str(e)}")
            return []
    
    def _evaluate_factual_overlap(self, output: str, rag_context: List[Dict[str, Any]]) -> float:
        """
        Evaluate factual overlap with RAG context.
        
        Args:
            output: Agent output text
            rag_context: RAG context documents
            
        Returns:
            Factual overlap score (0-1)
        """
        if not rag_context:
            return 0.0
        
        try:
            context_text = " ".join([doc.get("chunk", "") for doc in rag_context])
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an evaluation assistant. Your task is to evaluate the factual overlap between an agent's output and the RAG context provided. Score from 0 to 1, where 0 means no overlap and 1 means perfect overlap."},
                    {"role": "user", "content": f"RAG Context:\n{context_text}\n\nAgent Output:\n{output}\n\nEvaluate the factual overlap between the agent output and the RAG context. Return only a number between 0 and 1."}
                ],
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content.strip()
            try:
                score = float(score_text)
                return min(max(score, 0.0), 1.0)  # Ensure score is between 0 and 1
            except ValueError:
                logger.warning(f"Could not parse factual overlap score: {score_text}")
                return 0.5  # Default to middle score if parsing fails
                
        except Exception as e:
            logger.error(f"Error evaluating factual overlap: {str(e)}")
            return 0.5  # Default to middle score if evaluation fails
    
    def _evaluate_reasoning_clarity(self, output: str, steps: List[Dict[str, Any]]) -> float:
        """
        Evaluate reasoning clarity.
        
        Args:
            output: Agent output text
            steps: Agent execution steps
            
        Returns:
            Reasoning clarity score (0-1)
        """
        try:
            steps_text = json.dumps(steps, indent=2)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an evaluation assistant. Your task is to evaluate the clarity of reasoning in an agent's output and execution steps. Score from 0 to 1, where 0 means unclear reasoning and 1 means perfectly clear reasoning."},
                    {"role": "user", "content": f"Agent Output:\n{output}\n\nExecution Steps:\n{steps_text}\n\nEvaluate the clarity of reasoning. Return only a number between 0 and 1."}
                ],
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content.strip()
            try:
                score = float(score_text)
                return min(max(score, 0.0), 1.0)  # Ensure score is between 0 and 1
            except ValueError:
                logger.warning(f"Could not parse reasoning clarity score: {score_text}")
                return 0.5  # Default to middle score if parsing fails
                
        except Exception as e:
            logger.error(f"Error evaluating reasoning clarity: {str(e)}")
            return 0.5  # Default to middle score if evaluation fails
    
    def _save_results(self, results: Dict[str, Dict[str, Any]], output_path: str) -> None:
        """
        Save evaluation results to file.
        
        Args:
            results: Evaluation results
            output_path: Path to save results
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if self.output_format.lower() == "json":
            self._save_json_results(results, output_path)
        elif self.output_format.lower() == "csv":
            self._save_csv_results(results, output_path)
        else:
            logger.warning(f"Unsupported output format: {self.output_format}. Defaulting to JSON.")
            self._save_json_results(results, output_path)
    
    def _save_json_results(self, results: Dict[str, Dict[str, Any]], output_path: str) -> None:
        """
        Save results in JSON format.
        
        Args:
            results: Evaluation results
            output_path: Path to save results
        """
        if not output_path.endswith(".json"):
            output_path += ".json"
        
        serializable_results = {}
        for agent_name, agent_results in results.items():
            serializable_results[agent_name] = {
                "response_time": agent_results["response_time"],
                "token_usage": agent_results["token_usage"],
                "factual_overlap": agent_results["factual_overlap"],
                "reasoning_clarity": agent_results["reasoning_clarity"],
                "final_output": agent_results["final_output"],
                "steps": [
                    {k: v for k, v in step.items() if isinstance(v, (str, int, float, bool, list, dict))}
                    for step in agent_results["steps"]
                ]
            }
        
        serializable_results["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "format_version": "1.0"
        }
        
        with open(output_path, "w") as f:
            json.dump(serializable_results, f, indent=2)
        
        logger.info(f"Results saved to {output_path}")
    
    def _save_csv_results(self, results: Dict[str, Dict[str, Any]], output_path: str) -> None:
        """
        Save results in CSV format.
        
        Args:
            results: Evaluation results
            output_path: Path to save results
        """
        if not output_path.endswith(".csv"):
            output_path += ".csv"
        
        csv_data = []
        for agent_name, agent_results in results.items():
            csv_data.append({
                "agent_name": agent_name,
                "response_time": agent_results["response_time"],
                "token_usage": agent_results["token_usage"],
                "factual_overlap": agent_results["factual_overlap"],
                "reasoning_clarity": agent_results["reasoning_clarity"]
            })
        
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["agent_name", "response_time", "token_usage", "factual_overlap", "reasoning_clarity"])
            writer.writeheader()
            writer.writerows(csv_data)
        
        logger.info(f"Results saved to {output_path}")
        
        json_output_path = output_path.replace(".csv", "_detailed.json")
        self._save_json_results(results, json_output_path)
        logger.info(f"Detailed results saved to {json_output_path}")


def main():
    """
    Main function to run the evaluation.
    """
    parser = argparse.ArgumentParser(description="Evaluate agent framework outputs")
    parser.add_argument("--company", type=str, default="Microsoft Corporation", help="Company name to research")
    parser.add_argument("--output", type=str, default="../data/evaluation_results", help="Path to save evaluation results")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default="json", help="Output format (json or csv)")
    args = parser.parse_args()
    
    rag_service_url = f"http://{os.getenv('RAG_SERVICE_HOST', 'localhost')}:{os.getenv('RAG_SERVICE_PORT', '8000')}"
    
    evaluator = AgentEvaluator(rag_service_url, args.format)
    
    results = evaluator.run_evaluation(args.company, args.output)
    
    print("\nEvaluation Summary:")
    print("------------------")
    for agent_name, agent_results in results.items():
        print(f"\n{agent_name.upper()}:")
        print(f"  Response Time: {agent_results['response_time']:.2f} seconds")
        print(f"  Token Usage: {agent_results['token_usage']}")
        print(f"  Factual Overlap: {agent_results['factual_overlap']:.2f}")
        print(f"  Reasoning Clarity: {agent_results['reasoning_clarity']:.2f}")
    
    print(f"\nDetailed results saved to {args.output}")


if __name__ == "__main__":
    main()
