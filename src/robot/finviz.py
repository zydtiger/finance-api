"""
Finviz backend implemeneted with web scraping.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

FINVIZ_BASE_URL = "https://finviz.com/"
FINVIZ_STOCK_URL = f"{FINVIZ_BASE_URL}/quote.ashx"

CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

class ElementNotFoundError(Exception):
    pass

def get_tags(ticker: str) -> pd.DataFrame:
    """
    Gets tags for stock from finviz.com.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of stock tags
    """
    
    response = requests.get(
        FINVIZ_STOCK_URL,
        {"t": ticker},
        headers={"User-Agent": CHROME_USER_AGENT},
    )

    page = BeautifulSoup(response.content, "lxml")
    tags_container = page.select_one(".quote-links div")
    if not tags_container:
      raise ElementNotFoundError("Tags container not found")

    tags = tags_container.select("a")
    if len(tags) == 0:
      raise ElementNotFoundError("Tags not found")
    
    tag_links = [{'Name': tag.text, 'Link': f"{FINVIZ_BASE_URL}{tag.get("href")}"} for tag in tags]
    return pd.DataFrame(tag_links)
