# from rest_framework import serializers
# from .models import Game

# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = '__all__'

from rest_framework import serializers
from .models import PongSolo, PongMulti, TTT
from django.contrib.auth.models import User

class PongSerializer(serializers.ModelSerializer):    
    player1 = serializers.CharField(source='player1.username', read_only=True)
    player2 = serializers.CharField(source='player2.username', read_only=True)
    winner = serializers.CharField(source='winner.username', read_only=True)
    loser = serializers.CharField(source='loser.username', read_only=True)

    class Meta:
        model = PongSolo
        fields = '__all__'

class PongWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongSolo
        fields = '__all__'

class MultiWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongMulti
        fields = '__all__'
 
class TTTWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTT
        fields = '__all__'


class MultiSerializer(serializers.ModelSerializer):
    player1 = serializers.CharField(source='player1.username', read_only=True)
    player2 = serializers.CharField(source='player2.username', read_only=True)
    player3 = serializers.CharField(source='player3.username', read_only=True)
    player4 = serializers.CharField(source='player4.username', read_only=True)    
    winner = serializers.CharField(source='winner.username', read_only=True)    

    class Meta:
        model = PongMulti
        fields = '__all__'


class TTTSerializer(serializers.ModelSerializer):    
    player1 = serializers.CharField(source='player1.username', read_only=True)
    player2 = serializers.CharField(source='player2.username', read_only=True)
    winner = serializers.CharField(source='winner.username', read_only=True)
    loser = serializers.CharField(source='loser.username', read_only=True)

    class Meta:
        model = TTT
        fields = '__all__'


