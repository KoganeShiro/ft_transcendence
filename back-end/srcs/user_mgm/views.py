from rest_framework import generics
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes  
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, LogoutSerializer, ProfileUpdateSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone


#Login User
class Login(TokenObtainPairView):    
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])        
        user.save()
        return response

class Logout(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
     #   user = request.user        
     #   user.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)


#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# #api/profile  and api/profile/update
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getProfile(request):
#     user = request.user
#     serializer = ProfileSerializer(user, many=False)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request, lookup_value=None):
    """
    Fetch user profile using either user ID or username.
    """
    if lookup_value is None:  # Default to the current user if no lookup is provided
        user = request.user
    else:
        user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username

    serializer = ProfileSerializer(user, many=False)
    isOnline = user.last_seen > timezone.now() - timezone.timedelta(minutes=5)
    preparedData = {
        'username': serializer.data['username'],
        'cover_photo': serializer.data['cover_photo'],
        'online': isOnline,
        'last_seen': serializer.data['last_seen'],
        'is_active': serializer.data['is_active'],
    }
    return Response(preparedData)




# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateProfile(request):
#     user = request.user
#     serializer = ProfileSerializer(user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user    
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# @api_view(['PUT', 'PATCH'])
# @permission_classes([IsAuthenticated])
# def updateProfile(request, lookup_value=None):
#     """
#     Update user profile using either user ID or username.
#     """
#     # If no lookup value is provided, default to the current logged-in user
#     if lookup_value is None:
#         user = request.user
#     else:
#         user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username

#     serializer = ProfileSerializer(user, data=request.data, partial=True)  # Allow partial updates
#     if serializer.is_valid():
#         serializer.save()  # Save the updated profile data
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser  # Ensure you're using your custom user model
from .serializers import UserSerializer  # Your custom serializer for users

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated to access this data
def get_all_users(request):
    """
    Get all users from the CustomUser model and return their serialized data.
    """
    users = CustomUser.objects.all()  # Get all users from CustomUser
    serializer = UserSerializer(users, many=True)  # Serialize the queryset    
    return Response(serializer.data)  # Return the serialized data as the response


from django.shortcuts import redirect
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def social_auth_complete(request):
    
    """
    Retrieve the JWT tokens stored in the pipeline and return as JSON.
    """
    jwt_tokens = request.session.get('jwt_tokens')

    if jwt_tokens:
        return Response(jwt_tokens)
    
    return Response({'error': 'Authentication failed'}, status=400)



