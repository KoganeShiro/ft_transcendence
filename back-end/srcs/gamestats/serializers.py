# from rest_framework import serializers
# from .models import Game

# class GameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Game
#         fields = '__all__'

from rest_framework import serializers
from .models import PongSolo, PongMulti, TTT, PongTournament
from django.contrib.auth.models import User
from user_mgm.models import CustomUser

class PongTournamentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = PongTournament
        fields = '__all__'


class PongSerializer(serializers.ModelSerializer):    
    player1 = serializers.CharField(source='player1.username', read_only=True)
    player2 = serializers.CharField(source='player2.username', read_only=True)
    winner = serializers.CharField(source='winner.username', read_only=True)
    loser = serializers.CharField(source='loser.username', read_only=True)

    class Meta:
        model = PongSolo
        fields = '__all__'


# class PongWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PongSolo
#         fields = '__all__'


class PongWriteSerializer(serializers.ModelSerializer):
    # accepts usernames instead of user ids
    # player1 = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    # player2 = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    # winner = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    # loser = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')

    class Meta:
        model = PongSolo
        fields = '__all__'






       

class MultiWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongMulti
        fields = '__all__'
 
# class TTTWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TTT
#         fields = '__all__'


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

class TTTWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTT
        fields = '__all__'

