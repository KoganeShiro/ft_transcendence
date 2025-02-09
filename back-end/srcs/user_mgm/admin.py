from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add custom fields to the admin panel
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Additional Info', {'fields': ('cover_photo', 'stat_pong_solo_rank', 'stat_pong_solo_progress', 'stat_pong_solo_wins_tot', 'stat_pong_solo_loss_tot', 'stat_pong_solo_tournament_wins', 'stat_pong_solo_tournament_tot_nb_matches', 'stat_pong_solo_wins_tot_min5', 'stat_pong_solo_loss_tot_min5', 'stat_pong_solo_wins_tot_min10', 'stat_pong_solo_loss_tot_min10', 'stat_pong_solo_wins_tot_max10', 'stat_pong_solo_loss_tot_max10')}),
    # )


    fieldsets = UserAdmin.fieldsets + (
         ('Additional Info', {'fields': ('cover_photo', 'stat_pong_solo_rank', 'stat_pong_solo_progress', 'stat_pong_solo_wins_tot', 'stat_pong_solo_loss_tot', 'stat_pong_solo_tournament_wins', 'stat_pong_solo_tournament_loss', 'stat_pong_solo_wins_tot_min5', 'stat_pong_solo_loss_tot_min5', 'stat_pong_solo_wins_tot_min10', 'stat_pong_solo_loss_tot_min10', 'stat_pong_solo_wins_tot_max10', 'stat_pong_solo_loss_tot_max10', 'stat_pong_multi_rank', 'stat_pong_multi_progress', 'stat_pong_multi_wins_tot', 'stat_pong_multi_loss_tot', 'stat_pong_multi_wins_tot_min5', 'stat_pong_multi_loss_tot_min5', 'stat_pong_multi_wins_tot_min10', 'stat_pong_multi_loss_tot_min10', 'stat_pong_multi_wins_tot_max10', 'stat_pong_multi_loss_tot_max10', 'stat_ttt_rank', 'stat_ttt_progress', 'stat_ttt_wins_tot', 'stat_ttt_loss_tot', 'stat_ttt_wins_av_movm', 'stat_ttt_loss_av_movm')}),
        )

    list_display = ('username', 'email', 'last_seen')
    readonly_fields = ('last_seen',)