# payment/models.py
import uuid
from django.db import models
from recruitment.models import RecruitmentApplication

def generate_32_char_uuid():
    """Generates a secure 32-character unique hex string."""
    return uuid.uuid4().hex

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    application = models.ForeignKey(
        RecruitmentApplication,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )

    # Primary tracking key — sent to aamarPay as tran_id, and also our public transaction ID.
    # "tracking_id" column already exists in DB, no migration needed.
    tracking_id = models.CharField(
        max_length=32,
        default=generate_32_char_uuid,
        unique=True,
        db_index=True,
        editable=False
    )

    # Stores aamarPay's own pg_txnid after a successful callback.
    # "transaction_id" column already exists in DB, no migration needed.
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, default='aamarPay')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trx: {self.tracking_id} | {self.status}"