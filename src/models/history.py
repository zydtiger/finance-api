"""
History API related models.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.1
"""

from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Period(Enum):
    """
    Valid periods for historical data.
    """

    DAY = "1d"
    WEEK = "5d"
    MONTH = "1mo"
    QUARTER = "3mo"
    HALF_YR = "6mo"
    YEAR = "1y"
    TWO_YR = "2y"
    FIVE_YR = "5y"
    DECADE = "10y"
    YTD = "ytd"
    MAX = "max"


class Type(Enum):
    """
    Valid return types for historical data.
    """

    PLAIN = "plain"
    CSV = "csv"
    MODEL = "model"


class StockPriceRecord(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
