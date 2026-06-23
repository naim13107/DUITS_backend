# users/serializers.py
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

User = get_user_model()

class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'full_name', 'student_id', 
            'department', 'hall', 'session', 'phone', 
            'profile_image', 'role', 'is_superuser'
        )
        # Remove 'role' from here so it can be updated
        read_only_fields = ('email', 'join_date', 'is_verified')


