from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.CharField(default = '', max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)

