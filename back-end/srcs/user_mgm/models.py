from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any custom fields here, e.g., for a Pong game
    rank = models.IntegerField(default=0)  # User ranking in the game
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)