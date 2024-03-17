class ApiError(Exception):
    def __init__(self, message="A custom error occurred",code=500):
        self.message = message
        self.code = code
        super().__init__(self.message)