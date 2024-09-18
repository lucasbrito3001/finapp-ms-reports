from src.infra.consumer_handler import ConsumerHandler
from src.infra.schema_validator import SchemaValidator
from src.adapters import MonthlyExpensesReportRequestMessage
from src.schemas import InvalidSchemaException


class ProcessMonthlyExpensesRequestHandler(ConsumerHandler):
    def __init__(self, usecase, schema: SchemaValidator):
        super().__init__(usecase, schema)

    def handle(self, message_body: MonthlyExpensesReportRequestMessage):
        print("[ProcessMonthlyExpensesRequestHandler] Validating the message body")
        validation_result = self.schema.validate(message_body)

        if validation_result["status"] == False:
            print(
                "[ProcessMonthlyExpensesRequestHandler] Invalid message body, raising InvalidSchemaException"
            )
            raise InvalidSchemaException(validation_result["error"])

        try:
            self.usecase.execute(validation_result["validated_payload"])
        except Exception as exception:
            print(
                f"[ProcessMonthlyExpensesRequestHandler] Error running usecase, raising exception: {exception}"
            )
            raise Exception("Error running usecase")

        print(
            "[ProcessMonthlyExpensesRequestHandler] Message processed successfully"
        )
        return
