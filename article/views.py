# article/views.py
from rest_framework import viewsets, permissions, filters
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

    def get_permissions(self):
        """
        Anyone can view categories, but only Executives and Admins can create/edit them.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsExecutive()]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed, created, or edited.
    Combines advanced RBAC permissions with search, sorting, and status filtering.
    """
    # Enable searching and sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        """
        Returns different data depending on what the user is doing.
        """
        # Public feed gets the lightweight serializer (Title, ID, Cover Photo)
        if self.action == 'list':
            return ArticleListSerializer 
        # Clicking an article loads the heavy serializer (Full content)
        return ArticleDetailSerializer 

    def get_permissions(self):
        """
        Routes traffic securely based on your specific DUITS hierarchy.
        """
        # 1. PUBLIC: Anyone (even no login) can see the list of titles/covers
        if self.action == 'list':
            return [permissions.AllowAny()]
            
        # 2. VIEWER: To open and READ the full article, you must be logged in
        elif self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
            
        # 3. MEMBER: Only Members (and above) can POST/Create an article
        elif self.action == 'create':
            return [IsMember()]
            
        # 4. AUTHOR / EXEC: Only the original Author or an Executive can edit
        elif self.action in ['update', 'partial_update']:
            return [IsAuthorOrExecutive()]
            
        # 5. EXECUTIVE: Only Executives and Admins can DELETE an article
        elif self.action == 'destroy':
            return [IsExecutive()]
            
        return super().get_permissions()

    def get_queryset(self):
        """
        Custom logic to determine exactly which articles are returned based on Rank & Status.
        """
        queryset = Article.objects.all().order_by('-created_at')
        user = self.request.user

        # 1. VISIBILITY SECURITY:
        if user.is_authenticated and (user.is_staff or getattr(user, 'role', '') in ['executive', 'junior_executive']):
            # EXECUTIVES & ADMINS: Can see absolutely everything (Approved, Pending, Rejected)
            pass 
        elif user.is_authenticated:
            # MEMBERS & VIEWERS: Can see all 'APPROVED' articles, PLUS their own 'PENDING' articles
            queryset = queryset.filter(Q(status='APPROVED') | Q(author=user))
        else:
            # PUBLIC (Not logged in): Can strictly only see 'APPROVED' articles
            queryset = queryset.filter(status='APPROVED')

        # 2. CATEGORY FILTERING:
        # Allows frontend to filter articles by category slug (?category=tech-news)
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def perform_create(self, serializer):
        """
        Forcefully grabs the logged-in user from the JWT token and sets them as the author.
        Also sets the default status to PENDING so an Executive has to review it.
        """
        serializer.save(author=self.request.user, status='PENDING')