from schema import Schema, And, Use, Optional

monthly_expenses_report_request = Schema(
    {
        "request_id": Use(int),
        "report_format": Use(lambda format: format in {"xlsx", "csv", "pdf"}),
    }
)
