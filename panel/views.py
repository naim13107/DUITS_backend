# panel/views.py
from rest_framework import viewsets, permissions, filters
from .models import PanelMember
from .serializers import PanelMemberSerializer

class PanelMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing DUITS executive panel members.
    Strictly locked down so only Admins can assign designations.
    """
    # select_related pulls user data efficiently in a single query
    queryset = PanelMember.objects.all().select_related('user').order_by('order')
    serializer_class = PanelMemberSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['session', 'designation', 'panel_type']

    def get_permissions(self):
        """
        Dynamically assign permissions based on absolute Admin authority.
        """
        # 1. PUBLIC: Anyone (even visitors) can view the panel directory
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
            
        # 2. SUPER ADMINS ONLY: Only true Admins can create, edit, or remove 
        # panel designations (like President, VP, etc.)
        # (This uses Django's built-in check for is_staff=True)
        return [permissions.IsAdminUser()]