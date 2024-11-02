"""
Fastapi router file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.9.0
"""

from fastapi import APIRouter
from datetime import datetime
from pydantic import ValidationError

from robot import yahoo, finviz
from robot.finviz import ElementNotFoundError

from models import ResponseType
from models.history import Period, StockPriceRecord
from models.financials import (
    StatementType,
    SECFilingRecord,
    TagInfo,
    StockMetaInfo,
    NewsRecord,
)

from utils import forge_csv_response, convert_keys, internal_error, bad_request

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
        raise bad_request(
            "Bad request params to API, please refer to /docs for details"
        )

    if period is None and (start is None or end is None):
        period = Period.MAX

    def parse_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y-%m-%d")

    try:
        start_date = parse_date(start) if start is not None else None
        end_date = parse_date(end) if end is not None else None
    except ValueError as e:
        raise bad_request(f"wrong date format {e}")

    try:
        df = await yahoo.get_history(
            ticker, start=start_date, end=end_date, period=period
        )
    except Exception as e:
        raise internal_error(e)

    # if model, convert dataframe to list[model]
    if type is ResponseType.MODEL:
        # use number as index instead of date
        # so date can be parsed in row
        df.reset_index(inplace=True)
        rename_dict = {
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
        df.rename(columns=rename_dict, inplace=True)
        try:
            [StockPriceRecord(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise internal_error(e)

    return forge_csv_response(df, is_file=type is ResponseType.CSV, filename=ticker)


# todo: integration with frontend model
@router.get("/income/{ticker}", response_model=str)
async def get_income_statement(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = await yahoo.get_income_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_income_statement")


# todo: integration with frontend model
@router.get("/cashflow/{ticker}", response_model=str)
async def get_cashflow_statement(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = await yahoo.get_cashflow_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_cashflow_statement")


# todo: integration with frontend model
@router.get("/balance/{ticker}", response_model=str)
async def get_balance_sheet(
    ticker: str, type: StatementType = StatementType.YEARLY, file: bool = False
):
    df = await yahoo.get_cashflow_statement(ticker, type)
    return forge_csv_response(df, is_file=file, filename=f"{ticker}_balance_sheet")


@router.get("/sec/{ticker}", response_model=list[SECFilingRecord] | str)
async def get_sec_filings(ticker: str, type: ResponseType = ResponseType.PLAIN):
    df = await yahoo.get_sec_filings(ticker)

    # if model, convert dataframe to list[model]
    if type is ResponseType.MODEL:
        rename_dict = {
            "Date": "date",
            "Type": "type",
            "Title": "title",
            "Link": "link",
        }
        df.rename(columns=rename_dict, inplace=True)
        try:
            return [SECFilingRecord(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise internal_error(e)

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_sec_filings"
    )


@router.get("/tags/{ticker}", response_model=list[TagInfo] | str)
async def get_tags(ticker: str, type: ResponseType = ResponseType.PLAIN):
    try:
        df = await finviz.get_tags(ticker)
    except ElementNotFoundError as e:
        raise internal_error(e)

    if type is ResponseType.MODEL:
        rename_dict = {
            "Name": "name",
            "Link": "link",
        }
        df.rename(columns=rename_dict, inplace=True)
        try:
            return [TagInfo(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise internal_error(e)

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_tags"
    )


@router.get("/metainfo/{ticker}", response_model=StockMetaInfo | str)
async def get_metainfo(ticker: str, type: ResponseType = ResponseType.PLAIN):
    try:
        import pandas as pd

        df_yahoo = await yahoo.get_partial_metainfo_yahoo(ticker)
        df_finviz = await finviz.get_partial_metainfo_finviz(ticker)
        earnings_date = await yahoo.get_earnings_date(ticker)

        df = pd.concat([df_yahoo, df_finviz])
        df.loc["Earnings Date"] = earnings_date
    except ElementNotFoundError as e:
        raise internal_error(e)

    if type is ResponseType.MODEL:
        rename_dict = {
            original: converted
            for original, converted in zip(df.index, convert_keys(df.index.tolist()))
        }
        df.rename(index=rename_dict, inplace=True)
        df_dict = df.to_dict()["Value"]
        df_dict["index_participation"] = list(df_dict["index_participation"].split(","))
        try:
            return StockMetaInfo(**df_dict)
        except ValidationError as e:
            raise internal_error(e)

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_metainfo"
    )


@router.get("/news/{ticker}", response_model=list[NewsRecord] | str)
async def get_news(ticker: str, type: ResponseType = ResponseType.PLAIN):
    try:
        df = await finviz.get_news(ticker)
    except ElementNotFoundError as e:
        raise internal_error(e)

    if type is ResponseType.MODEL:
        rename_dict = {
            "Date": "date",
            "Title": "title",
            "Link": "link",
            "Publisher": "publisher",
            "Thumb Img Src": "thumb_img_src",
        }
        df.rename(columns=rename_dict, inplace=True)
        try:
            return [NewsRecord(**row.to_dict()) for _index, row in df.iterrows()]
        except ValidationError as e:
            raise internal_error(e)

    return forge_csv_response(
        df, is_file=type is ResponseType.CSV, filename=f"{ticker}_news"
    )
