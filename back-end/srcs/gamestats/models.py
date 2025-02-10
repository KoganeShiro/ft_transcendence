from django.db import models
from user_mgm.models import CustomUser

class PongSolo(models.Model):
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='soloplayer1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='soloplayer2')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='solowinner')
    loser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='sololoser')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    rank_player1_begin = models.IntegerField(default=0)  # Player1's rank
    rank_player2_begin = models.IntegerField(default=0)  # Player2's rank
    rank_player1_change = models.IntegerField(default=0)  # Player1's rank
    rank_player2_change = models.IntegerField(default=0)  # Player2's rank
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    type = models.CharField(max_length=50, default='solo')


    def save(self, *args, **kwargs):
        if not self.pk:  # Only set defaults for new instances
            self.rank_player1_begin = self.player1.stat_pong_solo_rank
            self.rank_player2_begin = self.player2.stat_pong_solo_rank
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pong: {self.player1.username} vs {self.player2.username}"
    
class PongTournament(models.Model):
    semi_final_1 = models.ForeignKey(PongSolo, on_delete=models.CASCADE, related_name='semi_final_1')
    semi_final_2 = models.ForeignKey(PongSolo, on_delete=models.CASCADE, related_name='semi_final_2')
    final = models.ForeignKey(PongSolo, on_delete=models.CASCADE, related_name='final')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Tournament: {self.semi_final_1.player1.username} vs {self.semi_final_1.player2.username} vs {self.semi_final_2.player1.username} vs {self.semi_final_2.player2.username} vs {self.final.player1.username} vs {self.final.player2.username}"


class PongMulti(models.Model):
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='multiplayer1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='multiplayer2')
    player3 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='multiplayer3')
    player4 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='multiplayer4')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='multiwinner')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    player3_score = models.IntegerField(default=0)
    player4_score = models.IntegerField(default=0)
    rank_player1_begin = models.IntegerField(default=0)  # Player1's rank
    rank_player2_begin = models.IntegerField(default=0)  # Player2's rank
    rank_player3_begin = models.IntegerField(default=0)  # Player3's rank
    rank_player4_begin = models.IntegerField(default=0)  # Player4's rank
    rank_player1_change = models.IntegerField(default=0)  # Player1's rank
    rank_player2_change = models.IntegerField(default=0)  # Player2's rank
    rank_player3_change = models.IntegerField(default=0)  # Player3's rank
    rank_player4_change = models.IntegerField(default=0)  # Player4's rank
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    type = models.CharField(max_length=50, default='multi')

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set defaults for new instances
            self.rank_player1_begin = self.player1.stat_pong_multi_rank
            self.rank_player2_begin = self.player2.stat_pong_multi_rank
            self.rank_player3_begin = self.player3.stat_pong_multi_rank
            self.rank_player4_begin = self.player4.stat_pong_multi_rank
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Multi-Pong: {self.player1.username} vs {self.player2.username} vs {self.player3.username} vs {self.player4.username}"

class TTT(models.Model):
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tttplayer1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tttplayer2')
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tttwinner')
    loser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tttloser')
    player1_turn = models.IntegerField(default=0)
    player2_turn = models.IntegerField(default=0)
    rank_player1_begin = models.IntegerField(default=0)  # Player1's rank
    rank_player2_begin = models.IntegerField(default=0)  # Player2's rank
    rank_player1_change = models.IntegerField(default=0)  # Player1's rank
    rank_player2_change = models.IntegerField(default=0)  # Player2's rank
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set defaults for new instances
            self.rank_player1_begin = self.player1.stat_ttt_rank
            self.rank_player2_begin = self.player2.stat_ttt_rank
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TTT: {self.player1.username} vs {self.player2.username}"



