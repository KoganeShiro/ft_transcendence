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
from django.contrib.auth import logout


#Login User
class Login(TokenObtainPairView):    
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])        
        user.save()
        tokens = response.data
        response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="Lax")
        response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")
        response.data = {
            'username': user.username,
            'email': user.email,
            'id': user.id
        }

        logout(request)  # This removes the session ID cookie
        response.delete_cookie('sessionid') # This deletes the session ID cookie
 

        return response
    


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

@api_view(['POST', 'GET'])
def refresh_tokens(request):
    # Get the refresh token from the cookies
    refresh_token = request.COOKIES.get('refresh_token')
    
    if not refresh_token:
        return Response({'message': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create RefreshToken object
        refresh_token = RefreshToken(refresh_token)
        
        # Get the user ID from the refresh token payload
        user_id = refresh_token.payload.get('user_id')
        
        if not user_id:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the user from the database
        user = User.objects.get(id=user_id)

        # Generate new access token
        access_token = str(refresh_token.access_token)
        
        # Generate new refresh token (rotating refresh token)
        new_refresh_token = RefreshToken.for_user(user)

        # Prepare the response
        response = Response({'message': 'Tokens refreshed successfully'})

        # Set the new access token as HttpOnly cookie
        response.set_cookie(
            'access_token', 
            access_token,
            httponly=True, 
            secure=True,  # Ensure HTTPS in production
            samesite='Lax', 
            max_age=timedelta(hours=1)  # 1-hour expiration
        )

        # Set the new refresh token as HttpOnly cookie
        response.set_cookie(
            'refresh_token', 
            str(new_refresh_token),
            httponly=True, 
            secure=True,  # Ensure HTTPS in production
            samesite='Lax', 
            max_age=timedelta(days=7)  # 7-day expiration
        )
        
        return response
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)







    
from rest_framework_simplejwt.tokens import RefreshToken

class Logout(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

     #   user = request.user        
     #   user.save()        
        return response
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not access_token or not refresh_token:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # Blacklist the refresh token
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except Exception as e:
            self.fail('bad_token')
        
        response = Response({'message': 'Logged out successfully'})
        
        # Delete the access and refresh token cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response

from social_django.models import UserSocialAuth


class deleteAccount(APIView):    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not access_token or not refresh_token:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # Blacklist the refresh token
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
        except Exception as e:
            self.fail('bad_token')
        
        user.username = 'anonymous' + str(user.id)
        user.email = 'anonymous' + str(user.id) + '@transcendence.com'
        user.is_active = False
        user.cover_photo.delete()
        user.cover_photo = None
        user.set_unusable_password()
        if user.is_42:
            user.is_42 = False
            UserSocialAuth.objects.filter(user_id=user.id).delete()      

        user.save()

        response = Response({'message': 'Account anonimized successfully'})        
        # Delete the access and refresh token cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response







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
        'id': serializer.data['id'],
        'username': serializer.data['username'],
        'cover_photo': serializer.data['cover_photo'],
        'online': isOnline,
        'last_seen': serializer.data['last_seen'],
        'is_active': serializer.data['is_active'],
        'is_42': serializer.data['is_42'],
    }
    return Response(preparedData)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStats(request, lookup_value=None):
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

'stats': {
        "Pong": {
          'currentRank': serializer.data['stat_pong_solo_rank'],
          'totalMatches': serializer.data['stat_pong_solo_wins_tot'] + serializer.data['stat_pong_solo_loss_tot'],
          'tournamentWins': serializer.data['stat_pong_solo_tournament_wins'],
          'wins': serializer.data['stat_pong_solo_wins_tot'],
          'losses': serializer.data['stat_pong_solo_loss_tot'],
          'rankProgression': serializer.data['stat_pong_solo_progress'],
          'pointsWonUnder5Exchanges': serializer.data['stat_pong_solo_wins_tot_min5'],
          'pointsWonUnder10Exchanges': serializer.data['stat_pong_solo_wins_tot_min10'],
          'pointsWonOver10Exchanges': serializer.data['stat_pong_solo_wins_tot_max10'],
          'pointsLostUnder5Exchanges': serializer.data['stat_pong_solo_loss_tot_min5'],
          'pointsLostUnder10Exchanges': serializer.data['stat_pong_solo_loss_tot_min10'],
          'pointsLostOver10Exchanges': serializer.data['stat_pong_solo_loss_tot_max10']
        },
        "4 Players Pong": {
          'currentRank': serializer.data['stat_pong_multi_rank'],
          'totalMatches': serializer.data['stat_pong_multi_wins_tot'] + serializer.data['stat_pong_multi_loss_tot'],
          'wins': serializer.data['stat_pong_multi_wins_tot'],
          'losses': serializer.data['stat_pong_multi_loss_tot'],
          'rankProgression': serializer.data['stat_pong_multi_progress'],
          'pointsWonUnder5Exchanges': serializer.data['stat_pong_multi_wins_tot_min5'],
          'pointsWonUnder10Exchanges': serializer.data['stat_pong_multi_wins_tot_min10'],
          'pointsWonOver10Exchanges': serializer.data['stat_pong_multi_wins_tot_max10'],
          'pointsLostUnder5Exchanges': serializer.data['stat_pong_multi_loss_tot_min5'],
          'pointsLostUnder10Exchanges': serializer.data['stat_pong_multi_loss_tot_min10'],
          'pointsLostOver10Exchanges': serializer.data['stat_pong_multi_loss_tot_max10']
        },
        "Tic Tac Toe": {
          'currentRank': serializer.data['stat_ttt_rank'],
          'totalMatches': serializer.data['stat_ttt_wins_tot'] + serializer.data['stat_ttt_loss_tot'],          
          'wins': serializer.data['stat_ttt_wins_tot'],
          'losses': serializer.data['stat_ttt_loss_tot'],
          'rankProgression': serializer.data['stat_ttt_progress'],
          'averageMovesPerWin': serializer.data['stat_ttt_wins_av_movm'],
          'averageMovesPerLoss': serializer.data['stat_ttt_loss_av_movm']                                                          
        }
      }


    }
    return Response(preparedData)

