from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login, callback


urlpatterns = [    
    #Authentication
    path('token/', views.Login.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.Logout.as_view(), name='auth_logout'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    #Social Auth
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', login, name='login'),
    path('auth/complete/42/', callback, name='callback'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
]

