# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    # Define the RBAC (Role-Based Access Control) choices
    ROLE_CHOICES = (
        ('Visitor', 'Visitor'),
        ('Member', 'Member'),
        ('Junior Executive', 'Junior Executive'),
        ('Executive', 'Executive'),
        ('Admin', 'Admin'),
    )

    # 1. Remove the username field
    username = None
    
    # 2. Set email as the primary identifier
    email = models.EmailField(unique=True)
    
    # 3. DUITS Specific Fields
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    hall = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=20, blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    
    # 4. Profile & Status Fields
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Visitor')
    bio = models.TextField(blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    # 5. Configuration
    USERNAME_FIELD = 'email'
    
    # REQUIRED_FIELDS prompts the terminal for these when running createsuperuser
    REQUIRED_FIELDS = ['full_name'] 

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"