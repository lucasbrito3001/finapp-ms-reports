import os
from src.infra.usecase import UseCase
from src.infra.rabbitmq_publisher import RabbitMQPublisher
from src.adapters import MonthlyExpensesReportRequestMessage
from src.adapters.repositories.expenses_repository import ExpensesRepository
from src.utils.report_file_creator import ReportFileCreator
from src.adapters.storage.gcp_storage import GcpStorage


class ProcessMontlhyExpensesReportRequest(UseCase):
    def __init__(
        self,
        expenses_repository: ExpensesRepository,
        report_file_creator: ReportFileCreator,
        rabbitmq_publisher: RabbitMQPublisher,
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
        target_month: str = f'{message["target_month"]}'
        target_year: str = f'{message["target_year"]}'

        print(
            f"[ProcessMontlhyExpensesReportRequest] Start processing report request - request_id: {request_id}"
        )

        print(f"[ProcessMontlhyExpensesReportRequest] Searching expenses in datasource")
        expenses = self.expenses_repository.getExpensesByMonth(
            target_month, target_year
        )

        filename = f"{request_id}"

        print(f"[ProcessMontlhyExpensesReportRequest] Creating report file")
        columns = [
            {"key": "Id", "format": "number", "width": 10},
            {"key": "Descrição", "format": "text", "width": 50},
            {"key": "Categoria", "format": "text", "width": 10},
            {"key": "Valor", "format": "currency", "width": 15},
            {"key": "Mês", "format": "text", "width": 10},
            {"key": "Ano", "format": "number", "width": 10},
            {"key": "Data de criação", "format": "datetime", "width": 20},
        ]

        created_file_path = self.report_file_creator.createXlsx(
            expenses,
            columns,
            filename,
            f"{target_month:0>2}-{target_year[2:]}",
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
            f"[ProcessMontlhyExpensesReportRequest] End processing report request successfully - request_id: {request_id}"
        )

        return
