from datetime import datetime
from schema import Schema, And, Use

current_year = datetime.now().year

monthly_expenses_report_request_schema = Schema(
    {
        "request_id": And(
            Use(int),
            lambda req_id: req_id >= 1,
            error="request_id must be a positive integer greater than 0",
        ),
        "file_extension": Schema(
            lambda format: format in {"xlsx", "csv", "pdf"},
            error="file_extension must be some of the following values: xlsx, csv or pdf",
        ),
        "target_year": And(
            Use(int),
            lambda year: 2022 <= year <= datetime.now().year,
            error=f"target_year must be an integer betweem 2022 and {current_year}",
        ),
        "target_month": And(
            Use(int),
            lambda month: 0 <= month <= 11,
            error="target_month must be an integer between 0 and 11",
        ),
    }
)
