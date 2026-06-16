# panel/serializers.py
from rest_framework import serializers
from .models import PanelMember

class PanelMemberSerializer(serializers.ModelSerializer):
    # Frontend Bonus: Pull the user details directly into the panel response
    full_name = serializers.ReadOnlyField(source='user.full_name')
    email = serializers.ReadOnlyField(source='user.email')
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)

    class Meta:
        model = PanelMember
        fields = (
            'id', 
            'user', 
            'full_name', 
            'email', 
            'profile_image', 
            'designation', 
            'panel_type', 
            'session', 
            'order'
        )