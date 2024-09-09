import os
from src.infra.usecase import UseCase
from src.adapters.messaging.message_publisher import MessagePublisher
from src.adapters import MonthlyExpensesReportRequestMessage
from src.adapters.repositories.expenses_repository import ExpensesRepository
from src.utils.report_file_creator import ReportFileCreator
from src.adapters.storage.gcp_storage import GcpStorage


class ProcessMontlhyExpensesReportRequest(UseCase):
    def __init__(
        self,
        expenses_repository: ExpensesRepository,
        report_file_creator: ReportFileCreator,
        rabbitmq_publisher: MessagePublisher,
        gcp_storage: GcpStorage,
    ) -> None:
        super().__init__()
        self.expenses_repository = expenses_repository
        self.report_file_creator = report_file_creator
        self.rabbitmq_publisher = rabbitmq_publisher
        self.gcp_storage = gcp_storage

    def execute(self, message: MonthlyExpensesReportRequestMessage) -> None:
        file_extension = message["file_extension"]
        request_id = message["request_id"]

        print(
            f"[ProcessMontlhyExpensesReportRequest] Start process - request_id: {request_id}"
        )

        print(f"[ProcessMontlhyExpensesReportRequest] Searching expenses by filters")
        expenses = self.expenses_repository.getExpensesByFilters(message["filters"])

        filename = f"{request_id}"

        print(f"[ProcessMontlhyExpensesReportRequest] Creating report file")
        created_file_path = self.report_file_creator.createXlsx(
            expenses, None, False, filename
        )

        bucket_path = f"monthly-expenses/{file_extension}/{filename}.{file_extension}"

        print(
            f"[ProcessMontlhyExpensesReportRequest] Uploading report file to the storage"
        )
        self.gcp_storage.uploadFile(
            os.environ.get("REPORTS_BUCKET_NAME"),
            created_file_path,
            bucket_path,
        )

        print(
            f"[ProcessMontlhyExpensesReportRequest] Publishing completion message to RabbitMQ"
        )
        self.rabbitmq_publisher.publish(
            os.environ.get("REPORT_EVENTS_EXCHANGE_NAME"),
            os.environ.get("REPORT_REQUEST_COMPLETED_ROUTING_KEY"),
            {"request_id": request_id, "bucket_path": bucket_path},
        )

        print(
            f"[ProcessMontlhyExpensesReportRequest] End process - request_id: {request_id}"
        )

        return
