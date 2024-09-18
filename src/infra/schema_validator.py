from schema import Schema, SchemaError


class SchemaValidatorOutput:
    status: bool
    validated_payload: any
    error: SchemaError


class SchemaValidator:
    def __init__(self, schema: Schema):
        self.schema = schema

    def validate(self, payload: any) -> SchemaValidatorOutput:
        try:
            validated = self.schema.validate(payload)

            print("[SchemaValidator] The payload is valid, schema validation succeeded")

            return {"status": True, "validated_payload": validated}
        except SchemaError as schema_error:
            print(f"[SchemaValidator] The payload is invalid, errors: {schema_error}")

            return {"status": False, "error": schema_error}
