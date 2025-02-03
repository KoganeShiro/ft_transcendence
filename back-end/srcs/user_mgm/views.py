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

#from django.shortcuts import redirect
#from django.conf import settings
#from social_django.models import UserSocialAuth

#def login(request):
#    return redirect('social:begin', backend='42')

#def callback(request):
#    return redirect(settings.LOGIN_REDIRECT_URL)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from social_django.utils import psa
import logging

logger = logging.getLogger(__name__)

class OAuth2Login(APIView):
    def get(self, request, *args, **kwargs):
        logging.debug('OAuth2Login: Request received')
        return redirect('social:begin', backend='42')

class OAuth2Complete(APIView):

    @psa('social:complete')
    def get(self, request, backend):
        logging.debug('OAuth2Complete: Request received')
        print ("OAuth2Complete: Request received")
        
        user = request.backend.do_auth(request.GET.get('code'))
        if user:
            logging.debug('OAuth2Complete: Authentication successful')
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            logging.debug('OAuth2Complete: Authentication failed')
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
