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
                user.cover_photo.save(filename, ContentFile(avatar_response.content), save=True)
                print(f"✅ Cover photo updated for {user.username}")
        except Exception as e:
            print(f"⚠️ Failed to update cover photo: {e}")



# import requests
# from django.core.files.base import ContentFile

# def save_avatar(backend, user, response, *args, **kwargs):
#     """
#     Downloads and saves the user's avatar from the social provider.
#     """
    

#     avatar_url = 

    
#     if avatar_url:
#         try:
#             avatar_response = requests.get(avatar_url)
#             avatar_response.raise_for_status()
#             print(avatar_response.content)
#             user.cover_photo.save(
#                 f"{user.username}_avatar.jpg",
#                 ContentFile(avatar_response.content),
#                 save=True
#             )
#         except requests.RequestException:
#             user.cover_photo = None           
#             pass
