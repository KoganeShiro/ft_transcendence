from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PongSolo, PongMulti, TTT, PongTournament

@admin.register(PongSolo)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'winner', 'loser', 'timestamp')

@admin.register(PongMulti)
class MultiAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'player3', 'player4', 'winner', 'timestamp')

@admin.register(TTT)
class TTTAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'winner', 'loser', 'timestamp')

@admin.register(PongTournament)
class PongTournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'semi_final_1', 'semi_final_2', 'final', 'winner', 'timestamp')





