"""
Yahoo backend implemeneted with yfinance.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.7.0
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

from models.history import Period
from models.financials import StatementType


def get_history(
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
    return yf.Ticker(ticker).history(
        period=period.value if period is not None else None,
        start=start,
        end=end,
        raise_errors=True,
    )


def get_income_statement(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets income statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of income statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    income_df = (
        yf.Ticker(ticker).income_stmt
        if type is StatementType.YEARLY
        else yf.Ticker(ticker).quarterly_income_stmt
    )
    return income_df.iloc[::-1, ::-1]  # reverse rows and columns


def get_cashflow_statement(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets cash flow statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of cash flow statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    cashflow_df = (
        yf.Ticker(ticker).cashflow
        if type is StatementType.YEARLY
        else yf.Ticker(ticker).quarterly_cashflow
    )
    return cashflow_df.iloc[::-1, ::-1]


def get_balance_sheet(ticker: str, type: StatementType) -> pd.DataFrame:
    """
    Gets balance sheet for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of balance sheet in the same order as on Yahoo
    """

    # adapter of yahoo finance
    balance_df = (
        yf.Ticker(ticker).balance_sheet
        if type is StatementType.YEARLY
        else yf.Ticker(ticker).quarterly_balance_sheet
    )
    return balance_df.iloc[::-1, ::-1]


def get_sec_filings(ticker: str) -> pd.DataFrame:
    """
    Gets SEC filings for stock.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of SEC filings
    """

    sec_filings = yf.Ticker(ticker).sec_filings
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


def get_earnings_date(ticker: str) -> datetime:
    """
    Gets earnings date for stock using yahoo.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        datetime: datetime object of earnings date
    """

    return yf.Ticker(ticker).calendar["Earnings Date"][0]


def get_partial_metainfo_yahoo(ticker: str) -> pd.DataFrame:
    """
    Gets partial metainfo for stock using yahoo.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of partial metainfo
    """

    metainfo_yf = yf.Ticker(ticker).info
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
