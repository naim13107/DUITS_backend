# analytics/views.py
from rest_framework import viewsets, filters

# Import your custom permissions
from permissions import IsExecutive

from .models import SystemLog
from .serializers import SystemLogSerializer

class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing system logs.
    Strictly read-only to prevent tampering with the audit trail.
    """
    # Use select_related to efficiently fetch the user data, and order newest first
    queryset = SystemLog.objects.all().select_related('user').order_by('-timestamp')
    serializer_class = SystemLogSerializer
    
    # Updated to use your custom DUITS hierarchy
    # Executives, Junior Executives, and Admins can view the logs
    permission_classes = [IsExecutive]
    
    # Allow searching logs by action, email, or IP address
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'details', 'user__email', 'ip_address']
    ordering_fields = ['timestamp']