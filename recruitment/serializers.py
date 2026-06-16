# recruitment/serializers.py
from rest_framework import serializers
from .models import RecruitmentSettings, RecruitmentApplication

class RecruitmentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentSettings
        fields = ('id', 'session_name', 'is_open', 'application_fee', 'deadline')


class RecruitmentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentApplication
        fields = (
            'id', 'full_name', 'email', 'phone', 'department', 'session', 
            'hall', 'student_id', 'skills', 'motivation', 'github', 
            'linkedin', 'portfolio', 'payment_status', 'transaction_id', 
            'payment_response', 'pdf_url', 'created_at'
        )
        
        # SECURITY: Strictly protect all payment and transaction details!
        # The applicant can only submit their personal info; the server handles the rest.
        read_only_fields = (
            'payment_status', 
            'transaction_id', 
            'payment_response', 
            'pdf_url', 
            'created_at'
        )