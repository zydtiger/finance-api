"""
Utilities file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.2
"""

import pandas as pd
from io import StringIO
from fastapi import status, HTTPException
from fastapi.responses import PlainTextResponse
from urllib.parse import urlparse


def forge_csv_response(
    df: pd.DataFrame, is_file: bool, filename: str
) -> PlainTextResponse:
    """
    Forges csv response as either direct text or downloaded file.

    Args:
        df (pd.DataFrame): source data
        is_file (bool): whether to download as file
        filename (str): filename of downloaded file

    Returns:
        PlainTextResponse: http response of either text or file
    """

    # plain text response
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    response = PlainTextResponse(csv_buffer.getvalue())

    # if file, download text as attachment
    if is_file:
        response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"

    return response


def convert_keys(keys: list[str]) -> list[str]:
    """
    Convert keys to lowercase and replace whitespaces with underlines.
    """

    converted_keys = []
    for key in keys:
        converted_keys.append(
            key.lower().replace(" ", "_").replace("(", "").replace(")", "")
        )

    return converted_keys


def internal_error(e: Exception) -> HTTPException:
    return HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        f"Internal server error: {e}",
    )


def bad_request(msg: str) -> HTTPException:
    return HTTPException(status.HTTP_400_BAD_REQUEST, f"Bad request: {msg}")


def get_url_origin(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"
