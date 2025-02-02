from rest_framework import generics
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes  
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, LogoutSerializer

#Login User
class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])
        user.online = True
        user.save()
        return response

class Logout(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = request.user
        user.online = False
        user.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)


#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# social login

from django.shortcuts import redirect
from django.conf import settings
from social_django.models import UserSocialAuth

def login(request):
    return redirect('social:begin', backend='42')

def callback(request):
    return redirect(settings.LOGIN_REDIRECT_URL)


