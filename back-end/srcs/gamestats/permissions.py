from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit or delete a game.
    Other users can only view it.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow modification if user is admin
        return request.user and request.user.is_staff