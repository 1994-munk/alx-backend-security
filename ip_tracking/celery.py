# ip_tracking/celery.py
# ==============================================
# Celery configuration file for Django project
# ==============================================

import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip_tracking.settings')

# Create the Celery app instance
app = Celery('ip_tracking')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Simple debug task to confirm Celery setup"""
    print(f'Request: {self.request!r}')
