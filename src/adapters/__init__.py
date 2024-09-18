class ReportRequestMessage:
    request_id: int
    file_extension: str


class MonthlyExpensesReportRequestMessage(ReportRequestMessage):
    target_month: str
    target_year: str
