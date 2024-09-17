"""
General models and types used for APIs.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

from enum import Enum


class ResponseType(Enum):
    """
    Valid return types for pd.DataFrame responses.
    """

    PLAIN = "plain"
    CSV = "csv"
    MODEL = "model"
