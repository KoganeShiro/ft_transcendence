from social_core.backends.oauth import BaseOAuth2

class FortyTwoOAuth2(BaseOAuth2):
    """42 OAuth2 authentication backend"""
    name = '42'
    AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
    USER_DATA_URL = 'https://api.intra.42.fr/v2/me'
    DEFAULT_SCOPE = ['profile']
    REDIRECT_STATE = False
    STATE_PARAMETER = False

    def auth_extra_arguments(self):
        """Ensure redirect_uri is always sent in the OAuth request"""
        return {'redirect_uri': self.setting('REDIRECT_URI')}

    def request_access_token(self, *args, **kwargs):
        """Ensure access token is requested using POST"""
        kwargs['method'] = 'POST'
        return super().request_access_token(*args, **kwargs)

    
    def get_user_details(self, response):
        """Extract user details from provider response"""
        return {
            'username': response.get('login'),
            'email': response.get('email'),
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
        }