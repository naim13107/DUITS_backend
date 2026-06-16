# contact/serializers.py
from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = (
            'id', 
            'name', 
            'email', 
            'subject', 
            'message', 
            'is_read', 
            'created_at'
        )
        
        # SECURITY: Prevent the public from manipulating admin-only fields.
        # When a POST request is made, it will default is_read to False and ignore any attempts to override it.
        read_only_fields = ('is_read', 'created_at')