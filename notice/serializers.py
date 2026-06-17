from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'category', 'is_active', 'created_at', 'author_name']