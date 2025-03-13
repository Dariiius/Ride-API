"""
User app custom permission
"""
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to allow access only to users with the role of 'admin'.
    """

    def has_permission(self, request, view):
        return request.user and getattr(request.user, "role", None) == "admin"