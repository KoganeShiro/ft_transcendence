from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import get_all_users, getProfile, updateProfile, refresh_tokens, getStats, deleteAccount, updateStats, add_solo_progress, add_multi_progress, add_ttt_progress, incrementStats, setup_2fa, enable_2fa, disable_2fa

import logging
# from .views import callback

logger = logging.getLogger(__name__)

urlpatterns = [    
    #Authentication
    path('login/', views.Login.as_view(), name='token_obtain_pair'),
    path('login/refresh/', refresh_tokens, name='token_refresh'),
    #path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.Logout.as_view(), name='auth_logout'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('delete_account/', views.deleteAccount.as_view(), name='delete_account'),
    path('setup_2fa/', setup_2fa, name='2fa_setup'),
    path('enable_2fa/', enable_2fa, name='2fa_enable'),
    path('disable_2fa/', disable_2fa, name='2fa_disable'),

    #Profile
    path('profile/', getProfile, name='my_profile'),
    path('profile/<str:lookup_value>/', views.getProfile, name='profile'),
    path('profile_update/', updateProfile, name='update-profile'),
    path('stats/', getStats, name='my_stats'),
    path('stats/<str:lookup_value>/', views.getStats, name='stats'),
    path('stats_update/<str:lookup_value>/', updateStats, name='update-stats'),
    path('stats_increment/<str:lookup_value>/', incrementStats, name='increment-stats'),
    path('stats_prog_update/solo/<str:lookup_value>/', add_solo_progress , name='add_solo_progress'),
    path('stats_prog_update/multi/<str:lookup_value>/', add_multi_progress , name='add_multi_progress'),
    path('stats_prog_update/ttt/<str:lookup_value>/', add_ttt_progress , name='add_ttt_progress'),
   # path('profile/update/<str:lookup_value>/', views.updateProfile, name='update-profile'),
    path('users/', get_all_users, name='get_all_users'),  # Endpoint for all users
  #  path('users/', views , name='update-profile'),

    #Social Auth  
    path('auth/get_token/', views.social_auth_complete, name='social_auth_complete'),
    path('auth/login42/', views.social_auth_login, name='social_auth_login'),
    path('auth/', include('social_django.urls', namespace='social')),
]

logger.debug('URL patterns defined')