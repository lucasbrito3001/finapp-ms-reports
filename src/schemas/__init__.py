class InvalidSchemaException(BaseException):
    def __init__(self, error):
        super().__init__()
        self.error = error