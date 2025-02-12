from django.db import models
from user_mgm.models import CustomUser


class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')
    # accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Friendship: {self.user.username} and {self.friend.username}"

class muted_User(models.Model):
    muter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='muter')
    muted = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='muted')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created    

    def __str__(self):
        return f"Muted: {self.muter.username} muted {self.muted.username}"

class blocked_User(models.Model):
    blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocker')
    blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Blocked: {self.blocker.username} blocked {self.blocked.username}"
    
class messages(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Message: {self.sender.username} to {self.receiver.username} on {self.timestamp}"