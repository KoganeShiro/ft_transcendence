from django.db import models
from user_mgm.models import CustomUser

class Game(models.Model):
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_player2')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    loser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_lost')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Game: {self.player1.username} vs {self.player2.username}"
