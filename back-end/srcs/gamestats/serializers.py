# from rest_framework import serializers
# from .models import Game

# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = '__all__'

from rest_framework import serializers
from .models import PongSolo
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):    
    player1 = serializers.CharField(source='player1.username', read_only=True)
    player2 = serializers.CharField(source='player2.username', read_only=True)
    winner = serializers.CharField(source='winner.username', read_only=True)
    loser = serializers.CharField(source='loser.username', read_only=True)

    class Meta:
        model = PongSolo
        fields = ['id', 'player1', 'player2', 'winner', 'loser', 'timestamp']

class GameWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongSolo
        fields = ['player1', 'player2', 'winner', 'loser']