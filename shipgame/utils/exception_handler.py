from rest_framework.exceptions import APIException

class BadRequestException(APIException):
    status_code = 400
    default_detail = 'An error occurred'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

        super().__init__(detail=self.detail)


class ServerErrorException(APIException):
    status_code = 500
    default_detail = 'Server error occurred'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

        super().__init__(detail=self.detail)
