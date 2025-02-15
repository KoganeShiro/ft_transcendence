from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

import pyotp


class CustomUser(AbstractUser):   
   username = models.CharField(max_length=150, unique=True)
   email = models.EmailField(blank=True)
   is_42 = models.BooleanField(default=False)
   cover_photo = models.ImageField(upload_to='profile_image', blank=True)
   last_seen = models.DateTimeField(auto_now_add=True)
   theme = models.CharField(max_length=10, default='dark')
   lang = models.CharField(max_length=5, default='en')

   mfasecret = models.CharField(max_length=100, blank=True)   
   mfa_enabled = models.BooleanField(default=False)
   mfa_verified = models.BooleanField(default=False)

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

   def generate_otp_secret(self):
        """Generate a new OTP secret key."""
        self.mfasecret = pyotp.random_base32()
        self.save()
    
   def get_totp_instance(self):
        """Return a TOTP instance based on the secret key."""
        return pyotp.TOTP(self.mfasecret)

