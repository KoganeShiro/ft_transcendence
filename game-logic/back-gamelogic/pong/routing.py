from django.urls import re_path
from . import consumers
from . import friends_consumer

websocket_urlpatterns = [
    re_path(r'ws/pong/$', consumers.PongConsumer.as_asgi()),
    re_path(r'ws/friendPong/(?P<room_name>\w+)/$', friends_consumer.FriendPongConsumer.as_asgi()), 
]
