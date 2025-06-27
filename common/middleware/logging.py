class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import logging
        from time import time

        from django.utils.timezone import now

        logger = logging.getLogger("django.request")

        start = time()
        response = self.get_response(request)
        duration = round(time() - start, 3)

        logger.info(f"{now()} - {request.method} {request.path} by {getattr(request.user, 'username', 'anon')} in {duration}s")  # noqa: E501

        return response
