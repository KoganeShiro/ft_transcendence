from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .permissions import IsAdminOrSelf
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer    
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Allow anyone to register (no authentication needed for POST)
            return [AllowAny()]
        else:
            # Only admin users can list all users (GET)
            return [IsAuthenticated()]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]