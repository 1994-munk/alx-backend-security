# ip_tracking/views.py

from django.http import HttpResponse
from ratelimit.decorators import ratelimit

# 👤 Anonymous users: 5 requests per minute
@ratelimit(key='ip', rate='5/m', block=True)
def public_view(request):
    return HttpResponse("This view is rate-limited for anonymous users.")

# 🔐 Authenticated users: 10 requests per minute
@ratelimit(key='user_or_ip', rate='10/m', block=True)
def login_view(request):
    return HttpResponse("This login view is rate-limited for logged-in users.")
