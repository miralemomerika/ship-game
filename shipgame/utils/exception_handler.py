from rest_framework.exceptions import APIException

class CustomException(APIException):
    status_code = 400
    default_detail = 'An error occurred'
    default_code = 'error'

    def __init__(self, detail=None, code=None, metadata=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code
        self.metadata = metadata or {}

        super().__init__(detail=self.detail, code=self.code)