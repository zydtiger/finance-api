"""
Yahoo backend implemeneted with yfinance.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
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
