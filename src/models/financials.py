"""
Financials APIs related models.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.2
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
