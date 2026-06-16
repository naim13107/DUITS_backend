# analytics/serializers.py
from rest_framework import serializers
from .models import SystemLog

class SystemLogSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SystemLog
        fields = (
            'id', 
            'user', 
            'user_email', 
            'action', 
            'details', 
            'ip_address', 
            'timestamp'
        )
        read_only_fields = (
            'user', 
            'action', 
            'details', 
            'ip_address', 
            'timestamp'
        )