from .serializers import StatsUpdateSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateStats(request, lookup_value):
    """
    Fetch user profile using either user ID or username.
    """
    #if request.user == None:
    if request.user.name == 'api_user':
    #if request.user == None or request.user.username == lookup_value:
        user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username
    else:
        return Response({'error': 'You are not allowed to update other users stats'}, status=400)

    serializer = StatsUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():        
        serializer.save()        
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


from .serializers import StatsIncrementSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def incrementStats(request, lookup_value):
    """
    Fetch user profile using either user ID or username.
    """
    #if request.user == None:
    if request.user.name == 'api_user':
    #if request.user == None or request.user.username == lookup_value:
        user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username
    else:
        return Response({'error': 'You are not allowed to increment users stats'}, status=400)
    
    data = request.data.copy()
        # Ensure stat_pong_solo_progress is a list
    if 'stat_pong_solo_progress' in data and isinstance(data['stat_pong_solo_progress'], int):
        data['stat_pong_solo_progress'] = [data['stat_pong_solo_progress']]

    # Ensure stat_pong_multi_progress is a list
    if 'stat_pong_multi_progress' in data and isinstance(data['stat_pong_multi_progress'], int):
        data['stat_pong_multi_progress'] = [data['stat_pong_multi_progress']]

    # Ensure stat_ttt_progress is a list
    if 'stat_ttt_progress' in data and isinstance(data['stat_ttt_progress'], int):
        data['stat_ttt_progress'] = [data['stat_ttt_progress']]

    serializer = StatsIncrementSerializer(user, data=data, partial=True)
    if serializer.is_valid():        
        serializer.save()        
        return Response(serializer.data)
    return Response(serializer.errors, status=400)












