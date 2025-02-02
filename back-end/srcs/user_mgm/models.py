from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):    
    cover_photo = models.ImageField(upload_to='profile_image', blank=True)
 #   cover_photo_url = models.URLField(blank=True)
    online = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)

