from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PongViewSet, LastFivePongView, LastFiveMultiView, LastFiveTTTView, MultiViewSet, TTTViewSet

router = DefaultRouter()
router.register(r'pong', PongViewSet, basename='pong_game')
router.register(r'multi', MultiViewSet, basename='multi_game')
router.register(r'ttt', TTTViewSet, basename='ttt_game')
router.register(r'last_five_pong_games', LastFivePongView, basename='last_five_pong_games')
router.register(r'last_five_multi_games', LastFiveMultiView, basename='last_five_multi_games')
router.register(r'last_five_ttt_games', LastFiveTTTView, basename='last_five_ttt_games')

urlpatterns = [
    path('', include(router.urls)),  # API endpoints for games
]