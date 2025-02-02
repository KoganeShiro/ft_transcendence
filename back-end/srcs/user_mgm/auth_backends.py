from social_core.backends.oauth import BaseOAuth2

class FortyTwoOAuth2(BaseOAuth2):
    """42 OAuth2 authentication backend"""
    name = '42'
    AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
    USER_DATA_URL = 'https://api.intra.42.fr/v2/me'

    def get_user_details(self, response):
        """Extract user details from provider response"""
        return {
            'username': response.get('login'),
            'email': response.get('email'),
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
        }