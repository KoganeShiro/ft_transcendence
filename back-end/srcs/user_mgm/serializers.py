from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username        
        # ...

        return token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired.'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception as e:
            self.fail('bad_token')
        




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])    
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    cover_photo = serializers.ImageField(
        required=False, allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'cover_photo')

    def create(self, validated_data):
  #      default_cover_photo = 'covers/default.jpg'
        user = CustomUser.objects.create(
        username=validated_data['username'],        
        cover_photo=validated_data.get('cover_photo', None),        
        )
        user.set_password(validated_data['password'])
      #  if user.cover_photo:
      #      user.cover_photo_url = user.cover_photo.url
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):    

    class Meta:
        model = CustomUser        
        exclude = ('password',)
    
    # def update(self, instance, validated_data):
    #     """
    #     Allow partial updates by checking for each field individually.
    #     """
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
        
    #     # Calculate online status based on last_seen
    #     current_time = timezone.now()
    #     last_seen = instance.last_seen
    #     time_difference = current_time - last_seen
    #     if time_difference.total_seconds() < 600:
    #         instance.online = True
    #     else:
    #         instance.online = False
        
    #     instance.save()
    #     return instance


class StatsUpdateSerializer(serializers.ModelSerializer):    

    class Meta:
        model = CustomUser
        fields = ('stat_pong_solo_rank', 'stat_pong_solo_progress', 'stat_pong_solo_wins_tot', 'stat_pong_solo_loss_tot', 'stat_pong_solo_tournament_wins', 'stat_pong_solo_tournament_loss', 'stat_pong_solo_wins_tot_min5', 'stat_pong_solo_loss_tot_min5', 'stat_pong_solo_wins_tot_min10', 'stat_pong_solo_loss_tot_min10', 'stat_pong_solo_wins_tot_max10', 'stat_pong_solo_loss_tot_max10', 'stat_pong_multi_rank', 'stat_pong_multi_progress', 'stat_pong_multi_wins_tot', 'stat_pong_multi_loss_tot', 'stat_pong_multi_wins_tot_min5', 'stat_pong_multi_loss_tot_min5', 'stat_pong_multi_wins_tot_min10', 'stat_pong_multi_loss_tot_min10', 'stat_pong_multi_wins_tot_max10', 'stat_pong_multi_loss_tot_max10', 'stat_ttt_rank', 'stat_ttt_progress', 'stat_ttt_wins_tot', 'stat_ttt_loss_tot', 'stat_ttt_wins_av_movm', 'stat_ttt_loss_av_movm')
              
       # exclude = ('password',)
    
    def update(self, instance, validated_data):
        """
        Allow partial updates by checking for each field individually.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)        
        instance.save()
        return instance
    

class StatsIncrementSerializer(serializers.ModelSerializer):    

    class Meta:
        model = CustomUser
        fields = ('stat_pong_solo_rank', 'stat_pong_solo_progress', 'stat_pong_solo_wins_tot', 'stat_pong_solo_loss_tot', 'stat_pong_solo_tournament_wins', 'stat_pong_solo_tournament_loss', 'stat_pong_solo_wins_tot_min5', 'stat_pong_solo_loss_tot_min5', 'stat_pong_solo_wins_tot_min10', 'stat_pong_solo_loss_tot_min10', 'stat_pong_solo_wins_tot_max10', 'stat_pong_solo_loss_tot_max10', 'stat_pong_multi_rank', 'stat_pong_multi_progress', 'stat_pong_multi_wins_tot', 'stat_pong_multi_loss_tot', 'stat_pong_multi_wins_tot_min5', 'stat_pong_multi_loss_tot_min5', 'stat_pong_multi_wins_tot_min10', 'stat_pong_multi_loss_tot_min10', 'stat_pong_multi_wins_tot_max10', 'stat_pong_multi_loss_tot_max10', 'stat_ttt_rank', 'stat_ttt_progress', 'stat_ttt_wins_tot', 'stat_ttt_loss_tot', 'stat_ttt_wins_av_movm', 'stat_ttt_loss_av_movm')
              
    def update(self, instance, validated_data):
        """
        Allow partial updates by checking for each field individually.
        """
        for attr, value in validated_data.items():
            if attr == 'stat_pong_solo_progress':
                if isinstance(value, list):
                    instance.stat_pong_solo_progress.extend(value)
                else:
                    instance.stat_pong_solo_progress.append(value)
            elif attr == 'stat_pong_multi_progress':
                if isinstance(value, list):
                    instance.stat_pong_multi_progress.extend(value)
                else:
                    instance.stat_pong_multi_progress.append(value)
            elif attr == 'stat_ttt_progress':
                if isinstance(value, list):
                    instance.stat_ttt_progress.extend(value)
                else:
                    instance.stat_ttt_progress.append(value)             
            else:
                setattr(instance, attr, getattr(instance, attr) + value)
        instance.save()
        return instance



class ProfileUpdateSerializer(serializers.ModelSerializer):    

    class Meta:
        model = CustomUser
        fields = ('username', 'cover_photo', 'password')        
       # exclude = ('password',)
    
    def update(self, instance, validated_data):
        """
        Allow partial updates by checking for each field individually.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])        
        instance.save()
        return instance


from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'cover_photo', 'last_seen')



