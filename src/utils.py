"""
Utilities file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

import pandas as pd
from io import StringIO
from fastapi.responses import PlainTextResponse


def forge_csv_response(
    df: pd.DataFrame, is_file: bool, filename: str
) -> PlainTextResponse:
    # plain text response
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    response = PlainTextResponse(csv_buffer.getvalue())

    # if file, download text as attachment
    if is_file:
        response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"

    return response
