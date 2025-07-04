class ExcelOperationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class InvalidActionSchema(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class FileNotFound(Exception):
    def __init__(self, file_id: str):
        self.message = f"File with ID '{file_id}' not found."
        super().__init__(self.message)
