from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
#    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        #fields = ('username', 'email', 'password', 'cover_photo')
        fields = ('username', 'email', 'password')

 #   def validate(self, attrs):
 #       if attrs['password'] != attrs['password2']:
 #           raise serializers.ValidationError(
 #               {"password": "Password fields didn't match."})

 #       return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
          #  bio=validated_data['bio'],
          #  cover_photo=validated_data['cover_photo']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ProfileSerializer(serializers.ModelSerializer):    

    class Meta:
        model = CustomUser
        fields = '__all__'
