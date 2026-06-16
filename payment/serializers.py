# payment/serializers.py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """
    Used by the Executive Panel to view the payment ledger.
    tracking_id  → our internal UUID sent to aamarPay as tran_id (shown to users as transaction reference)
    transaction_id → aamarPay's pg_txnid, populated only after a COMPLETED callback
    """
    applicant_name = serializers.ReadOnlyField(source='application.full_name')
    department = serializers.ReadOnlyField(source='application.department')

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = [
            'tracking_id',
            'transaction_id',
            'amount',
            'status',
            'created_at',
            'updated_at',
        ]