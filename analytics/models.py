from django.db import models
from django.conf import settings

class SystemLog(models.Model):
    # Allow null/blank because some actions (like failed logins) might happen when no user is authenticated
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255, help_text="e.g., LOGIN, APPLY, PAYMENT_SUCCESS")
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "System Log"

    def __str__(self):
        actor = self.user.email if self.user else "Anonymous/System"
        return f"[{self.action}] by {actor} at {self.timestamp}"