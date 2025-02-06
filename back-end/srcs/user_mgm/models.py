from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):   
   username = models.CharField(max_length=150, unique=True)    
   email = models.EmailField(blank=True)
   cover_photo = models.ImageField(upload_to='profile_image', blank=True)
   last_seen = models.DateTimeField(auto_now_add=True)
   stat_pong_solo_rank = models.IntegerField(default=0)
   stat_pong_solo_progress = ArrayField(models.IntegerField(), default=list)
   stat_pong_solo_wins_tot = models.IntegerField(default=0)
   stat_pong_solo_loss_tot = models.IntegerField(default=0)
   stat_pong_solo_tournament_wins = models.IntegerField(default=0)
   stat_pong_solo_tournament_tot_nb_matches = models.IntegerField(default=0)
   stat_pong_solo_loss = models.IntegerField(default=0)
   stat_pong_solo_wins_tot_min5 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_min5 = models.IntegerField(default=0)
   stat_pong_solo_wins_tot_min10 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_min10 = models.IntegerField(default=0)
   stat_pong_solo_wins_tot_max10 = models.IntegerField(default=0)
   stat_pong_solo_loss_tot_max10 = models.IntegerField(default=0)
