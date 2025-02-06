from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from .models import Friendship, muted_User, blocked_User, messages
# from .serializers import FriendshipSerializer, muted_UserSerializer, blocked_UserSerializer, messagesSerializer

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