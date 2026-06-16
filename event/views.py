# event/views.py
from rest_framework import viewsets, permissions, filters
from .models import Event
from .serializers import EventSerializer

# 1. Import your custom DUITS hierarchy permission
from permissions import IsExecutive

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing DUITS events.
    Secured dynamically based on the organizational hierarchy.
    """
    serializer_class = EventSerializer
    
    # Enable searching and sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at']

    def get_permissions(self):
        """
        Dynamically assign permissions based on what the user is trying to do.
        """
        # 1. PUBLIC: Anyone (even without an account) can view the events
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
            
        # 2. EXECUTIVES: Only Junior Executives, Executives, and Admins 
        # can create, update, or delete events.
        return [IsExecutive()]

    def get_queryset(self):
        """
        Custom logic to hide unpublished "draft" events from the public.
        """
        # Order by date so the newest/upcoming events show up properly
        queryset = Event.objects.all().order_by('-date')
        user = self.request.user
        
        # EXECUTIVES & ADMINS: See absolutely everything (Published and Drafts)
        if user.is_authenticated and (user.is_staff or getattr(user, 'role', '') in ['Executive', 'Junior Executive', 'Admin']):
            pass 
            
        # PUBLIC, VISITORS & MEMBERS: Strictly only see published events
        else:
            queryset = queryset.filter(is_published=True)
            
        return queryset