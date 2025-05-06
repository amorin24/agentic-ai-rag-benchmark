"""
Financial Modeling Prep API integration module for the Agentic AI RAG Benchmark project.

This module provides functions to fetch financial data from the Financial Modeling Prep API.
It handles API requests, error handling, and data normalization.
"""

import logging
import time
import requests
from typing import Dict, Any, Optional, List, Union

from utils.config import FMP_API_KEY, LOGS_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

failed_requests_handler = logging.FileHandler(LOGS_DIR / 'fmp_api_errors.log')
failed_requests_handler.setLevel(logging.ERROR)
failed_requests_logger = logging.getLogger('fmp_api_errors')
failed_requests_logger.addHandler(failed_requests_handler)
failed_requests_logger.propagate = False  # Don't propagate to root logger

FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"


def fetch_financials(ticker: str) -> Dict[str, Any]:
    """
    Fetch financial data for a company from Financial Modeling Prep API.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        Dictionary containing normalized financial data
    """
    if not FMP_API_KEY:
        logger.error("Financial Modeling Prep API key not found in environment variables")
        failed_requests_logger.error(f"API key missing for ticker: {ticker}")
        return {}
    
    ticker = ticker.upper().strip()
    
    try:
        logger.info(f"Fetching financial data for '{ticker}'")
        
        financial_data = {
            "ticker": ticker,
            "company_profile": _fetch_company_profile(ticker),
            "income_statement": _fetch_income_statement(ticker),
            "balance_sheet": _fetch_balance_sheet(ticker),
            "cash_flow": _fetch_cash_flow(ticker),
            "key_metrics": _fetch_key_metrics(ticker),
            "financial_ratios": _fetch_financial_ratios(ticker),
            "stock_price": _fetch_stock_price(ticker),
            "news": _fetch_company_news(ticker, limit=5)
        }
        
        if not financial_data["company_profile"] and not financial_data["stock_price"]:
            logger.warning(f"No financial data found for ticker: {ticker}")
            return {}
            
        logger.info(f"Successfully fetched financial data for {ticker}")
        return financial_data
        
    except Exception as e:
        error_message = f"Unexpected error fetching financial data for ticker '{ticker}': {str(e)}"
        logger.error(error_message)
        failed_requests_logger.error(error_message)
        return {}


def _make_api_request(endpoint: str, params: Dict[str, Any] = None) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
    """
    Make a request to the Financial Modeling Prep API.
    
    Args:
        endpoint: API endpoint to call
        params: Additional query parameters
        
    Returns:
        API response data or None if the request failed
    """
    if params is None:
        params = {}
        
    params["apikey"] = FMP_API_KEY
    
    try:
        url = f"{FMP_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except requests.exceptions.Timeout:
        logger.error(f"Request to FMP API timed out for endpoint: {endpoint}")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to FMP API failed for endpoint '{endpoint}': {str(e)}")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error in FMP API request for endpoint '{endpoint}': {str(e)}")
        return None


def _fetch_company_profile(ticker: str) -> Dict[str, Any]:
    """Fetch company profile information."""
    try:
        endpoint = f"profile/{ticker}"
        data = _make_api_request(endpoint)
        
        if not data or not isinstance(data, list) or len(data) == 0:
            return {}
            
        return data[0]
    except Exception as e:
        logger.error(f"Error fetching company profile for {ticker}: {str(e)}")
        return {}


def _fetch_income_statement(ticker: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch income statement data."""
    try:
        endpoint = f"income-statement/{ticker}"
        data = _make_api_request(endpoint, {"limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching income statement for {ticker}: {str(e)}")
        return []


def _fetch_balance_sheet(ticker: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch balance sheet data."""
    try:
        endpoint = f"balance-sheet-statement/{ticker}"
        data = _make_api_request(endpoint, {"limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching balance sheet for {ticker}: {str(e)}")
        return []


def _fetch_cash_flow(ticker: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch cash flow statement data."""
    try:
        endpoint = f"cash-flow-statement/{ticker}"
        data = _make_api_request(endpoint, {"limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching cash flow for {ticker}: {str(e)}")
        return []


def _fetch_key_metrics(ticker: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch key financial metrics."""
    try:
        endpoint = f"key-metrics/{ticker}"
        data = _make_api_request(endpoint, {"limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching key metrics for {ticker}: {str(e)}")
        return []


def _fetch_financial_ratios(ticker: str, limit: int = 4) -> List[Dict[str, Any]]:
    """Fetch financial ratios."""
    try:
        endpoint = f"ratios/{ticker}"
        data = _make_api_request(endpoint, {"limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching financial ratios for {ticker}: {str(e)}")
        return []


def _fetch_stock_price(ticker: str) -> Dict[str, Any]:
    """Fetch current stock price and related data."""
    try:
        endpoint = f"quote/{ticker}"
        data = _make_api_request(endpoint)
        
        if not data or not isinstance(data, list) or len(data) == 0:
            return {}
            
        return data[0]
    except Exception as e:
        logger.error(f"Error fetching stock price for {ticker}: {str(e)}")
        return {}


def _fetch_company_news(ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch recent news about the company."""
    try:
        endpoint = f"stock_news"
        data = _make_api_request(endpoint, {"tickers": ticker, "limit": limit})
        
        if not data or not isinstance(data, list):
            return []
            
        return data
    except Exception as e:
        logger.error(f"Error fetching company news for {ticker}: {str(e)}")
        return []


if __name__ == "__main__":
    """Test the Financial Modeling Prep API functionality."""
    import json
    
    financials = fetch_financials("AAPL")
    
    if financials:
        print(f"Successfully fetched financial data for AAPL")
        print("\nCompany Profile:")
        if financials.get("company_profile"):
            profile = financials["company_profile"]
            print(f"Name: {profile.get('companyName')}")
            print(f"Industry: {profile.get('industry')}")
            print(f"Description: {profile.get('description', '')[:100]}...")
        
        print("\nStock Price:")
        if financials.get("stock_price"):
            price = financials["stock_price"]
            print(f"Price: ${price.get('price')}")
            print(f"Change: {price.get('change')} ({price.get('changesPercentage')}%)")
            print(f"Market Cap: ${price.get('marketCap')}")
    else:
        print("Failed to fetch financial data for AAPL")
    
    import os
    original_key = os.environ.get('FMP_API_KEY', '')
    os.environ['FMP_API_KEY'] = 'invalid_key'
    
    print("\nTesting with invalid API key:")
    invalid_financials = fetch_financials("MSFT")
    print(f"Result: {bool(invalid_financials)}")
    
    os.environ['FMP_API_KEY'] = original_key
