from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import OAuth2Login, OAuth2Complete, get_all_users
import logging
# from .views import callback

logger = logging.getLogger(__name__)

urlpatterns = [    
    #Authentication
    path('token/', views.Login.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.Logout.as_view(), name='auth_logout'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/<str:lookup_value>/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
    path('profile/update/<str:lookup_value>/', views.updateProfile, name='update-profile'),
    path('users/', get_all_users, name='get_all_users'),  # Endpoint for all users
  #  path('users/', views , name='update-profile'),

    #Social Auth
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/login42/', OAuth2Login.as_view(), name='oauth2_login'),
    path('auth/complete42/<str:backend>/', OAuth2Complete.as_view(), name='oauth2_complete'),
    #path('auth/complete42/42/', OAuth2Complete.as_view(), name='oauth2_complete'),

]

logger.debug('URL patterns defined')
