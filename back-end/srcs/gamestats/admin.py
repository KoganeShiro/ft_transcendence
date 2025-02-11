from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PongSolo

@admin.register(PongSolo)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'winner', 'loser', 'timestamp')
