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

from data.view_sets import SportViewSet, LeagueViewSet, TeamViewSet, PositionViewSet, LeaguePositionViewSet, \
    SeasonViewSet, TeamSeasonViewSet, PlayerViewSet, GameViewSet, PlayerGameViewSet
from data.views import daily_fantasy_sports_site_list, daily_fantasy_sports_site_detail, \
    daily_fantasy_sports_site_league_position_list, daily_fantasy_sports_site_league_position_detail, \
    daily_fantasy_sports_site_league_position_group_list, daily_fantasy_sports_site_league_position_group_detail, \
    daily_fantasy_sports_site_player_game_list, daily_fantasy_sports_site_player_game_detail

# Create a router and register our viewsets with it.
router = DefaultRouter()
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

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^daily-fantasy-sports-sites/$', daily_fantasy_sports_site_list, name='daily_fantasy_sports_site_list'),
    url(r'^daily-fantasy-sports-sites/(?P<pk>[0-9]+)/$', daily_fantasy_sports_site_detail,
        name='daily_fantasy_sports_site_detail'),

    url(r'^daily-fantasy-sports-sites/leagues/positions/$', daily_fantasy_sports_site_league_position_list,
        name='daily_fantasy_sports_site_league_position_list'),
    url(r'^daily-fantasy-sports-sites/leagues/positions/(?P<pk>[0-9]+)/$',
        daily_fantasy_sports_site_league_position_detail, name='daily_fantasy_sports_site_league_position_detail'),

    url(r'^daily-fantasy-sports-sites/leagues/positions/groups/', daily_fantasy_sports_site_league_position_group_list,
        name='daily_fantasy_sports_site_league_position_group_list'),
    url(r'^daily-fantasy-sports-sites/leagues/positions/groups/(?P<pk>[0-9]+)/$',
        daily_fantasy_sports_site_league_position_group_detail, name='daily_fantasy_sports_site_league_position_group_detail'),

    url(r'^daily-fantasy-sports-sites/games/players/$', daily_fantasy_sports_site_player_game_list,
        name='daily_fantasy_sports_site_player_game_list'),
    url(r'^daily-fantasy-sports-sites/games/players/(?P<pk>[0-9]+)/$',
        daily_fantasy_sports_site_player_game_detail, name='daily_fantasy_sports_site_player_game_detail'),
]
