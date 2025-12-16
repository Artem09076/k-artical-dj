from .metrics import (HTTP_REQUESTS_TOTAL,
                      HTTP_RESPONSES_2XX, HTTP_RESPONSES_4XX, HTTP_RESPONSES_5XX)
import uuid

class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        HTTP_REQUESTS_TOTAL.inc()

        status_code = response.status_code

        if 200 <= status_code < 300:
            HTTP_RESPONSES_2XX.inc()
        elif 400 <= status_code < 500:
            HTTP_RESPONSES_4XX.inc()
        elif 500 <= status_code < 600:
            HTTP_RESPONSES_5XX.inc()

        return response
    
class CorrelationIdMiddleware:
    HEADER_NAME = "HTTP_X_CORRELATION_ID"
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        correlation_id = request.META.get(self.HEADER_NAME)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        request.correlation_id = correlation_id
        

        response = self.get_response(request)
        response["X-Correlation-ID"] = correlation_id
        return response