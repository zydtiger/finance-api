"""
Yahoo backend implemeneted with yfinance.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.3.0
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

from models.history import Period


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


def get_income_statement(ticker: str) -> pd.DataFrame:
    """
    Gets income statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of income statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    income_df = yf.Ticker(ticker).income_stmt
    return income_df.iloc[::-1, ::-1]  # reverse rows and columns


def get_cashflow_statement(ticker: str) -> pd.DataFrame:
    """
    Gets cash flow statement for ticker.

    Args:
        ticker (str): stock ticker symbol

    Returns:
        pd.DataFrame: pandas DataFrame of cashflow statement in the same order as on Yahoo
    """

    # adapter of yahoo finance
    cashflow_df = yf.Ticker(ticker).cashflow
    return cashflow_df.iloc[::-1, ::-1]
