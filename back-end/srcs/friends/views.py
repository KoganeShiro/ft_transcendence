from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Friendship, muted_User, blocked_User, messages
from .serializers import FriendSerializer, muted_UserSerializer, blocked_UserSerializer, messagesSerializer, messagesSerializerWrite
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from user_mgm.models import CustomUser
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_friends(request):
    user = request.user
    blocked_users = blocked_User.objects.filter(blocker=user).values_list('blocked_id', flat=True)  
    friends = Friendship.objects.filter(
#        (Q(user=user) | Q(friend=user)) &         
#        ~Q(friend__in=blocked_users)
        (Q(user=user) | Q(friend=user))
    ).select_related('user', 'friend')
    
    friends_list = []
    for friendship in friends:
        friend = friendship.friend if friendship.user == user else friendship.user
        is_online = friend.last_seen > timezone.now() - timezone.timedelta(minutes=5)
        is_blocked = blocked_User.objects.filter(blocker=user, blocked=friend).exists()
        friends_list.append({
            'username': friend.username,
            'online_status': is_online,
            'is_blocked': is_blocked
        })
    
    return Response(friends_list)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def block_user(request):
    username_to_block = request.data.get('username')
    if not username_to_block:
        return Response({'error': 'Username is required'}, status=400)
    
    try:
        user_to_block = CustomUser.objects.get(username=username_to_block)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)
    
    if blocked_User.objects.filter(blocker=request.user, blocked=user_to_block).exists():
        return Response({'error': 'User is already blocked'}, status=400)

    blocked_User.objects.create(blocker=request.user, blocked=user_to_block)
    return Response({'success': f'User {username_to_block} has been blocked'}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unblock_user(request):
    username_to_unblock = request.data.get('username')
    if not username_to_unblock:
        return Response({'error': 'Username is required'}, status=400)
    
    try:
        user_to_unblock = CustomUser.objects.get(username=username_to_unblock)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)
    
    blocked_user = blocked_User.objects.filter(blocker=request.user, blocked=user_to_unblock).first()
    if not blocked_user:
        return Response({'error': 'User is not blocked'}, status=400)
    
    blocked_user.delete()
    return Response({'success': f'User {username_to_unblock} has been unblocked'}, status=200)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(request):
    username_to_add = request.data.get('username')
    if not username_to_add:
        return Response({'error': 'Username is required'}, status=400)
    
    try:
        user_to_add = CustomUser.objects.get(username=username_to_add)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)
    
    if Friendship.objects.filter(user=request.user, friend=user_to_add).exists() or Friendship.objects.filter(user=user_to_add, friend=request.user).exists():
        return Response({'error': 'Friendship already exists'}, status=400)
    
    Friendship.objects.create(user=request.user, friend=user_to_add)
    return Response({'success': f'User {username_to_add} has been added as a friend'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_friend(request):
    username_to_remove = request.data.get('username')
    if not username_to_remove:
        return Response({'error': 'Username is required'}, status=400)
    
    try:
        user_to_remove = CustomUser.objects.get(username=username_to_remove)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)
    
    friendship = Friendship.objects.filter(
        (Q(user=request.user) & Q(friend=user_to_remove)) | 
        (Q(user=user_to_remove) & Q(friend=request.user))
    ).first()
    
    if not friendship:
        return Response({'error': 'Friendship does not exist'}, status=400)
    
    friendship.delete()
    return Response({'success': f'User {username_to_remove} has been removed from friends'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    receiver_username = request.data.get('receiver')
    message_content = request.data.get('message')
    
    if not receiver_username or not message_content:
        return Response({'error': 'Receiver and message content are required'}, status=400)
    
    if len(message_content) > 160:
        return Response({'error': 'Message content exceeds 160 characters'}, status=400)
    
    try:
        receiver = CustomUser.objects.get(username=receiver_username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Receiver does not exist'}, status=404)
    
    messages.objects.create(sender=request.user, receiver=receiver, message=message_content)
    return Response({'success': 'Message sent successfully'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_last_15_messages(request):
    other_username = request.data.get('username')
    if not other_username:
        return Response({'error': 'Username is required'}, status=400)
    
    try:
        other_user = CustomUser.objects.get(username=other_username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)
    
    user = request.user
    last_15_messages = messages.objects.filter(
        (Q(sender=user) & Q(receiver=other_user)) | 
        (Q(sender=other_user) & Q(receiver=user))
    ).order_by('-timestamp')[:15]
    
    serializer = messagesSerializer(last_15_messages, many=True)
    
    return Response(serializer.data)

# class FriendshipViewSet(viewsets.ModelViewSet):
#     queryset = Friendship.objects.all()
#     serializer_class = FriendshipSerializer
#     permission_classes = [IsAuthenticated]

# class muted_UserViewSet(viewsets.ModelViewSet):
#     queryset = muted_User.objects.all()
#     serializer_class = muted_UserSerializer
#     permission_classes = [IsAuthenticated]

# class blocked_UserViewSet(viewsets.ModelViewSet):
#     queryset = blocked_User.objects.all()
#     serializer_class = blocked_UserSerializer
#     permission_classes = [IsAuthenticated]

# class messagesViewSet(viewsets.ModelViewSet):
#     queryset = messages.objects.all()
#     serializer_class = messagesSerializer
#     permission_classes = [IsAuthenticated]
#     def get_serializer_class(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH']:  # Use write serializer for input
#             return messagesSerializerWrite
#         return messagesSerializer  # Use read serializer for output
    
#     def get_queryset(self):
#         user = self.request.user
#         friends = Friendship.objects.filter(user=user, friend__blocked_user__isnull=True, friend__muted_user__isnull=True)
#         friend_ids = friends.values_list('friend_id', flat=True)
#         return messages.objects.filter(sender__in=friend_ids, receiver=user) | messages.objects.filter(sender=user, receiver__in=friend_ids)