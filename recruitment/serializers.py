# recruitment/serializers.py
from rest_framework import serializers
from .models import RecruitmentSettings, RecruitmentApplication

class RecruitmentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentSettings
        fields = ('id', 'session_name', 'is_open', 'application_fee', 'deadline')


class RecruitmentApplicationSerializer(serializers.ModelSerializer):
    # NEW: Expose the actual drive name to the frontend
    recruitment_drive_name = serializers.ReadOnlyField(source='recruitment_drive.session_name')

    class Meta:
        model = RecruitmentApplication
        fields = (
            'id', 'full_name', 'email', 'phone', 'department', 'session', 
            'hall', 'student_id', 'skills', 'motivation', 'github', 
            'linkedin', 'portfolio', 'payment_status', 'transaction_id', 
            'payment_response', 'pdf_url', 'created_at',
            'recruitment_drive',         # <--- Added
            'recruitment_drive_name'     # <--- Added
        )
        
        read_only_fields = (
            'payment_status', 'transaction_id', 'payment_response', 
            'pdf_url', 'created_at', 'recruitment_drive', 'recruitment_drive_name'
        )