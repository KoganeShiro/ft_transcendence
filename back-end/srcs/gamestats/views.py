# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Game
# from .serializers import GameSerializer

# class GameViewSet(viewsets.ModelViewSet):
#     queryset = Game.objects.all().order_by('-timestamp')  # Show latest games first
#     serializer_class = GameSerializer
#     permission_classes = [IsAuthenticated]  # Require authentication to access


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PongSolo
from .serializers import GameSerializer, GameWriteSerializer
from rest_framework.response import Response

class GameViewSet(viewsets.ModelViewSet):
    queryset = PongSolo.objects.all().order_by('-timestamp')  
    permission_classes = [IsAuthenticated]  

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
            return GameWriteSerializer
        return GameSerializer  # Use read serializer for output
    

class LastFiveGamesView(viewsets.ViewSet):
    def list(self, request):
        games = PongSolo.objects.filter(player1=request.user) | PongSolo.objects.filter(player2=request.user)
        last_five_games = games.order_by('-timestamp')[:5]
        serializer = GameSerializer(last_five_games, many=True)
        data = serializer.data
        for game in data:
            if game['player1'] == request.user.username:
                game['opponent'] = game['player2']
            if game['player2'] == request.user.username:
                game['opponent'] = game['player1']
            if game['winner'] == request.user.username:
                game['won'] = True
            if game['loser'] == request.user.username:
                game['won'] = False
            game['my_score'] = game['player1_score'] if game['player1'] == request.user.username else game['player2_score']
            game['opponent_score'] = game['player1_score'] if game['player2'] == request.user.username else game['player2_score']
            game['my_rank'] = game['rank_player1_begin'] if game['player1'] == request.user.username else game['rank_player2_begin']
            game['opponent_rank'] = game['rank_player1_begin'] if game['player2'] == request.user.username else game['rank_player2_begin']
            
        
            


        return Response(data)



