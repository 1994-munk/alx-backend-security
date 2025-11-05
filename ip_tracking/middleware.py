from datetime import datetime
from .models import RequestLog

# Custom middleware class
class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Django passes the next middleware or view

    def __call__(self, request):
        # Extract the client IP address
        ip_address = self.get_client_ip(request)
        # Create a new log record
        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            timestamp=datetime.now()
        )
        # Continue processing the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Some proxies set HTTP_X_FORWARDED_FOR header
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
