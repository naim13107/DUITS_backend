# article/serializers.py
from rest_framework import serializers
from .models import Category, Article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Used for the public feed and Admin Dashboard list.
    """
    # Dynamically fetch actual names so the frontend public feed can display them easily
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        # FIXED: Added 'status' back so the Admin Dashboard can read the current status on reload!
        fields = (
            'id', 'title', 'cover_image', 'category_name', 
            'author_name', 'created_at', 'status'
        ) 


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    Used when a Viewer clicks an article to read it, or an Author/Exec edits it.
    """
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'cover_image', 'tags', 
            'category', 'category_name', 'author', 'author_name', 
            'status', 'created_at', 'updated_at'
        )
        
        # SECURITY PROJECTIONS:
        read_only_fields = ('author', 'created_at', 'updated_at')

    def validate_status(self, value):
        """
        SECURITY CHECK: Ensures that ONLY Admins and Executives can approve/reject articles.
        If a normal member tries to intercept the API and approve their own article, it blocks them.
        """
        request = self.context.get('request')
        
        if request and request.user:
            user = request.user
            user_role = getattr(user, 'role', '').lower()
            
            # If the user is an Admin, Executive, or Junior Executive, allow the status change
            if user.is_superuser or user.is_staff or user_role in ['executive', 'junior_executive', 'admin']:
                return value
                
            # If a regular member tries to change the status, block the request
            raise serializers.ValidationError("Permission Denied: Only Executives can approve or reject articles.")
            
        return value