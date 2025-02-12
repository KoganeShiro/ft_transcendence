from rest_framework import serializers
from .models import blocked_User, muted_User, messages, Friendship

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'

class blocked_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = blocked_User
        fields = '__all__'

class muted_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = muted_User
        fields = '__all__'

class messagesSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = messages
        fields = '__all__'
        extra_kwargs = {
            'sender': {'write_only': True},
            'receiver': {'write_only': True}
        }

class messagesSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = messages
        fields = '__all__'
