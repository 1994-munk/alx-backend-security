import ipinfo
from django.utils import timezone
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP



class IPLoggingMiddleware:
    """
    Middleware that:
      - Blocks requests from IPs in BlockedIP
      - Logs IP, path, timestamp, and geolocation
      - Caches geolocation lookups for 24 hours
    """

    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

        # Initialize IPInfo handler (replace with your actual API token)
        access_token = "your_ipinfo_token_here"
        self.handler = ipinfo.getHandler(access_token)

    def __call__(self, request):
        """
        Called for each request before the view (and later middleware) are called.
        """
        ip_address = self.get_client_ip(request)
        path = request.path

        # Fetch geolocation data from cache if available
        location_data = cache.get(ip_address)
        
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: your IP has been blocked.")

        path = request.path
        location_data = cache.get(ip_address)


        if not location_data:
            try:
                details = self.handler.getDetails(ip_address)
                country = details.country
                city = details.city
            except Exception:
                country = None
                city = None

            # Cache result for 24 hours (86,400 seconds)
            location_data = {'country': country, 'city': city}
            cache.set(ip_address, location_data, timeout=86400)

        # Log request in the database
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            timestamp=timezone.now(),
            country=location_data.get('country'),
            city=location_data.get('city')
        )

        # Continue request processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Extracts the client's IP address from the request headers.
        Handles both direct and proxied requests.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip