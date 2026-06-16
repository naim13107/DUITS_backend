# gallery/serializers.py
from rest_framework import serializers
from .models import GalleryImage

class GalleryImageSerializer(serializers.ModelSerializer):
    # Frontend Bonus: Send the uploader's name along with the image
    uploaded_by_name = serializers.ReadOnlyField(source='uploaded_by.full_name')

    class Meta:
        model = GalleryImage
        fields = ('id', 'image', 'caption', 'uploaded_by', 'uploaded_by_name', 'created_at')
        
        # We will automatically set 'uploaded_by' in the View based on the logged-in admin
        read_only_fields = ('uploaded_by', 'created_at')