import os
import pika
import pika.credentials
import pika.exceptions
from dotenv import load_dotenv
from src.infra.consumer import Consumer
from src.infra.rabbitmq_publisher import RabbitMQPublisher
from src.infra.schema_validator import SchemaValidator
from src.infra.database import DatabaseConnector, DatabaseCursor, DatabaseConnection
from src.adapters.repositories.expenses_repository import ExpensesRepository
from src.adapters.handlers.process_monthly_expenses_request_handler import (
    ProcessMonthlyExpensesRequestHandler,
)
from src.utils.report_file_creator import ReportFileCreator
from src.adapters.storage.gcp_storage import GcpStorage
from src.usecases.process_montlhy_expenses_report_request import (
    ProcessMontlhyExpensesReportRequest,
)
from src.schemas.monthly_expenses_report_request import (
    monthly_expenses_report_request_schema,
)

load_dotenv(".env")

print("===========================================================================")
print("[Bootstrap] Starting application bootstrap\n")

# external connections
# ----------------------------------------------------
rabbitmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.environ.get("RABBITMQ_HOST"),
        virtual_host=os.environ.get("RABBITMQ_VHOST"),
        port=int(os.environ.get("RABBITMQ_PORT")),
        credentials=pika.credentials.PlainCredentials(
            os.environ.get("RABBITMQ_USER"), os.environ.get("RABBITMQ_PASSWORD")
        ),
        connection_attempts=3,
        retry_delay=3,
    )
)

database_connection = DatabaseConnector().connect(
    os.environ.get("DB_CONNECTION_STRING")
)

channel = rabbitmq_connection.channel()

report_file_creator = ReportFileCreator()
rabbitmq_publisher = RabbitMQPublisher(channel)
gcp_storage = GcpStorage()
expenses_repository = ExpensesRepository(database_connection)

# usecases
# ----------------------------------------------------
process_monthly_expenses_report_request = ProcessMontlhyExpensesReportRequest(
    report_file_creator=report_file_creator,
    rabbitmq_publisher=rabbitmq_publisher,
    expenses_repository=expenses_repository,
    gcp_storage=gcp_storage,
)

# schemas
# ----------------------------------------------------
monthly_expenses_report_request_schema_validator = SchemaValidator(
    monthly_expenses_report_request_schema
)

# handlers
# ----------------------------------------------------
process_monthly_expenses_request_handler = ProcessMonthlyExpensesRequestHandler(
    usecase=process_monthly_expenses_report_request,
    schema=monthly_expenses_report_request_schema_validator,
)

# consumers
# ----------------------------------------------------
monthly_expenses_report_consumer = Consumer(
    os.environ.get("MONTLHY_EXPENSES_REPORT_QUEUE_NAME"),
    process_monthly_expenses_request_handler,
    channel,
)

monthly_expenses_report_consumer.prepare()

try:
    print("\n[Bootstrap] Application bootstrap done!")
    print("[Application] Consuming configured queues...")
    print("===========================================================================\n")
    channel.start_consuming()
except pika.exceptions.ConnectionClosedByBroker:
    print("Connection closed by broker")
    channel.close()
    pass
