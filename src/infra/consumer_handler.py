from src.infra.usecase import UseCase
from src.infra.schema_validator import SchemaValidator


class ConsumerHandler:
    def __init__(self, usecase: UseCase, schema: SchemaValidator):
        self.usecase = usecase
        self.schema = schema

    def handle(self, message_body: any):
        return