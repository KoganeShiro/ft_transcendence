from rest_framework.permissions import BasePermission

class IsAdminOrSelf(BasePermission):
    """
    Custom permission to allow only admins or the user themselves to modify/delete their account.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can modify/delete any user
        if request.user.is_staff:
            return True

        # Regular users can only modify/delete their own account
        return obj == request.user
