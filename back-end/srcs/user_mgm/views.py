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
from django.http import HttpResponse
from io import BytesIO
import qrcode

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def setup_2fa(request):
	logger.debug('Setting up 2FA for user %s', request.user.username)
	"""Setup 2FA for the user by generating a QR code."""
	user = request.user

	if user.mfa_enabled:
		return Response({'error': '2FA is already enabled'}, status=400)

	if not user.enc_mfa_secret:
		user.generate_otp_secret()  # Generate a secret key if not set
	
#	if user.mfa_enabled:
#		return Response({'error': '2FA is already enabled'}, status=400)	

	totp = user.get_totp_instance()
	qr_uri = totp.provisioning_uri(name=user.username, issuer_name="Transcendence")

	# Generate QR code
	qr = qrcode.make(qr_uri)
	buffer = BytesIO()
	qr.save(buffer)
	buffer.seek(0)
	user.save()

	return HttpResponse(buffer.getvalue(), content_type="image/png")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enable_2fa(request):
	logger.debug('Enabling 2FA for user %s', request.user.username)
	"""Activate 2FA for the user."""
	user = request.user
	otp = request.data.get("otp")
	if user.get_totp_instance().verify(otp):
		user.mfa_enabled = True
		user.save()
		return Response({"message": "2FA enabled successfully"})
	else:
		return Response({'error': 'Invalid OTP'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_2fa(request):
	logger.debug('Disabling 2FA for user %s', request.user.username)
	"""Deactivate 2FA for the user."""
	user = request.user
	otp = request.data.get("otp")
	if user.get_totp_instance().verify(otp):
		user.mfa_enabled = False
		user.enc_mfa_secret = None
		user.save()
		return Response({"message": "2FA disabled successfully"})    	
	return Response({"message": "Invalid OTP"}, status=400)


#Login User
class Login(TokenObtainPairView):    
	serializer_class = MyTokenObtainPairSerializer
	
	def post(self, request, *args, **kwargs):
		logger.debug('Logging in user %s', request.data['username'])
		otp = request.data.get("otp")
		response = super().post(request, *args, **kwargs)
		user = CustomUser.objects.get(username=request.data['username'])        
		tokens = response.data
		response.set_cookie("access_token", tokens["access"], httponly=True, secure=True, samesite="None")        
		response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True, samesite="None")
		if user.mfa_enabled:
			if user.get_totp_instance().verify(otp):
				logout(request)  # This removes the session ID cookie
				response.delete_cookie('sessionid') # This deletes the session ID cookie
				response.data = {
					'username': user.username,
					'email': user.email,
					'id': user.id,
					'is_42': user.is_42,
					'theme': user.theme,
					'lang': user.lang
					}
				
				return response
			else:
				negresponse = Response({'error': 'Invalid OTP'}, status=400)
				logout(request)  # This removes the session ID cookie
				negresponse.delete_cookie('sessionid') # This deletes the session ID cookie
				return negresponse
		else:
			response.data = {
				'username': user.username,
				'email': user.email,
				'id': user.id,
				'is_42': user.is_42,
				'theme': user.theme,
				'lang': user.lang
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
	logger.debug('Refreshing tokens')
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
			samesite='None', 
			max_age=timedelta(hours=12)  # 1-hour expiration
		)

		# Set the new refresh token as HttpOnly cookie
		response.set_cookie(
			'refresh_token', 
			str(new_refresh_token),
			httponly=True, 
			secure=True,  # Ensure HTTPS in production
			samesite='None', 
			max_age=timedelta(days=10)  # 7-day expiration
		)
		
		return response
	except User.DoesNotExist:
		return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)


	
from rest_framework_simplejwt.tokens import RefreshToken

