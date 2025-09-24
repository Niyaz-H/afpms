from functools import wraps
from django.core.exceptions import PermissionDenied
from .models import Profile

def role_required(allowed_roles):
    """
    Decorator for views that checks that the user has one of the allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                raise PermissionDenied

            if profile.role not in allowed_roles:
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator