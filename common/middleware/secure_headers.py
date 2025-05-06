class SecureHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Frame-Options"] = "DENY"
        response["X-Content-Type-Options"] = "nosniff"
        response["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains" # noqa501
        response["Content-Security-Policy"] = "default-src 'self'"
        return response
