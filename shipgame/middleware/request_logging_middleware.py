import logging
import json

logger = logging.getLogger('request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_data = {
            'request_method': request.method,
            'request_path': request.path,
            'request_query_params': request.GET.dict(),
            'request_body': request.body.decode(),
        }
        logger.info('Request received', extra=log_data)

        response = self.get_response(request)

        return response
