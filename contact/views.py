# contact/views.py
from rest_framework import viewsets, permissions, filters

# 1. Import your custom DUITS hierarchy permission
from permissions import IsExecutive

from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the public to submit contact messages,
    but only allows Executives and Admins to read and manage them.
    """
    # Order by newest first so executives see fresh messages at the top
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    
    # Enable executives to search messages by email or name
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'is_read']

    def get_permissions(self):
        """
        Dynamically assign permissions based on the DUITS hierarchy.
        """
        # 1. PUBLIC: Anyone can submit a contact form (POST)
        if self.action == 'create':
            return [permissions.AllowAny()]
            
        # 2. EXECUTIVES: Only Junior Executives, Executives, and Admins 
        # can view the list, read a specific message, or delete them.
        return [IsExecutive()]