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

class GameViewSet(viewsets.ModelViewSet):
    queryset = PongSolo.objects.all().order_by('-timestamp')  
    permission_classes = [IsAuthenticated]  

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
            return GameWriteSerializer
        return GameSerializer  # Use read serializer for output
    


