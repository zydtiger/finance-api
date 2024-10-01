"""
Financials APIs related models.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.2.0
"""

from enum import Enum
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class StatementType(Enum):
    """
    Statement type for income, cash flow, and balance sheet.
    """

    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class SECFilingRecord(BaseModel):
    """
    SEC filing model.
    """

    date: datetime
    type: str
    title: str
    link: HttpUrl


class TagInfo(BaseModel):
    """
    Tag model for stocks.
    """

    name: str
    link: HttpUrl


class StockMetaInfo(BaseModel):
    """
    Stock meta info model.
    """

    # yahoo
    ticker: str  # symbol
    name: str  # longName
    exchange: str  # exchange
    summary: str  # longBusinessSummary
    employees: int  # fullTimeEmployees
    dividend_rate: float  # dividendRate
    price_to_book: float  # priceToBook
    pirce_to_earning_ttm: float  # trailingPE
    eps_ttm: float  # trailingEps
    market_cap: int  # marketCap
    fiftytwo_week_low: float  # fiftyTwoWeekLow
    fiftytwo_week_high: float  # fiftyTwoWeekHigh
    shares_outstanding: int  # sharesOutstanding
    revenue: int  # totalRevenue
    ebitda: int  # ebitda
    gross_margins: float  # grossMargins
    operating_margins: float  # operatingMargins
    net_profit_margins: float  # profitMargins

    # finviz
    index_partipation: list[str]  # Index
    eps_yearly_growth: float  # EPS Y/Y TTM
    eps_quarterly_growth: float  # EPS Q/Q
    eps_surprise: float  # EPS Surprise

    # get_calendar
    earnings_date: datetime


# todo: current_price?
