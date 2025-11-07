from django.db import models

# This model stores details about every incoming request
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255) 
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    
class BlockedIP(models.Model):
    """
    Stores blacklisted IP addresses that should be blocked from accessing the site.
    """
    ip_address = models.GenericIPAddressField(unique=True)
  
       
    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"
