from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = None

        # 1️⃣ Check for Authorization header first
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]  # Extract the token

        # 2️⃣ If no token in header, check for cookies
        if not access_token:
            access_token = request.COOKIES.get('access_token')

        # 3️⃣ If no token is found, return None (AllowAny will work)
        if not access_token:
            return None  # This ensures unauthenticated users can access views with AllowAny

        try:
            # Validate and decode the token
            token = AccessToken(access_token)
            user = CustomUser.objects.get(id=token['user_id'])
            return (user, token)

        except CustomUser.DoesNotExist:
            return None  # Prevent authentication failure from blocking AllowAny views

        except Exception:
            return None  # Prevent errors from blocking AllowAny views


from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class that verifies API keys passed in headers.
    """
    def authenticate(self, request):
        # Get the API key from headers
        api_key = request.headers.get('X-API-KEY')

        if not api_key:
            return None  # No authentication, move to the next authentication class

        # Compare the API key with the one in settings (or fetch from DB)
        if api_key != settings.API_KEY:
            raise AuthenticationFailed("Invalid API key")

        return (None, None)  # No user object needed for service-to-service auth

