from django.db import models
from django.conf import settings

class PanelMember(models.Model):
    PANEL_CHOICES = (
        ('CURRENT', 'Current Panel'),
        ('EX', 'Ex Panel'),
    )
    
    # Links to your Custom User Model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='panel_roles')
    designation = models.CharField(max_length=100, help_text="e.g., President, General Secretary")
    panel_type = models.CharField(max_length=10, choices=PANEL_CHOICES, default='CURRENT')
    session = models.CharField(max_length=50, help_text="e.g., 2023-2024")
    
    # Determines the hierarchy on the frontend website
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first (e.g., 1 for President)")

    class Meta:
        # Automatically sorts queries by the 'order' field
        ordering = ['order']
        verbose_name = "Panel Member"
        verbose_name_plural = "Panel Members"

    def __str__(self):
        return f"{self.user.full_name} - {self.designation} ({self.panel_type})"