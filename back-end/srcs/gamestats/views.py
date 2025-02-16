from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PongSolo, PongMulti, TTT, PongTournament
from .serializers import PongSerializer, PongWriteSerializer, MultiSerializer, TTTSerializer, MultiWriteSerializer, TTTWriteSerializer, PongTournamentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied 
from rest_framework.decorators import action
from user_mgm.permissions import IsAPIUser

import logging

logging.basicConfig(level=logging.DEBUG)

class PongTournamentViewSet(viewsets.ModelViewSet):
    queryset = PongTournament.objects.all().order_by('-timestamp')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PongTournamentSerializer
        return PongTournamentSerializer

    def create(self, request, *args, **kwargs):
        logging.debug("create tournament")
        self.check_permissions(request)
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        logging.debug("update tournament")
        self.check_permissions(request)
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        logging.debug("partial update tournament")
        self.check_permissions(request)
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        return self.update(request, *args, **kwargs)



class PongViewSet(viewsets.ModelViewSet):
    queryset = PongSolo.objects.all().order_by('-timestamp')
    permission_classes = [IsAuthenticated]  # Apply custom permission class

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
            return PongWriteSerializer
        return PongSerializer  # Use read serializer for output

    def create(self, request, *args, **kwargs):
        logging.debug("create pong")
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        logging.debug("update pong") 
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        logging.debug("partial update pong")
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        return self.update(request, *args, **kwargs)
   
class MultiViewSet(viewsets.ModelViewSet):
    queryset = PongMulti.objects.all().order_by('-timestamp')  
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
            return MultiWriteSerializer
        return MultiSerializer  # Use read serializer for output
    
    def create(self, request, *args, **kwargs):
        logging.debug("create multi")
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        logging.debug("update multi")        
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        logging.debug("partial update multi")
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.usernamename != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        return self.update(request, *args, **kwargs)
    
class TTTViewSet(viewsets.ModelViewSet):
    queryset = TTT.objects.all().order_by('-timestamp')  
    permission_classes = [IsAuthenticated]  

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
            return TTTWriteSerializer
        return TTTSerializer  # Use read serializer for output
    
    def create(self, request, *args, **kwargs):
        logging.debug("create ttt")      
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        logging.debug("update ttt")        
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        logging.debug("partial update ttt")
        self.check_permissions(request)  # Check permissions explicitly
        if request.user.username != 'api_user':
            raise PermissionDenied("User is not authenticated or not an API user")
        return self.update(request, *args, **kwargs)

    

class LastFivePongView(viewsets.ViewSet):
    def list(self, request):
        logging.debug("last five pong")
        games = PongSolo.objects.filter(player1=request.user) | PongSolo.objects.filter(player2=request.user)
        last_five_games = games.order_by('-timestamp')[:5]
        serializer = PongSerializer(last_five_games, many=True)
        data = serializer.data
        for game in data:
            if game['player1'] == request.user.username:
                game['opponent'] = game['player2']
            if game['player2'] == request.user.username:
                game['opponent'] = game['player1']
            if game['winner'] == request.user.username:
                game['won'] = True
            else:
                game['won'] = False            
            game['my_score'] = game['player1_score'] if game['player1'] == request.user.username else game['player2_score']
            game['opponent_score'] = game['player1_score'] if game['player2'] == request.user.username else game['player2_score']
            game['my_rank'] = game['rank_player1_begin'] if game['player1'] == request.user.username else game['rank_player2_begin']
            game['opponent_rank'] = game['rank_player1_begin'] if game['player2'] == request.user.username else game['rank_player2_begin']

        return Response(data)

class LastFiveMultiView(viewsets.ViewSet):
    def list(self, request):
        logging.debug("last five multi")
        games = PongMulti.objects.filter(player1=request.user) | PongMulti.objects.filter(player2=request.user) | PongMulti.objects.filter(player3=request.user) | PongMulti.objects.filter(player4=request.user)      
        last_five_games = games.order_by('-timestamp')[:5]
        serializer = MultiSerializer(last_five_games, many=True)
        data = serializer.data
        for game in data:
            if game['player1'] == request.user.username:
                game['opponent1'] = game['player2']
                game['opponent2'] = game['player3']
                game['opponent3'] = game['player4']
                game['opponent1_score'] = game['player2_score']
                game['opponent2_score'] = game['player3_score']
                game['opponent3_score'] = game['player4_score']
                game['my_score'] = game['player1_score']
                game['my_rank'] = game['rank_player1_begin']
                game['opponent1_rank'] = game['rank_player2_begin']
                game['opponent2_rank'] = game['rank_player3_begin']
                game['opponent3_rank'] = game['rank_player4_begin']
            if game['player2'] == request.user.username:
                game['opponent1'] = game['player1']
                game['opponent2'] = game['player3']
                game['opponent3'] = game['player4']
                game['opponent1_score'] = game['player1_score']
                game['opponent2_score'] = game['player3_score']
                game['opponent3_score'] = game['player4_score']
                game['my_score'] = game['player2_score']
                game['my_rank'] = game['rank_player2_begin']
                game['opponent1_rank'] = game['rank_player1_begin']
                game['opponent2_rank'] = game['rank_player3_begin']
                game['opponent3_rank'] = game['rank_player4_begin']
            if game['player3'] == request.user.username:
                game['opponent1'] = game['player1']
                game['opponent2'] = game['player2']
                game['opponent3'] = game['player4']
                game['opponent1_score'] = game['player1_score']
                game['opponent2_score'] = game['player2_score']
                game['opponent3_score'] = game['player4_score']
                game['my_score'] = game['player3_score']
                game['my_rank'] = game['rank_player3_begin']
                game['opponent1_rank'] = game['rank_player1_begin']
                game['opponent2_rank'] = game['rank_player2_begin']
                game['opponent3_rank'] = game['rank_player4_begin']
            if game['player4'] == request.user.username:
                game['opponent1'] = game['player1']
                game['opponent2'] = game['player2']
                game['opponent3'] = game['player3']
                game['opponent1_score'] = game['player1_score']
                game['opponent2_score'] = game['player2_score']
                game['opponent3_score'] = game['player3_score']
                game['my_score'] = game['player4_score']
                game['my_rank'] = game['rank_player4_begin']
                game['opponent1_rank'] = game['rank_player1_begin']
                game['opponent2_rank'] = game['rank_player2_begin']
                game['opponent3_rank'] = game['rank_player3_begin']
            if game['winner'] == request.user.username:
                game['won'] = True
            else:
                game['won'] = False
        return Response(data)
    
class LastFiveTTTView(viewsets.ViewSet):
    def list(self, request):
        logging.debug("last five ttt")
        games = TTT.objects.filter(player1=request.user) | TTT.objects.filter(player2=request.user)
        last_five_games = games.order_by('-timestamp')[:5]
        serializer = TTTSerializer(last_five_games, many=True)
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
            game['my_turn'] = game['player1_turn'] if game['player1'] == request.user.username else game['player2_turn']
            game['opponent_turn'] = game['player1_turn'] if game['player2'] == request.user.username else game['player2_turn']
            game['my_rank'] = game['rank_player1_begin'] if game['player1'] == request.user.username else game['rank_player2_begin']
            game['opponent_rank'] = game['rank_player1_begin'] if game['player2'] == request.user.username else game['rank_player2_begin']

        return Response(data)



