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


# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.contrib.auth import logout
# from datetime import timedelta
# from rest_framework.renderers import JSONRenderer

# def generate_jwt_token(backend, user, response, request, *args, **kwargs):
#     """
#     Store JWT tokens in HttpOnly cookies so they can be accessed securely later.
#     """
#     refresh = RefreshToken.for_user(user)
    
#     response = Response()

#         # Set the renderer
#     response.accepted_renderer = JSONRenderer()
#     response.accepted_media_type = 'application/json'
#     response.renderer_context = {}
    
#     access_token = str(refresh.access_token)
#     refresh_token = str(refresh)

#     # Store the tokens in HttpOnly cookies (secure and cannot be accessed by JavaScript)
#     response.set_cookie(
#         'access_token',
#         access_token,
#         httponly=True,
#         secure=True,  # Use this in production (requires HTTPS)
#         max_age=timedelta(days=1),  # Set cookie expiry
#         samesite='Lax'  # Adjust as necessary
#     )
#     response.set_cookie(
#         'refresh_token',
#         refresh_token,
#         httponly=True,
#         secure=True,
#         max_age=timedelta(days=7),  # Refresh token can be stored for longer
#         samesite='Lax'
#     )

#     return response










import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse




def save_avatar(backend, user, response, *args, **kwargs):
    """
    Fetch the user's avatar from the 42 API and save it to the cover_photo field.
    """
    if backend.name != "42":  # Ensure it's from the 42 authentication
        return

    # Extract the avatar URL from the response
    avatar_url = response.get("image", {}).get("link")

    if avatar_url:
        try:
            # Download the avatar image
            avatar_response = requests.get(avatar_url)

            if avatar_response.status_code == 200:
                # Extract filename from URL
                filename = urlparse(avatar_url).path.split("/")[-1]

                # Save the image to cover_photo
                if not user.cover_photo:
                    user.cover_photo.save(filename, ContentFile(avatar_response.content), save=True)
                user.is_42 = True
                user.save()
                print(f"✅ Cover photo updated for {user.username}")
        except Exception as e:
            print(f"⚠️ Failed to update cover photo: {e}")



# def clear_session_before_redirect(strategy, backend, request=None, *args, **kwargs):
#     """Clears the session before redirecting to the OAuth provider."""
#     print('clear_session_before_redirect')
#     if request and request.session.session_key:
#         request.session.flush()


