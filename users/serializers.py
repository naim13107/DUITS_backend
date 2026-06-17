# users/serializers.py
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

User = get_user_model()

class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        # MAKE SURE 'is_superuser' AND 'role' ARE IN THIS LIST!
        fields = (
            'id', 
            'email', 
            'full_name', 
            'student_id', 
            'department', 
            'hall', 
            'session', 
            'phone', 
            'profile_picture',
            'role',          # <--- Added
            'is_superuser'   # <--- Added
        )


class CustomUserSerializer(BaseUserSerializer):
    """
    Serializer used when fetching or updating a user profile.
    """
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'full_name', 'phone', 'department', 'hall', 
            'session', 'student_id', 'profile_image', 'role', 'bio', 
            'join_date', 'is_verified'
        )
        # SECURITY: Prevent users from upgrading their own role or verification status via API!
        read_only_fields = ('email', 'role', 'join_date', 'is_verified')