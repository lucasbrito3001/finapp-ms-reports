from src.infra.consumer_handler import ConsumerHandler
from src.infra.schema_validator import SchemaValidator
from src.adapters import MonthlyExpensesReportRequestMessage


class ProcessMonthlyExpensesRequestHandler(ConsumerHandler):
    def __init__(self, usecase, schema: SchemaValidator):
        super().usecase = usecase
        super().schema = schema

    def handle(self, message_body: MonthlyExpensesReportRequestMessage):
        validation_result = self.schema.validate(message_body)

        if validation_result.status == False:
            print(
                "[ProcessMonthlyExpensesRequestHandler] Invalid schema, raising exception"
            )
            raise Exception("Invalid schema")

        try:
            self.usecase.execute(validation_result.validated_payload)
        except Exception as exception:
            print(
                f"[ProcessMonthlyExpensesRequestHandler] Error running usecase, raising exception: {exception}"
            )
            raise Exception("Error running usecase")

        return
