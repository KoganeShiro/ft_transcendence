from django.utils.timezone import now, timedelta
from django.utils.deprecation import MiddlewareMixin

class UpdateLastSeenMiddleware:
    """
    Middleware to update the 'last_seen' field of authenticated users on each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.is_logout_req(request) and request.user != None and request.user.is_authenticated:
            user = request.user
            user.last_seen = now() - timedelta(seconds=600)
            user.save(update_fields=['last_seen'])         
        elif request.user != None and request.user.is_authenticated:
            user = request.user
            user.last_seen = now()
            user.save(update_fields=['last_seen'])  # Only updates the 'last_seen' field
        return response
    
    def is_logout_req(self, request):
        # Example condition: skip middleware for requests to the '/api/health/' endpoint
        if request.path == '/api/logout/':
            return True
        # Add more conditions as needed
        return False