from django.db import models
from django.conf import settings

class Notice(models.Model):
    CATEGORY_CHOICES = (
        ('GENERAL', 'General'),
        ('URGENT', 'Urgent'),
        ('EVENT', 'Event'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL')
    is_active = models.BooleanField(default=True)
    
    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notices')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.category})"