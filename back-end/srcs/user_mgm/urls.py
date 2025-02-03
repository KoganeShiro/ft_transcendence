from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import OAuth2Login, OAuth2Complete
# from .views import callback


urlpatterns = [    
    #Authentication
    path('token/', views.Login.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.Logout.as_view(), name='auth_logout'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),

    #Social Auth
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/login/', OAuth2Login.as_view(), name='oauth2_login'),
    path('auth/complete/<str:backend>/', OAuth2Complete.as_view(), name='oauth2_complete'),

]

