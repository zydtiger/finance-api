"""
Finviz backend implemeneted with web scraping.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.3.0
"""

import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
from utils import get_url_origin
from datetime import datetime
import pytz

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
            FINVIZ_STOCK_URL,
            params={"t": ticker},
            headers={"User-Agent": CHROME_USER_AGENT},
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
            "name": "EPS Yearly Growth (TTM)",
            "callback": lambda s: float(s[:-1]) / 100,
        },
        "EPS Q/Q": {
            "name": "EPS Quarterly Growth (YoY)",
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


async def get_news(ticker: str) -> pd.DataFrame:
    """
    Gets news list for stock using finviz.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of news list
    """

    page = await parse_stock_page(ticker)
    news_table_elem = page.select_one(".news-table")
    if not news_table_elem:
        raise ElementNotFoundError("News table not found")

    news_table_rows = news_table_elem.select("tr")

    news_list = []
    for row in news_table_rows:
        cells = row.select("td")
        if len(cells) != 2:
            continue

        title_link = cells[1].select_one("a.tab-link-news")
        if not title_link:
            continue  # simply skip loading ones
        title = title_link.text.strip()
        link = str(title_link.get("href"))
        thumb_img_src = f"{get_url_origin(link)}/favicon.ico"

        publisher = cells[1].select_one(".news-link-right")
        if not publisher:
            continue
        publisher_name = publisher.text.strip()
        if "(" not in publisher_name:
            continue  # skip finviz elite paid news
        publisher_name = publisher_name[1:-1]  # remove () wrap

        news_list.append(
            {
                "Date": cells[0].text.strip(),
                "Title": title,
                "Link": link,
                "Publisher": publisher_name,
                "Thumb Img Src": thumb_img_src,
            }
        )

    # pad dates
    for i, news in enumerate(news_list):
        if news["Date"][0].isdigit():
            news["Date"] = f"{news_list[i-1]['Date'].split(' ')[0]} {news['Date']}"
        elif news["Date"].startswith("Today"):
            timezone = pytz.timezone("US/Eastern")
            today_date = datetime.now(timezone).strftime("%b-%d-%y")
            news["Date"] = news["Date"].replace("Today", today_date)

    # parse dates
    for news in news_list:
        news["Date"] = datetime.strptime(news["Date"], "%b-%d-%y %I:%M%p")

    return pd.DataFrame(news_list)