import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_solo_progress(request, lookup_value):
    try:
        #if request.user == None:
        if request.user.name == 'api_user':
        #if request.user == None or request.user.username == lookup_value:
            user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username
        else:
            return Response({'error': 'You are not allowed to update other users stats'}, status=400)               
        
        logger.debug('Updating progress for user %s', user.username)

        # Parse JSON data from request
        data = json.loads(request.body)
        new_values = data.get("progress", [])
        
        # Validate that new_values is a list of integers
        if not isinstance(new_values, list) or not all(isinstance(i, int) for i in new_values):
            return Response({"error": "progress must be a list of integers"}, status=400)

        # Append new values to the existing array
        user.stat_pong_solo_progress.extend(new_values)
        user.save()

        return Response({"message": "Progress updated", "updated_progress": user.stat_pong_solo_progress}, status=200)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)



import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_multi_progress(request, lookup_value):
    try:
        #if request.user == None:
        if request.user.name == 'api_user':
        #if request.user == None or request.user.username == lookup_value:
            user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username
        else:
            return Response({'error': 'You are not allowed to update other users stats'}, status=400)               
        
        logger.debug('Updating progress for user %s', user.username)

        # Parse JSON data from request
        data = json.loads(request.body)
        new_values = data.get("progress", [])
        
        # Validate that new_values is a list of integers
        if not isinstance(new_values, list) or not all(isinstance(i, int) for i in new_values):
            return Response({"error": "progress must be a list of integers"}, status=400)

        # Append new values to the existing array
        user.stat_pong_multi_progress.extend(new_values)
        user.save()

        return Response({"message": "Progress updated", "updated_progress": user.stat_pong_multi_progress}, status=200)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)




import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_ttt_progress(request, lookup_value):
    try:
        #if request.user == None:
        if request.user.name == 'api_user':
        #if request.user == None or request.user.username == lookup_value:
            user = get_object_or_404(CustomUser, username=lookup_value)  # Lookup by username
        else:
            return Response({'error': 'You are not allowed to update other users stats'}, status=400)               
        
        logger.debug('Updating progress for user %s', user.username)

        # Parse JSON data from request
        data = json.loads(request.body)
        new_values = data.get("progress", [])
        
        # Validate that new_values is a list of integers
        if not isinstance(new_values, list) or not all(isinstance(i, int) for i in new_values):
            return Response({"error": "progress must be a list of integers"}, status=400)

        # Append new values to the existing array
        user.stat_ttt_progress.extend(new_values)
        user.save()

        return Response({"message": "Progress updated", "updated_progress": user.stat_ttt_progress}, status=200)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)



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
        if 'cover_photo' in serializer.validated_data:
            user.cover_photo.delete()  # Delete the old cover photo
        serializer.save()
        response = Response()
        data = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
        }
        return Response(data)
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
from django.contrib.auth import logout
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view



@api_view(['GET'])
@permission_classes([AllowAny])  # This endpoint should also be public
def social_auth_complete(request):
    
    """
    Retrieve the JWT tokens stored in the pipeline and return as JSON.
    """
    jwt_tokens = request.session.get('jwt_tokens')

    if jwt_tokens:
        logout(request)  # This removes the session ID cookie
        # response = Response(jwt_tokens)        
        response = redirect("/profile")  # Redirect URL
        response.delete_cookie('sessionid') # This deletes the session ID cookie

        response.set_cookie("access_token", jwt_tokens["access"], httponly=True, secure=True, samesite="Lax")
        response.set_cookie("refresh_token", jwt_tokens["refresh"], httponly=True, secure=True, samesite="Lax")



        return response
    
    return Response({'error': 'Authentication failed'}, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from logging import getLogger

logger = getLogger(__name__)


@permission_classes([AllowAny])  # Make sure this is accessible to all users
@api_view(['GET'])
def social_auth_login(request):
    logout(request)  # This removes the session ID cookie
    logger.info('Logging out user before social auth')
    return redirect('social:begin', '42')


