from django.db import models
from user_mgm.models import CustomUser

class PongSolo(models.Model):
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games_as_player2')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    loser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_lost')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    rank_player1_begin = models.IntegerField(default=0)  # Player1's rank
    rank_player2_begin = models.IntegerField(default=0)  # Player2's rank
    rank_player1_change = models.IntegerField(default=0)  # Player1's rank
    rank_player2_change = models.IntegerField(default=0)  # Player2's rank
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set defaults for new instances
            self.rank_player1_begin = self.player1.stat_pong_solo_rank
            self.rank_player2_begin = self.player2.stat_pong_solo_rank
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game: {self.player1.username} vs {self.player2.username}"
