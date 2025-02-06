from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin

class UpdateLastSeenMiddleware:
    """
    Middleware to update the 'last_seen' field of authenticated users on each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = request.user
            user.last_seen = now()
            user.save(update_fields=['last_seen'])  # Only updates the 'last_seen' field
        return response