class Logout(APIView):
	def post(self, request):
		logger.debug('Logging out user (post)')
		serializer = LogoutSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		response = Response()
		response.delete_cookie('access_token')
		response.delete_cookie('refresh_token')  
		return response
	
	@permission_classes([IsAuthenticated])
	def get(self, request):
		logger.debug('Logging out user (get)')
		access_token = request.COOKIES.get('access_token')
		refresh_token = request.COOKIES.get('refresh_token')
		
		if not access_token or not refresh_token:
			return Response({'message': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
		
		user = request.user        
		
		# Blacklist the refresh token
	   # try:
		refresh_token = RefreshToken(refresh_token)
		if refresh_token.check_blacklist():
			response = Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)                        
			response.delete_cookie('access_token')
			response.delete_cookie('refresh_token')
			return response            
		refresh_token.blacklist()                
		response = Response({'message': 'Logged out successfully'})        
		# Delete the access and refresh token cookies
		response.delete_cookie('access_token')
		response.delete_cookie('refresh_token')
		return response


from social_django.models import UserSocialAuth

class deleteAccount(APIView):    
	@permission_classes([IsAuthenticated])
	def get(self, request):
		logger.debug('Anonymizing account')
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request, lookup_value=None):
    logger.debug('Fetching profile for user %s', lookup_value)
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
        'theme': serializer.data['theme'],
        'lang': serializer.data['lang'],
        'mfa_enabled': serializer.data['mfa_enabled'],
        'currentRank': serializer.data['stat_pong_solo_rank'],
    }
    return Response(preparedData)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStats(request, lookup_value=None):
	logger.debug('Fetching stats for user %s', lookup_value)
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
		# "4 Players Pong": {
		#   'currentRank': serializer.data['stat_pong_multi_rank'],
		#   'totalMatches': serializer.data['stat_pong_multi_wins_tot'] + serializer.data['stat_pong_multi_loss_tot'],
		#   'wins': serializer.data['stat_pong_multi_wins_tot'],
		#   'losses': serializer.data['stat_pong_multi_loss_tot'],
		#   'rankProgression': serializer.data['stat_pong_multi_progress'],
		#   'pointsWonUnder5Exchanges': serializer.data['stat_pong_multi_wins_tot_min5'],
		#   'pointsWonUnder10Exchanges': serializer.data['stat_pong_multi_wins_tot_min10'],
		#   'pointsWonOver10Exchanges': serializer.data['stat_pong_multi_wins_tot_max10'],
		#   'pointsLostUnder5Exchanges': serializer.data['stat_pong_multi_loss_tot_min5'],
		#   'pointsLostUnder10Exchanges': serializer.data['stat_pong_multi_loss_tot_min10'],
		#   'pointsLostOver10Exchanges': serializer.data['stat_pong_multi_loss_tot_max10']
		# },
		"Tic Tac Toe": {
		  'currentRank': serializer.data['stat_ttt_rank'],
		  'totalMatches': serializer.data['stat_ttt_wins_tot'] + serializer.data['stat_ttt_loss_tot'],          
		  'wins': serializer.data['stat_ttt_wins_tot'],
		  'losses': serializer.data['stat_ttt_loss_tot'],
		  'rankProgression': serializer.data['stat_ttt_progress'],
		  'averageMovesPerWin': serializer.data['stat_ttt_wins_av_movm'],
		  'averageMovesPerLoss': serializer.data['stat_ttt_loss_av_movm'],
		  'pointsWonUnder5Moves': serializer.data['stat_ttt_wins_tot_min5'],
		  'pointsWonUnder10Moves': serializer.data['stat_ttt_wins_tot_min10'],
		  'pointsWonOver10Moves': serializer.data['stat_ttt_wins_tot_max10'],
		  'pointsLostUnder5Moves': serializer.data['stat_ttt_loss_tot_min5'],
		  'pointsLostUnder10Moves': serializer.data['stat_ttt_loss_tot_min10'],
		  'pointsLostOver10Moves': serializer.data['stat_ttt_loss_tot_max10']
		  

		}
	  }


	}
	return Response(preparedData)

from .serializers import StatsUpdateSerializer

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateStats(request, lookup_value):
	logger.debug('Updating stats for user %s', lookup_value)
	"""
	Fetch user profile using either user ID or username.
	"""
	#if request.user == None:
	if request.user.username == 'api_user':
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
	logger.debug('Incrementing stats for user %s', lookup_value)
	"""
	Fetch user profile using either user ID or username.
	"""
	#if request.user == None:
	if request.user.username == 'api_user':
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


from .serializers import TTTStatsUpdateSerializer

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def stats_ttt(request):
	logger.debug('Incrementing TTT stats for user %s', request.user.username)
	"""
	Fetch user profile using either user ID or username.
	"""
	user = request.user
	serializer = TTTStatsUpdateSerializer(user, data=request.data, partial=True)
	if not serializer.is_valid():
		return Response(serializer.errors, status=400)	
	serializer.save()
	return Response(serializer.data)


	











import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_solo_progress(request, lookup_value):
	logger.debug('Updating progress for user %s', lookup_value)
	try:
		#if request.user == None:
		if request.user.username == 'api_user':
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
	logger.debug('Updating progress for user %s', lookup_value)
	try:
		#if request.user == None:
		if request.user.username == 'api_user':
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
	logger.debug('Updating progress for user %s', lookup_value)
	try:
		#if request.user == None:
		if request.user.username == 'api_user':
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



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
	logger.debug('Updating profile for user %s', request.user.username)
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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser  # Ensure you're using your custom user model
from .serializers import UserSerializer  # Your custom serializer for users

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated to access this data
def get_all_users(request):
	logger.debug('Fetching all users')
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
	logger.debug('Completing social auth')
	
	"""
	Retrieve the JWT tokens stored in the pipeline and return as JSON.
	"""
	jwt_tokens = request.session.get('jwt_tokens')

	if jwt_tokens:
		logout(request)  # This removes the session ID cookie
		# response = Response(jwt_tokens)        
		response = redirect("/profile")  # Redirect URL
		response.delete_cookie('sessionid') # This deletes the session ID cookie

		response.set_cookie("access_token", jwt_tokens["access"], httponly=True, secure=True, samesite="None")
		response.set_cookie("refresh_token", jwt_tokens["refresh"], httponly=True, secure=True, samesite="None")



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
	logger.debug('Redirect user for social auth')
	logout(request)  # This removes the session ID cookie
	logger.info('Logging out user before social auth')
	return redirect('social:begin', '42')


