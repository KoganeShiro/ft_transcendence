from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):   
   username = models.CharField(max_length=150, unique=True)
   email = models.EmailField(blank=True)
   cover_photo = models.ImageField(upload_to='profile_image', blank=True)
   last_seen = models.DateTimeField(auto_now_add=True)
   theme = models.CharField(max_length=10, default='dark')
   lang = models.CharField(max_length=5, default='en')
   stat_pong_solo_rank = models.IntegerField(default=0)
   stat_pong_solo_progress = ArrayField(models.IntegerField(), default=list)
   stat_pong_solo_wins_tot = models.IntegerField(default=0)
   stat_pong_solo_loss_tot = models.IntegerField(default=0)
   stat_pong_solo_tournament_wins = models.IntegerField(default=0)
   stat_pong_solo_tournament_loss = models.IntegerField(default=0)   
   stat_pong_solo_wins_tot_min5 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_min5 = models.IntegerField(default=0)
   stat_pong_solo_wins_tot_min10 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_min10 = models.IntegerField(default=0)
   stat_pong_solo_wins_tot_max10 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_max10 = models.IntegerField(default=0)

   stat_pong_multi_rank = models.IntegerField(default=0)
   stat_pong_multi_progress = ArrayField(models.IntegerField(), default=list)
   stat_pong_multi_wins_tot = models.IntegerField(default=0)
   stat_pong_multi_loss_tot = models.IntegerField(default=0)
   stat_pong_multi_wins_tot_min5 = models.IntegerField(default=0)
   stat_pong_multi_loss_tot_min5 = models.IntegerField(default=0)
   stat_pong_multi_wins_tot_min10 = models.IntegerField(default=0)
   stat_pong_multi_loss_tot_min10 = models.IntegerField(default=0)
   stat_pong_multi_wins_tot_max10 = models.IntegerField(default=0)
   stat_pong_multi_loss_tot_max10 = models.IntegerField(default=0)

   stat_ttt_rank = models.IntegerField(default=0)
   stat_ttt_progress = ArrayField(models.IntegerField(), default=list)
   stat_ttt_wins_tot = models.IntegerField(default=0)
   stat_ttt_loss_tot = models.IntegerField(default=0)
   stat_ttt_wins_av_movm = models.IntegerField(default=0)
   stat_ttt_loss_av_movm = models.IntegerField(default=0)

