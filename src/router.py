"""
Fastapi router file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import PlainTextResponse
from datetime import datetime
from io import StringIO

from robot import yahoo
from models.history import Period

router = APIRouter()


@router.get("/history/{ticker}")
async def get_history(
    ticker: str,
    start: str | None = None,
    end: str | None = None,
    period: Period | None = None,
):
    if start is not None and end is not None and period is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Bad request params to API, please refer to /docs for details",
        )

    if period is None and (start is None or end is None):
        period = Period.MAX

    def parse_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y-%m-%d")

    try:
        start_date = parse_date(start) if start is not None else None
        end_date = parse_date(end) if end is not None else None
    except ValueError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"Bad request date format: {e}"
        )

    try:
        df = yahoo.get_history(ticker, start=start_date, end=end_date, period=period)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        return PlainTextResponse(csv_buffer.getvalue())
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Historical data triggered internal error: {e}",
        )
