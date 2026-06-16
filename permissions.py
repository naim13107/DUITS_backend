# permissions.py
from rest_framework import permissions

class IsExecutive(permissions.BasePermission):
    """
    Allows access strictly to Executives, Junior Executives, and Admins.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'role', '') in ['Executive', 'Junior Executive', 'Admin'])
        )

class IsMember(permissions.BasePermission):
    """
    Allows access to Members and anyone above them.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'role', '') in ['Member', 'Executive', 'Junior Executive', 'Admin'])
        )

class IsAuthorOrExecutive(permissions.BasePermission):
    """
    Allows a Member to edit their OWN object.
    Allows Executives/Admins to edit ANY object.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Admins and Execs bypass the ownership check
        if request.user.is_staff or getattr(request.user, 'role', '') in ['Executive', 'Junior Executive', 'Admin']:
            return True
            
        # Members can only pass if they own it
        owner = getattr(obj, 'author', getattr(obj, 'user', None))
        return bool(owner == request.user)