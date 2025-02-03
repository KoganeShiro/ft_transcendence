from social_core.backends.oauth import BaseOAuth2
import logging

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

    def auth_extra_arguments(self):
        """Ensure redirect_uri is always sent in the OAuth request"""
        print("auth_extra_arguments")
        return {'redirect_uri': self.setting('REDIRECT_URI')}
    
    def request_access_token(self, *args, **kwargs):
        print("request_access_token")
        """Overrides request_access_token to add debugging"""
        logger.debug(f"OAuth Request URL: {self.ACCESS_TOKEN_URL}")
        
        logger.debug(f"OAuth Request Data: {args}, {kwargs}")

        response = super().request_access_token(*args, **kwargs)
        logger.debug(f"OAuth Response Status: {response.status_code}")
        logger.debug(f"OAuth Response Content: {response.text}")

        return response

 #   def request_access_token(self, *args, **kwargs):
 #       """Ensure access token is requested using POST"""
 #       kwargs['method'] = 'POST'
 #       return super().request_access_token(*args, **kwargs)

    
  #  def get_user_details(self, response):
  #      """Extract user details from provider response"""
  #      return {
  #          'username': response.get('login'),
  #          'email': response.get('email'),
  #          'first_name': response.get('first_name'),
  #          'last_name': response.get('last_name'),
  #      }
    
    def auth_complete(self, *args, **kwargs):
        self.redirect_uri = self.strategy.build_absolute_uri(self.redirect_uri)
        return super(FortyTwoOAuth2, self).auth_complete(*args, **kwargs)
    

