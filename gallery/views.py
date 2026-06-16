# gallery/views.py
from rest_framework import viewsets, permissions, filters
from .models import GalleryImage
from .serializers import GalleryImageSerializer

# 1. Import your custom DUITS hierarchy permission
from permissions import IsExecutive

class GalleryImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing DUITS gallery images.
    Secured dynamically based on the organizational hierarchy.
    """
    # Using order_by('-id') ensures the newest uploaded photos always appear first
    queryset = GalleryImage.objects.all().select_related('uploaded_by').order_by('-id')
    serializer_class = GalleryImageSerializer
    
    # Optional: Enable filtering in case you want to search photos by caption
    filter_backends = [filters.SearchFilter]
    search_fields = ['caption'] # Update this if your model uses a different field for text, like 'description'

    def get_permissions(self):
        """
        Dynamically assign permissions based on what the user is trying to do.
        """
        # 1. PUBLIC: Anyone (even without an account) can view the gallery photos
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
            
        # 2. EXECUTIVES: Only Junior Executives, Executives, and Admins 
        # can upload new photos, edit captions, or delete images.
        return [IsExecutive()]

    def perform_create(self, serializer):
        """
        Automatically sets the uploader to the logged-in Executive/Admin.
        """
        serializer.save(uploaded_by=self.request.user)