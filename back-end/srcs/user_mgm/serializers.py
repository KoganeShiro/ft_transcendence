from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'rank', 'password', 'avatar']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # Get the password if provided

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # If a new password is provided, hash it and set it
        if password:
            instance.set_password(password)
        
        instance.save()  # Save the updated instance
        return instance