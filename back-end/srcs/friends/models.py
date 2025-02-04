from django.db import models
from user_mgm.models import CustomUser
# Create your models here.
# class Friendship(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
#     friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')
#     accepted = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

#     def __str__(self):
#         return f"Friendship: {self.user.username} and {self.friend.username}"

# class muted_User(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='muted_user')
#     muted = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='muted')
#     timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created    

#     def __str__(self):
#         return f"Muted: {self.user.username} muted {self.muted.username}"

# class blocked_User(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked_user')
#     blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked')
#     timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

#     def __str__(self):
#         return f"Blocked: {self.user.username} blocked {self.blocked.username}"
    
# class messages(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
#     friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

#     def __str__(self):
#         return f"Message: {self.user.username} to {self.friend.username} on {self.timestamp}"