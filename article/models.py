from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories" # Fixes spelling in Django Admin

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the category name if it's empty
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True)
    
    # Simple CharField for comma-separated tags (e.g., "tech, ai, coding")
    tags = models.CharField(max_length=255, help_text="Enter comma-separated tags", blank=True)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    
    # We use settings.AUTH_USER_MODEL to safely link to your new Custom User model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Standard best practice to track edits

    def __str__(self):
        return f"{self.title} by {self.author.full_name}"