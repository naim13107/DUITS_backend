from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='events/covers/', blank=True, null=True)
    
    # A draft system so admins can prepare events before showing them on the website
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Automatically sorts so the newest events show up first
        ordering = ['-date']

    def __str__(self):
        return self.title