from django.urls import path
from .views import user_friends, block_user, add_friend, remove_friend, send_message, get_last_15_messages, unblock_user

urlpatterns = [
    path('user_friends/', user_friends),
    path('block_user/', block_user),
    path('unblock_user/', unblock_user),

    path('add_friend/', add_friend),
    path('remove_friend/', remove_friend),    
    path('send_message/', send_message),
    path('get_last_15_messages/', get_last_15_messages),
]
