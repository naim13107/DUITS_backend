from django.db import models
from django.core.exceptions import ValidationError

class RecruitmentSettings(models.Model):
    session_name = models.CharField(max_length=100, help_text="e.g., Spring 2024, Fall 2024")
    is_open = models.BooleanField(default=False)
    application_fee = models.DecimalField(max_digits=6, decimal_places=2, default=300.00)
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = "Recruitment Setting"
        verbose_name_plural = "Recruitment Settings"

    def clean(self):
        # Ensure only one active recruitment setting exists at a time
        if self.is_open:
            active_settings = RecruitmentSettings.objects.filter(is_open=True).exclude(pk=self.pk)
            if active_settings.exists():
                raise ValidationError("Another recruitment session is currently open. Close it before opening a new one.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "OPEN" if self.is_open else "CLOSED"
        return f"{self.session_name} ({status})"


class RecruitmentApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    recruitment_drive = models.ForeignKey(
        'RecruitmentSettings', 
        on_delete=models.CASCADE, # <--- Change SET_NULL to CASCADE!
        null=True, 
        blank=True, 
        related_name='applications'
    )

    # Personal Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    # University Info
    department = models.CharField(max_length=100)
    session = models.CharField(max_length=20)
    hall = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    
    # Application Info
    skills = models.TextField(help_text="List your technical/soft skills")
    motivation = models.TextField(help_text="Why do you want to join DUITS?")
    
    # Links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    
    # Payment & Processing
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    payment_response = models.JSONField(blank=True, null=True, help_text="Store full AamarPay JSON response")
    pdf_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.student_id}"