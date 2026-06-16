# article/serializers.py
from rest_framework import serializers
from .models import Category, Article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Used ONLY for the public feed. Lightweight and hides the main content.
    """
    # Dynamically fetch actual names so the frontend public feed can display them easily
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        # Notice 'content' and 'status' are completely removed to keep the payload fast and secure
        fields = (
            'id', 'title', 'cover_image', 'category_name', 
            'author_name', 'created_at'
        ) 


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Used when a Viewer clicks an article to read it, or an Author/Exec edits it.
    """
    # 1. Dynamically fetch the actual names for the frontend
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'cover_image', 'tags', 
            'category', 'category_name', 'author', 'author_name', 
            'status', 'created_at', 'updated_at'
        )
        
        # 2. SECURITY PROJECTIONS:
        # - author: Set automatically in the View based on who is logged in.
        # - status: Regular users cannot approve their own articles.
        # - dates: Should never be manually edited.
        read_only_fields = ('author', 'status', 'created_at', 'updated_at')