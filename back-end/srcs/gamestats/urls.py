from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, LastFiveGamesView

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'last_five_solo_games', LastFiveGamesView, basename='last_five_games')

urlpatterns = [
    path('', include(router.urls)),  # API endpoints for games
]