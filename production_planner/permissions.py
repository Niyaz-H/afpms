from rest_framework import permissions
from core.models import Profile

class IsFactoryManager(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'Factory Manager' role to edit objects.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the factory manager.
        return request.user.profile.role == Profile.Role.FACTORY_MANAGER