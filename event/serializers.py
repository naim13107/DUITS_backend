# event/serializers.py
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 
            'title', 
            'description', 
            'date', 
            'location', 
            'cover_image', 
            'is_published', 
            'created_at'
        )
        
        # Security: Prevent unauthorized publishing via API
        read_only_fields = ('created_at',)