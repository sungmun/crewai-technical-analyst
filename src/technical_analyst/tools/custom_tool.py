from crewai_tools import ScrapeWebsiteTool
from crewai.tools import tool
import yfinance as yf
import pandas as pd
from datetime import datetime as dt
import os
import pickle
import re
date = dt.now().strftime("%m-%d")

if os.path.isdir("output")==False:
    os.mkdir("output")

data_dir=f"output/{date}"
if os.path.isdir(data_dir)==False:
    os.mkdir(data_dir)


def cache(func):
    def wrapper(ticker):
        func_name=func.__name__
        clean_str=re.search(r'[A-Z]+',ticker).group()
        print(f"{func_name}({clean_str}) : ",end="")
        if os.path.isdir(f"{data_dir}/{clean_str}")==False:
            os.mkdir(f"{data_dir}/{clean_str}")
            os.mkdir(f"{data_dir}/{clean_str}/data")
        cache_full_path=f"{data_dir}/{clean_str}/data/{func_name}.pkl"
        if os.path.isfile(cache_full_path)==True:
            output=cache_get(cache_full_path)
            print(f'success \n{output}')
            return output
        output=func(clean_str)
        print(f"\n{output}")
        if isinstance(output,list) or isinstance(output,pd.DataFrame):
            cache_set(cache_full_path,output)
        return output
    wrapper.__name__=func.__name__
    wrapper.__doc__=func.__doc__
    return wrapper

def cache_set(key:str,data):
    with open(key,'wb') as file:
        pickle.dump(data,file)

def cache_get(key:str):
    with open(key,'rb') as file:
        return pickle.load(file)


@tool("Stock News")
@cache
def stock_news(ticker: str):
    """
    Retrieves the latest news for a given stock ticker.
    
    Parameters:
    - ticker (str): The stock ticker symbol (e.g. AAPL for Apple Inc., NET for Cloudflare Inc.). 
      The ticker should be a valid stock symbol listed on a major stock exchange.

    Returns:
    - List of news articles related to the stock, or an error message if the ticker is invalid.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        if not ticker_data.info:
            return f"Invalid ticker: {ticker}"
        return ticker_data.news
    except Exception as e:
        return f"An error occurred: {e}"


@tool("Stock Price")
@cache
def stock_price(ticker: str):
    """
    Retrieves historical stock price data for a given stock ticker.

    Parameters:
    - ticker (str): The stock ticker symbol (e.g. AAPL for Apple Inc., NET for Cloudflare Inc.). 
      The ticker should be a valid stock symbol listed on a major stock exchange.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        if not ticker_data.info:
            return f"Invalid ticker: {ticker}"
        # return ticker_data.history(period="1y")
        return ticker_data.history(period="1y")
    except Exception as e:
        return f"An error occurred: {e}"

@tool("Income Statement")
@cache
def income_stmt(ticker: str):
    """
    Retrieves the income statement for a given stock ticker.

    Parameters:
    - ticker (str): The stock ticker symbol (e.g. AAPL for Apple Inc., NET for Cloudflare Inc.). 
      The ticker should be a valid stock symbol listed on a major stock exchange.

    Returns:
    - Income statement of the company, or an error message if the ticker is invalid.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        if not ticker_data.info:
            return f"Invalid ticker: {ticker}"
        return ticker_data.income_stmt
    except Exception as e:
        return f"An error occurred: {e}"

@tool("Balance Sheet")
@cache
def balance_sheet(ticker: str):
    """
    Retrieves the balance sheet for a given stock ticker.

    Parameters:
    - ticker (str): The stock ticker symbol (e.g. AAPL for Apple Inc., NET for Cloudflare Inc.). 
      The ticker should be a valid stock symbol listed on a major stock exchange.

    Returns:
    - Balance sheet of the company, or an error message if the ticker is invalid.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        if not ticker_data.info:
            return f"Invalid ticker: {ticker}"
        return ticker_data.balance_sheet
    except Exception as e:
        return f"An error occurred: {e}"

@tool("Insider Transactions")
@cache
def insider_transactions(ticker: str):
    """
    Retrieves insider transactions for a given stock ticker.

    Parameters:
    - ticker (str): The stock ticker symbol (e.g. AAPL for Apple Inc., NET for Cloudflare Inc.). 
      The ticker should be a valid stock symbol listed on a major stock exchange.

    Returns:
    - Insider transactions of the company, or an error message if the ticker is invalid.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        if not ticker_data.info:
            return f"Invalid ticker: {ticker}"
        return ticker_data.insider_transactions
    except Exception as e:
        return f"An error occurred: {e}"

scrape_tool = ScrapeWebsiteTool()