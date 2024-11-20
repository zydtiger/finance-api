"""
Financials APIs related models.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.3.0
"""

from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
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

    ## FROM yahoo
    # symbol
    ticker: str
    # longName
    full_name: str = Field(serialization_alias="fullName")
    # exchange
    exchange: str
    # longBusinessSummary
    summary: str | None
    # fullTimeEmployees
    employees: int | None
    # dividendRate
    dividend_rate: float | None = Field(serialization_alias="dividendRate")
    # priceToBook
    price_to_book: float | None = Field(serialization_alias="priceToBook")
    # trailingPE
    price_to_earning_ttm: float | None = Field(serialization_alias="priceToEarningTTM")
    # trailingEps
    eps_ttm: float | None = Field(serialization_alias="epsTTM")
    # marketCap
    market_cap: int | None = Field(serialization_alias="marketCap")
    # fiftyTwoWeekLow
    fiftytwo_week_low: float = Field(serialization_alias="fiftytwoWeekLow")
    # fiftyTwoWeekHigh
    fiftytwo_week_high: float = Field(serialization_alias="fiftytwoWeekHigh")
    # sharesOutstanding
    shares_outstanding: int | None = Field(serialization_alias="sharesOutstanding")
    # totalRevenue
    revenue: int | None
    # ebitda
    ebitda: int | None
    # grossMargins
    gross_margins: float | None = Field(serialization_alias="grossMargins")
    # operatingMargins
    operating_margins: float | None = Field(serialization_alias="operatingMargins")
    # profitMargins
    net_profit_margins: float | None = Field(serialization_alias="netProfitMargins")

    ## FROM get_calendar (yahoo)
    earnings_date: datetime | None = Field(serialization_alias="earningsDate")

    ## FROM finviz
    # Index
    index_participation: list[str] | None = Field(
        serialization_alias="indexParticipation"
    )
    # EPS Y/Y TTM
    eps_yearly_growth_ttm: float | None = Field(
        serialization_alias="epsYearlyGrowthTTM"
    )
    # EPS Q/Q
    eps_quarterly_growth_yoy: float | None = Field(
        serialization_alias="epsQuarterlyGrowthYoY"
    )
    # EPS Surprise
    eps_surprise: float | None = Field(serialization_alias="epsSurprise")


class NewsRecord(BaseModel):
    """
    News record type, matches frontend.
    """

    date: datetime
    title: str
    link: str
    publisher: str
    thumb_img_src: str = Field(serialization_alias="thumbImgSrc")
