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

from data.views import sport_leagues_list, sport_leagues_detail, team_detail, teams_list, sports_list, sport_detail, \
    players_list, games_list, player_detail, game_detail, seasons_list, league_position_list, league_position_detail
from dfs_site_persistence.views import daily_fantasy_sports_site_list, daily_fantasy_sports_site_detail, \
    daily_fantasy_sports_site_league_position_list, daily_fantasy_sports_site_league_position_detail, \
    daily_fantasy_sports_site_league_position_group_list, daily_fantasy_sports_site_league_position_group_detail, \
    daily_fantasy_sports_site_player_game_list
from nba_persistence.views import game_player_box_score_list, game_player_box_score_detail

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^sports/$', sports_list, name='sports_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/$', sport_detail, name='sport_detail'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/$', sport_leagues_list, name='sport_leagues_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/$', sport_leagues_detail, name='sport_leagues_detail'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/teams/$', teams_list, name='teams_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/teams/(?P<team_id>[0-9]+)/$', team_detail, name='team_detail'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/players/$', players_list, name='players_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/players/(?P<player_id>[0-9]+)$',
        player_detail, name='player_detail'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/games/$', games_list, name='games_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/games/(?P<game_id>[0-9]+)/$',
        game_detail, name='game_detail'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/seasons/$', seasons_list, name='seasons_list'),

    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/positions/$',
        league_position_list, name='league_position_list'),
    url(r'^sports/(?P<sport_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/positions/(?P<position_id>[0-9]+)/$',
        league_position_detail, name='league_position_detail'),

    url(r'^daily-fantasy-sports-sites/$', daily_fantasy_sports_site_list, name='daily_fantasy_sports_site_list'),
    url(r'^daily-fantasy-sports-sites/(?P<pk>[0-9]+)/$', daily_fantasy_sports_site_detail,
        name='daily_fantasy_sports_site_detail'),

    url(r'^daily-fantasy-sports-sites/(?P<daily_fantasy_sports_site_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/positions/$',
        daily_fantasy_sports_site_league_position_list, name='daily_fantasy_sports_site_league_position_list'),
    url(r'^daily-fantasy-sports-sites/(?P<daily_fantasy_sports_site_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/positions/(?P<position_id>[0-9]+)/$',
        daily_fantasy_sports_site_league_position_detail, name='daily_fantasy_sports_site_league_position_detail'),

    url(r'^daily-fantasy-sports-sites/(?P<daily_fantasy_sports_site_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/position-groups/$',
        daily_fantasy_sports_site_league_position_group_list, name='daily_fantasy_sports_site_league_position_group_list'),
    url(r'^daily-fantasy-sports-sites/(?P<daily_fantasy_sports_site_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/position-groups/(?P<position_group_id>[0-9]+)/$',
        daily_fantasy_sports_site_league_position_group_detail, name='daily_fantasy_sports_site_league_position_group_detail'),

    url(r'^daily-fantasy-sports-sites/(?P<daily_fantasy_sports_site_id>[0-9]+)/leagues/(?P<league_id>[0-9]+)/player-games/$',
        daily_fantasy_sports_site_player_game_list, name='daily_fantasy_sports_site_player_game_list'),

    url(r'^box-scores/$', game_player_box_score_list, name='box_scores_list'),
    url(r'^box-scores/(?P<box_score_id>[0-9]+)/$', game_player_box_score_detail, name='box_scores_detail')
]
