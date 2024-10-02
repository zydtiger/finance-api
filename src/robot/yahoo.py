"""
Yahoo backend implemeneted with yfinance.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.7.1
"""

import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime

from models.history import Period
from models.financials import StatementType


async def get_history(
    ticker: str, start: datetime | None, end: datetime | None, period: Period | None
) -> pd.DataFrame:
    """
    Gets historical data for ticker given the datetime constraints using yahoo backend.

    Args:
        ticker (str): stock ticker symbol
        start (datetime | None): start datetime
        end (datetime | None): end datetime
        period (Period | None): period to query

    Returns:
        pd.DataFrame: pandas DataFrame of historical data

    Raises:
        Exceptions if any error occurs.
    """

    # adapter of yahoo finance
    history_func = lambda: yf.Ticker(ticker).history(
        period=period.value if period is not None else None,
        start=start,
        end=end,
        raise_errors=True,
    )

    # wrap inside asyncio.to_thread to make non-blocking
    return await asyncio.to_thread(history_func)


async def get_income_statement(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets income statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of income statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    yearly_income_func = lambda: yf.Ticker(ticker).income_stmt
    quarterly_income_func = lambda: yf.Ticker(ticker).quarterly_income_stmt

    income_df = (
        await asyncio.to_thread(yearly_income_func)
        if type is StatementType.YEARLY
        else await asyncio.to_thread(quarterly_income_func)
    )
    return income_df.iloc[::-1, ::-1]  # reverse rows and columns


async def get_cashflow_statement(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets cash flow statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of cash flow statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    yearly_cashflow_func = lambda: yf.Ticker(ticker).cashflow
    quarterly_cashflow_func = lambda: yf.Ticker(ticker).quarterly_cashflow

    cashflow_df = (
        await asyncio.to_thread(yearly_cashflow_func)
        if type is StatementType.YEARLY
        else await asyncio.to_thread(quarterly_cashflow_func)
    )
    return cashflow_df.iloc[::-1, ::-1]


async def get_balance_sheet(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets balance sheet for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of balance sheet in the same order as on Yahoo
    """

    # adapter of yahoo finance
    yearly_balance_sheet_func = lambda: yf.Ticker(ticker).balance_sheet
    quarterly_balance_sheet_func = lambda: yf.Ticker(ticker).quarterly_balance_sheet

    balance_df = (
        await asyncio.to_thread(yearly_balance_sheet_func)
        if type is StatementType.YEARLY
        else await asyncio.to_thread(quarterly_balance_sheet_func)
    )
    return balance_df.iloc[::-1, ::-1]


async def get_sec_filings(ticker: str) -> pd.DataFrame:
    """
    Gets SEC filings for stock.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of SEC filings
    """

    sec_filings = await asyncio.to_thread(lambda: yf.Ticker(ticker).sec_filings)
    sec_filings_parsable = [
        {
            "Date": filing["date"],
            "Type": filing["type"],
            "Title": filing["title"],
            "Link": filing["edgarUrl"],
        }
        for filing in sec_filings
    ]
    return pd.DataFrame(sec_filings_parsable)


async def get_earnings_date(ticker: str) -> datetime:
    """
    Gets earnings date for stock using yahoo.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        datetime: datetime object of earnings date
    """

    earnings_date = await asyncio.to_thread(
        lambda: yf.Ticker(ticker).calendar["Earnings Date"][0]
    )
    return earnings_date


async def get_partial_metainfo_yahoo(ticker: str) -> pd.DataFrame:
    """
    Gets partial metainfo for stock using yahoo.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of partial metainfo
    """

    metainfo_yf = await asyncio.to_thread(lambda: yf.Ticker(ticker).info)
    metainfo_dict = {
        "Ticker": metainfo_yf["symbol"],
        "Full Name": metainfo_yf["longName"],
        "Exchange": metainfo_yf["exchange"],
        "Summary": metainfo_yf["longBusinessSummary"],
        "Employees": metainfo_yf["fullTimeEmployees"],
        "Dividend Rate": metainfo_yf["dividendRate"],
        "Price to Book": metainfo_yf["priceToBook"],
        "Price to Earning (TTM)": metainfo_yf["trailingPE"],
        "EPS (TTM)": metainfo_yf["trailingEps"],
        "Market Cap": metainfo_yf["marketCap"],
        "Fiftytwo Week Low": metainfo_yf["fiftyTwoWeekLow"],
        "Fiftytwo Week High": metainfo_yf["fiftyTwoWeekHigh"],
        "Shares Outstanding": metainfo_yf["sharesOutstanding"],
        "Revenue": metainfo_yf["totalRevenue"],
        "EBITDA": metainfo_yf["ebitda"],
        "Gross Margins": metainfo_yf["grossMargins"],
        "Operating Margins": metainfo_yf["operatingMargins"],
        "Net Profit Margins": metainfo_yf["profitMargins"],
    }

    return pd.DataFrame.from_dict(metainfo_dict, orient="index", columns=["Value"])
