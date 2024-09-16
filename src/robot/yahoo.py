"""
Yahoo backend implemeneted with yfinance.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.4.1
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

from models.history import Period
from models.statements import StatementType


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
