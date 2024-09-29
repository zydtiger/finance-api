"""
Fastapi router file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.7.0
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import ValidationError

from robot import yahoo, finviz
from robot.finviz import ElementNotFoundError

from models import ResponseType
from models.history import Period, StockPriceRecord
from models.financials import StatementType, SECFilingRecord, TagInfo

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
        # use number as index instead of date
        # so date can be parsed in row
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
async def get_income_statement(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = yahoo.get_income_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_income_statement")


# todo: integration with frontend model
@router.get("/cashflow/{ticker}", response_model=str)
async def get_cashflow_statement(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = yahoo.get_cashflow_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_cashflow_statement")


# todo: integration with frontend model
@router.get("/balance/{ticker}", response_model=str)
async def get_balance_sheet(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = yahoo.get_cashflow_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_balance_sheet")


# todo: integration with frontend model
@router.get("/calendar/{ticker}", response_model=dict)
async def get_calendar(ticker: str):
    return yahoo.get_calendar(ticker)


@router.get("/sec/{ticker}", response_model=list[SECFilingRecord] | str)
async def get_sec_filings(ticker: str, type: ResponseType = ResponseType.PLAIN):
    df = yahoo.get_sec_filings(ticker)

    # if model, convert dataframe to list[model]
    if type is ResponseType.MODEL:
        df.rename(
            columns={
                "Date": "date",
                "Type": "type",
                "Title": "title",
                "Link": "link",
            },
            inplace=True,
        )
        try:
            return [SECFilingRecord(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal Server Error: {e}"
            )

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_sec_filings"
    )


@router.get("/tags/{ticker}", response_model=list[TagInfo] | str)
async def get_tags(ticker: str, type: ResponseType = ResponseType.PLAIN):
    try:
        df = finviz.get_tags(ticker)
    except ElementNotFoundError as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Inernal Server Error: {e}"
        )

    if type is ResponseType.MODEL:
        try:
            df.rename(
                columns={
                    "Name": "name",
                    "Link": "link",
                },
                inplace=True,
            )
            return [TagInfo(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal Server Error: {e}"
            )

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_tags"
    )
