# article/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q 

from .models import Category, Article
from .serializers import CategorySerializer, ArticleListSerializer, ArticleDetailSerializer

# Import your custom hierarchical permissions from the root directory
from permissions import IsExecutive, IsMember, IsAuthorOrExecutive


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    # Force default permission to AllowAny
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsExecutive()]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed, created, or edited.
    Combines advanced RBAC permissions with search, sorting, and status filtering.
    """
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    
    # Force default permission to AllowAny to prevent 401 unauthorized errors for visitors
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer 
        return ArticleDetailSerializer 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [IsMember()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthorOrExecutive()]
        elif self.action == 'destroy':
            return [IsExecutive()]
        return super().get_permissions()

    # --- BULLETPROOF PUBLIC LIST METHOD ---
    def list(self, request, *args, **kwargs):
        """
        Explicitly serves APPROVED articles for the list view, completely bypassing 
        the request.user checks that cause JWT crashes for anonymous users.
        """
        queryset = Article.objects.filter(status='APPROVED').order_by('-created_at')
        
        category_slug = request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # --- BULLETPROOF PUBLIC RETRIEVE METHOD ---
    def retrieve(self, request, *args, **kwargs):
        """
        Allows anyone to retrieve an APPROVED article, but safely restricts PENDING/REJECTED ones.
        """
        instance = self.get_object()
        
        if instance.status != 'APPROVED':
            user = request.user
            if not user or not user.is_authenticated:
                raise PermissionDenied("This article is not yet approved.")
            
            if not (user.is_staff or getattr(user, 'role', '').lower() in ['executive', 'junior_executive', 'admin'] or instance.author == user):
                raise PermissionDenied("You do not have permission to view this article.")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Fallback logic for Admin dashboard and Create/Update/Delete operations.
        Wrapped in a try-except to prevent anonymous user crashes.
        """
        queryset = Article.objects.all().order_by('-created_at')
        
        try:
            user = self.request.user
            if user and user.is_authenticated:
                if user.is_staff or getattr(user, 'role', '').lower() in ['executive', 'junior_executive', 'admin']:
                    return queryset
                else:
                    return queryset.filter(Q(status='APPROVED') | Q(author=user))
        except Exception:
            pass
            
        return queryset.filter(status='APPROVED')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, status='PENDING')