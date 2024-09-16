"""
Fastapi router file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.3.1
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import ValidationError

from robot import yahoo
from models.history import Period, ResponseType, StockPriceRecord
from utils import forge_csv_response

router = APIRouter()


@router.get("/history/{ticker}", response_model=list[StockPriceRecord] | str)
async def get_history(
    ticker: str,
    start: str | None = None,
    end: str | None = None,
    period: Period | None = None,
    type: ResponseType = ResponseType.PLAIN,
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
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Historical data triggered internal error: {e}",
        )

    # if model, convert dataframe to list[model]
    if type is ResponseType.MODEL:
        df.reset_index(inplace=True)
        df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            },
            inplace=True,
        )
        try:
            return list(
                map(lambda row: StockPriceRecord(**row[1].to_dict()), df.iterrows())
            )
        except ValidationError as e:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal Server Error: {e}"
            )

    return forge_csv_response(df, is_file=type is ResponseType.CSV, filename=ticker)


# todo: integration with frontend model
@router.get("/income/{ticker}", response_model=str)
async def get_income_statement(ticker: str, file: bool = False):
    df = yahoo.get_income_statement(ticker)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_income_statement")


# todo: integration with frontend model
@router.get("/cashflow/{ticker}", response_model=str)
async def get_cashflow_statement(ticker: str, file: bool = False):
    df = yahoo.get_cashflow_statement(ticker)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_cashflow_statement")
