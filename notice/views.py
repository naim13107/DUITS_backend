from rest_framework import viewsets, permissions
from .models import Notice
from .serializers import NoticeSerializer
from permissions import IsExecutive

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.filter(is_active=True)
    serializer_class = NoticeSerializer

    def get_permissions(self):
        # Allow anyone to view notices
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # Require 'IsExecutive' permission for creating/updating/deleting
        return [IsExecutive()]

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)