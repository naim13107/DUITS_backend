from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response

class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)