from social_core.backends.oauth import BaseOAuth2
from django.conf import settings
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class FortyTwoOAuth2(BaseOAuth2):
    """42 OAuth2 authentication backend"""
    name = '42'
    AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
    USER_DATA_URL = 'https://api.intra.42.fr/v2/me'    
    STATE_PARAMETER = False
    ACCESS_TOKEN_METHOD = "POST"
    REDIRECT_STATE = False
    DEFAULT_SCOPE = []
    EXTRA_DATA = ["expires_in"]

    def get_redirect_uri(self, state=None):
        """Ensure redirect_uri is always sent in the OAuth request"""        
        return settings.REDIRECT_URI

    
    def request_access_token(self, *args, **kwargs):
        print("request_access_token")
        """Overrides request_access_token to add debugging"""
        logger.debug(f"OAuth Request URL: {self.ACCESS_TOKEN_URL}")
        
        logger.debug(f"OAuth Request Data: {args}, {kwargs}")
        response = None
        try:
            response = super().request_access_token(*args, **kwargs)
            logger.debug(f"OAuth Response: {response}")
        except Exception as e:
            logger.error(f"OAuth Request Error: {e}")
            raise e

        return response

    def get_user_details(self, response):
        print("get_user_details")
        return {
            'username': response.get('login'),
            'email': response.get('email'),            
        }
    
    def user_data(self, access_token, *args, **kwargs):
         return self.get_json(self.USER_DATA_URL, headers={'Authorization': f'Bearer {access_token}'})
    

