from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin panel
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('cover_photo', 'stat_pong_solo_rank', 'stat_pong_solo_progress', 'stat_pong_solo_wins_tot', 'stat_pong_solo_loss_tot', 'stat_pong_solo_tournament_wins', 'stat_pong_solo_tournament_tot_nb_matches', 'stat_pong_solo_loss', 'stat_pong_solo_wins_tot_min5', 'stat_pong_solo_loss_tot_min5', 'stat_pong_solo_wins_tot_min10', 'stat_pong_solo_loss_tot_min10', 'stat_pong_solo_wins_tot_max10', 'stat_pong_solo_loss_tot_max10')}),
    )