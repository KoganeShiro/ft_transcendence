from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):    
    cover_photo = models.ImageField(upload_to='covers/', default='covers/default.jpg')
    online = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)

