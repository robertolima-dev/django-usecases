import uuid


class CorrelationIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4())) # noqa501
        response = self.get_response(request)
        response["X-Correlation-ID"] = request.correlation_id
        return response
