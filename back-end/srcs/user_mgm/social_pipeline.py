from rest_framework_simplejwt.tokens import RefreshToken
from django.http import request
import logging

logger = logging.getLogger(__name__)

def generate_jwt_token(backend, user, response, request, *args, **kwargs):
    """
    Store JWT token in kwargs so it can be accessed later.
    """
    refresh = RefreshToken.for_user(user)
    
    tokens = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
        # 'user': {
        #     'id': user.id,
        #     'email': user.email,
        #     'username': user.username
        # }
    }

    request.session["jwt_tokens"] = tokens
    request.session.modified = True 

    # logger.info(f"JWT Tokens: {kwargs['jwt_tokens']}")

    

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.response import Response



# def generate_jwt_token(backend, user, response, *args, **kwargs):
#     """
#     Generate JWT token after successful social authentication.
#     """
#     print("generate_jwt_token")
#     refresh = RefreshToken.for_user(user)


#     tokens = {
#         'access': str(refresh.access_token),
#         'refresh': str(refresh),
#             'user': { 'username' : user.username,
#                       'email' : user.email
#             }                     
#     }
#     return tokens


import requests
from django.core.files.base import ContentFile

# def save_avatar(backend, user, response, *args, **kwargs):
#     """
#     Downloads and saves the user's avatar from the social provider.
#     """
#     if backend.name == 'facebook':
#         avatar_url = f"http://graph.facebook.com/{response['id']}/picture?type=large"
#     elif backend.name == 'google-oauth2':
#         avatar_url = response['picture']
#     elif backend.name == 'github':
#         avatar_url = response['avatar_url']
#     else:
#         avatar_url = None

#     if avatar_url:
#         try:
#             avatar_response = requests.get(avatar_url)
#             avatar_response.raise_for_status()
#             user.cover_photo.save(
#                 f"{user.username}_avatar.jpg",
#                 ContentFile(avatar_response.content),
#                 save=True
#             )
#         except requests.RequestException:
#             # Handle exceptions, e.g., log the error or set a default image
#             pass
