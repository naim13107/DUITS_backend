# users/views.py
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response

class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        requester = request.user
        is_admin = (
            requester.is_staff or 
            requester.is_superuser or 
            getattr(requester, 'role', '') == 'Admin'
        )
        if is_admin:
            instance = self.get_object()
            if instance == requester:
                return Response(
                    {'detail': "You can't delete your own account here."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)