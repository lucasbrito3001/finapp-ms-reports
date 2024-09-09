class ReportRequestMessage:
    request_id: int
    file_extension: str


class MonthlyExpensesReportFilters:
    target_month: str
    user_id: int
    user_fullname: str


class MonthlyExpensesReportRequestMessage(ReportRequestMessage):
    filters: MonthlyExpensesReportFilters
