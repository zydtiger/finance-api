"""
Statements APIs related models.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

from enum import Enum


class StatementType(Enum):
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
