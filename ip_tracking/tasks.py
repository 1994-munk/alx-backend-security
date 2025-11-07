# ip_tracking/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP

# 🕒 Task runs hourly to detect anomalies
@shared_task
def detect_anomalies():
    # Simulate some fake log data (for demonstration)
    logs = [
        {'ip': '192.168.1.10', 'path': '/login', 'requests_last_hour': 120},
        {'ip': '192.168.1.11', 'path': '/admin', 'requests_last_hour': 5},
        {'ip': '192.168.1.12', 'path': '/home', 'requests_last_hour': 15},
    ]

    suspicious_paths = ['/login', '/admin']
    flagged = 0

    for log in logs:
        if log['requests_last_hour'] > 100 or log['path'] in suspicious_paths:
            SuspiciousIP.objects.update_or_create(
                ip_address=log['ip'],
                defaults={
                    'reason': f"High traffic ({log['requests_last_hour']}/hr) or sensitive path access {log['path']}",
                    'timestamp': timezone.now()
                }
            )
            flagged += 1

    return f"{flagged} suspicious IPs flagged."
