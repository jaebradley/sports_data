"""dfs_site_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from data.views import DfsSiteViewSet, SportViewSet, LeagueViewSet, TeamViewSet, PositionViewSet, LeaguePositionViewSet, \
    SeasonViewSet, TeamSeasonViewSet, PlayerViewSet, GameViewSet, PlayerGameViewSet, \
    DailyFantasySportsSiteLeaguePositionViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'sites', DfsSiteViewSet, base_name='sites')
router.register(r'sports', SportViewSet, base_name='sites')
router.register(r'leagues', LeagueViewSet, base_name='leagues')
router.register(r'teams', TeamViewSet, base_name='teams')
router.register(r'positions', PositionViewSet, base_name='positions')
router.register(r'seasons', SeasonViewSet, base_name='seasons')
router.register(r'team-seasons', TeamSeasonViewSet, base_name='team-seasons')
router.register(r'league-positions', LeaguePositionViewSet, base_name='league-positions')
router.register(r'players', PlayerViewSet, base_name='players')
router.register(r'games', GameViewSet, base_name='games')
router.register(r'player-games', PlayerGameViewSet, base_name='player-games')
router.register(r'daily-fantasy-sports-sites/league-positions', DailyFantasySportsSiteLeaguePositionViewSet, base_name='daily-fantasy-sports-sites-league-positions')

urlpatterns = [
    url(r'^', include(router.urls)),
]
