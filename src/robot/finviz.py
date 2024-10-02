"""
Finviz backend implemeneted with web scraping.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.2.1
"""

import pandas as pd
import aiohttp
from bs4 import BeautifulSoup

FINVIZ_BASE_URL = "https://finviz.com/"
FINVIZ_STOCK_URL = f"{FINVIZ_BASE_URL}/quote.ashx"

CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"


class ElementNotFoundError(Exception):
    pass


async def parse_stock_page(ticker: str) -> BeautifulSoup:
    """
    Gets parsed html page contents for stock from finviz.com.

    Args:
        ticker (str): stock ticker symbol

    Returns:
       BeautifulSoup: parsed html page
    """
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            FINVIZ_STOCK_URL, params={"t": ticker}, headers={"User-Agent": CHROME_USER_AGENT}
        )
        content = await response.text()
        return BeautifulSoup(content, "lxml")


async def get_tags(ticker: str) -> pd.DataFrame:
    """
    Gets tags for stock from finviz.com.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of stock tags
    """

    page = await parse_stock_page(ticker)
    tags_container = page.select_one(".quote-links div")
    if not tags_container:
        raise ElementNotFoundError("Tags container not found")

    tags = tags_container.select("a")
    if len(tags) == 0:
        raise ElementNotFoundError("Tags not found")

    tag_links = [
        {"Name": tag.text, "Link": f"{FINVIZ_BASE_URL}{tag.get("href")}"}
        for tag in tags
    ]
    return pd.DataFrame(tag_links)


async def get_partial_metainfo_finviz(ticker: str) -> pd.DataFrame:
    """
    Gets partial metainfo for stock using finviz.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of partial metainfo
    """

    page = await parse_stock_page(ticker)
    metainfo_table_elem = page.select_one(".js-snapshot-table")
    if not metainfo_table_elem:
        raise ElementNotFoundError("Metainfo table not found")

    metainfo_table_cells = metainfo_table_elem.select("td")

    target_labels = {
        "Index": {
            "name": "Index Participation",
            "callback": lambda s: ",".join([name.strip() for name in s.split(",")]),
        },
        "EPS Y/Y TTM": {
            "name": "EPS Yearly Growth",
            "callback": lambda s: float(s[:-1]) / 100,
        },
        "EPS Q/Q": {
            "name": "EPS Quarterly Growth",
            "callback": lambda s: float(s[:-1]) / 100,
        },
        "EPS Surprise": {
            "name": "EPS Surprise",
            "callback": lambda s: float(s[:-1]) / 100,
        },
    }

    metainfo_dict = {}
    for i in range(0, len(metainfo_table_cells), 2):
        label = metainfo_table_cells[i].text
        if label in target_labels:
            key = target_labels[label]["name"]
            callback = target_labels[label]["callback"]
            metainfo_dict[key] = callback(metainfo_table_cells[i + 1].text)

    return pd.DataFrame.from_dict(metainfo_dict, orient="index", columns=["Value"])
